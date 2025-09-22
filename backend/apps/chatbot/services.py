import requests
from django.conf import settings
from apps.chatbot.models import Venue, Booking, PriceTier, AdditionalService, JTCCHistory, Contact
from datetime import datetime, timedelta
import json

class OpenRouterService:
    def __init__(self):
        self.api_key = getattr(settings, 'OPENROUTER_API_KEY', '')
        self.api_url = getattr(settings, 'OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1/chat/completions')
        self.default_model = 'openai/gpt-3.5-turbo'
        self.temperature = 0.7
        self.max_tokens = 1000
        
        # Check if API key is configured
        if not self.api_key:
            print("WARNING: OPENROUTER_API_KEY not set. Using fallback responses.")
    
    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': getattr(settings, 'SITE_URL', 'http://localhost:3000'),
            'X-Title': getattr(settings, 'SITE_NAME', 'EventAura'),
        }

    def generate_response(self, message, conversation_history=None):
        """Generate response using OpenRouter API with database context"""
        
        # First, try to get database-specific information
        db_context = self._get_database_context(message)
        
        # If no API key, use enhanced fallback responses with database data
        if not self.api_key:
            return self._get_enhanced_fallback_response(message, db_context)
        
        messages = []
        
        # Add system prompt with database context
        system_prompt = f"""You are EventAura assistant for Jaffna Thiruvalluvar Cultural Centre.
        Help users with venue bookings, pricing, and event information.
        Be helpful, friendly, and professional.
        
        Current database information:
        {db_context}
        
        Use this information to provide accurate, specific answers about venues, bookings, and availability."""
        
        messages.append({'role': 'system', 'content': system_prompt})
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current message
        messages.append({'role': 'user', 'content': message})
        
        payload = {
            'model': self.default_model,
            'messages': messages,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.get_headers(),
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            response_data = response.json()
            
            if 'choices' in response_data and len(response_data['choices']) > 0:
                return response_data['choices'][0]['message']['content']
            else:
                raise Exception("Invalid response from OpenRouter")
                
        except Exception as e:
            print(f"OpenRouter API error: {str(e)}")
            # Fallback to enhanced local response if API fails
            return self._get_enhanced_fallback_response(message, db_context)
    
    def _get_database_context(self, message):
        """Get relevant database information based on the message"""
        message_lower = message.lower()
        context = []
        
        try:
            # Get venue information
            if any(word in message_lower for word in ['venue', 'space', 'hall', 'room', 'available', 'list', 'auditorium', 'conference', 'amphitheatre', 'library', 'exhibition']):
                venues = Venue.objects.filter(status='active')
                if venues.exists():
                    context.append("🏛️ Available Venues at JTCC:")
                    for venue in venues:
                        context.append(f"\n📍 {venue.venue_name}")
                        context.append(f"   Capacity: {venue.capacity} people")
                        context.append(f"   Description: {venue.description[:200]}...")
                        
                        # Get pricing for this venue
                        price_tiers = PriceTier.objects.filter(venue=venue).order_by('duration')
                        if price_tiers.exists():
                            context.append("   💰 Pricing:")
                            for tier in price_tiers:
                                context.append(f"      {tier.duration}h: LKR {tier.price:,.2f}")
                else:
                    context.append("No venues currently available.")
            
            # Get booking information
            if any(word in message_lower for word in ['booking', 'booked', 'reservation', 'schedule', 'book']):
                recent_bookings = Booking.objects.filter(
                    created_at__gte=datetime.now() - timedelta(days=7)
                ).order_by('-created_at')[:5]
                
                if recent_bookings.exists():
                    context.append("📅 Recent Bookings:")
                    for booking in recent_bookings:
                        venue_name = booking.venue.venue_name if booking.venue else f"Venue {booking.venue_id}"
                        context.append(f"- {venue_name} on {booking.event_date} {booking.start_time}")
                        context.append(f"  Status: {booking.status}, Hours: {booking.total_hours}")
                else:
                    context.append("No recent bookings found.")
            
            # Get pricing information
            if any(word in message_lower for word in ['price', 'cost', 'rate', 'fee', 'pricing', 'how much']):
                venues = Venue.objects.filter(status='active')
                if venues.exists():
                    context.append("💰 Venue Pricing:")
                    for venue in venues:
                        context.append(f"\n📍 {venue.venue_name}:")
                        price_tiers = PriceTier.objects.filter(venue=venue).order_by('duration')
                        for tier in price_tiers:
                            context.append(f"   {tier.duration}h: LKR {tier.price:,.2f}")
            
            # Get capacity information
            if any(word in message_lower for word in ['capacity', 'people', 'size', 'large', 'small', 'how many']):
                venues = Venue.objects.filter(status='active').order_by('capacity')
                if venues.exists():
                    context.append("👥 Venue Capacities:")
                    for venue in venues:
                        context.append(f"- {venue.venue_name}: {venue.capacity} people")
            
            # Get additional services
            if any(word in message_lower for word in ['service', 'amenities', 'sound', 'lighting', 'catering', 'security', 'cleaning']):
                services = AdditionalService.objects.all()
                if services.exists():
                    context.append("🔧 Additional Services:")
                    for service in services:
                        mandatory = " (Required)" if service.is_mandatory else ""
                        context.append(f"- {service.service_name}{mandatory}: LKR {service.basic_rate:,.2f} + LKR {service.extra_hourly_rate:,.2f}/hour")
            
            # Get JTCC information
            if any(word in message_lower for word in ['jtcc', 'centre', 'center', 'about', 'information', 'history']):
                jtcc_info = JTCCHistory.objects.first()
                if jtcc_info:
                    context.append("🏛️ About JTCC:")
                    context.append(f"Official Name: {jtcc_info.official_name}")
                    context.append(f"Location: {jtcc_info.location}")
                    context.append(f"Description: {jtcc_info.description[:300]}...")
                    context.append(f"Facilities: {jtcc_info.facilities}")
            
            # Get contact information
            if any(word in message_lower for word in ['contact', 'phone', 'email', 'call', 'reach']):
                contact = Contact.objects.first()
                if contact:
                    context.append("📞 Contact Information:")
                    context.append(f"Phone: {contact.phone_number}")
                    context.append(f"Email: {contact.email}")
                    context.append(f"Available: {contact.available_time}")
            
        except Exception as e:
            print(f"Error getting database context: {str(e)}")
            context.append("Database information temporarily unavailable.")
        
        return "\n".join(context) if context else "No specific database information available."
    
    def _get_enhanced_fallback_response(self, message, db_context):
        """Provide enhanced fallback responses with database information"""
        message_lower = message.lower()
        
        # Venue-related queries
        if any(word in message_lower for word in ['venue', 'space', 'hall', 'room', 'auditorium', 'conference', 'amphitheatre', 'library', 'exhibition']):
            if "🏛️ Available Venues at JTCC:" in db_context:
                return f"🏛️ Welcome to Jaffna Thiruvalluvar Cultural Centre! Here are our available venues:\n\n{db_context}\n\nWhich venue interests you most? I can provide more details about any of these spaces!"
            else:
                return "🏛️ I can help you with venue bookings at JTCC! We have various spaces available including auditoriums, conference halls, and outdoor areas. What type of event are you planning?"
        
        # Pricing queries
        elif any(word in message_lower for word in ['price', 'cost', 'rate', 'fee', 'pricing', 'how much', 'expensive', 'cheap']):
            if "💰 Venue Pricing:" in db_context:
                return f"💰 Here are our current venue rates:\n\n{db_context}\n\nAll prices are in Sri Lankan Rupees (LKR). Would you like more specific pricing information for a particular venue or duration?"
            else:
                return "💰 Our venue pricing varies based on size, duration, and amenities. We offer flexible pricing from 2-hour sessions to full-day events. What type of event are you planning?"
        
        # Booking queries
        elif any(word in message_lower for word in ['book', 'reserve', 'schedule', 'booking', 'reservation']):
            return "📅 Great! I'd be happy to help you book a venue at JTCC. To get started, I'll need to know:\n• What type of event?\n• How many people?\n• Preferred date and time?\n• Which venue interests you?\n\nYou can also ask me about availability for specific dates!"
        
        # Availability queries
        elif any(word in message_lower for word in ['availability', 'available', 'free', 'open', 'when']):
            if "🏛️ Available Venues at JTCC:" in db_context:
                return f"📅 Here are our available venues:\n\n{db_context}\n\nPlease let me know the date and time you're interested in, and I can check specific availability for that period!"
            else:
                return "📅 I can check venue availability for you! Please let me know the date and time you're interested in, and I'll show you what's available at JTCC."
        
        # Capacity queries
        elif any(word in message_lower for word in ['capacity', 'people', 'size', 'large', 'small', 'how many', 'accommodate']):
            if "👥 Venue Capacities:" in db_context:
                return f"👥 Here are our venue capacities:\n\n{db_context}\n\nWhat size event are you planning? I can recommend the best venue based on your guest count!"
            else:
                return "👥 Our venues have different capacities ranging from intimate gatherings to large events. What size event are you planning? I can help you find the perfect space!"
        
        # Services queries
        elif any(word in message_lower for word in ['service', 'amenities', 'sound', 'lighting', 'catering', 'security', 'cleaning', 'include']):
            if "🔧 Additional Services:" in db_context:
                return f"🔧 Here are our additional services:\n\n{db_context}\n\nThese services can enhance your event experience. Which services are you interested in?"
            else:
                return "🔧 We offer various additional services including sound systems, lighting, catering, security, and more. What services would you like to know about?"
        
        # JTCC information queries
        elif any(word in message_lower for word in ['jtcc', 'centre', 'center', 'about', 'information', 'history', 'what is']):
            if "🏛️ About JTCC:" in db_context:
                return f"🏛️ Here's information about our cultural centre:\n\n{db_context}\n\nIs there anything specific about JTCC you'd like to know more about?"
            else:
                return "🏛️ Jaffna Thiruvalluvar Cultural Centre (JTCC) is a modern cultural facility promoting cultural exchange and community development. We offer various venues for events, conferences, and cultural activities. What would you like to know about us?"
        
        # Contact queries
        elif any(word in message_lower for word in ['contact', 'phone', 'email', 'call', 'reach', 'speak', 'talk']):
            if "📞 Contact Information:" in db_context:
                return f"📞 Here's how you can reach us:\n\n{db_context}\n\nFeel free to contact us for any questions or to make a booking!"
            else:
                return "📞 You can contact us at +94 21 222 1234 or info@jtcc.lk. We're available Monday to Friday, 9:00 AM - 5:00 PM. How can I help you today?"
        
        # Greeting
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return "👋 Hello! Welcome to Jaffna Thiruvalluvar Cultural Centre (JTCC)! I'm your virtual assistant and I'm here to help you with:\n• Venue bookings and reservations\n• Pricing information\n• Event planning assistance\n• Information about our facilities\n\nHow can I assist you today?"
        
        # Help queries
        elif any(word in message_lower for word in ['help', 'what can you do', 'assist', 'support']):
            return "🤝 I'm here to help you with everything related to JTCC! I can assist you with:\n\n🏛️ **Venue Information** - Details about our auditoriums, conference halls, and outdoor spaces\n💰 **Pricing** - Rates for different venues and durations\n📅 **Bookings** - Help you reserve venues for your events\n🔧 **Services** - Information about additional services like catering, sound, lighting\n📞 **Contact** - How to reach us\n\nWhat would you like to know about?"
        
        # Default response
        else:
            return "Thank you for your message! I'm here to help you with venue bookings and event planning at JTCC. You can ask me about:\n• Available venues and their capacities\n• Pricing for different durations\n• How to make a booking\n• Additional services we offer\n• Information about our cultural centre\n\nWhat would you like to know about?"
    
    def _get_fallback_response(self, message):
        """Legacy fallback method - redirects to enhanced version"""
        return self._get_enhanced_fallback_response(message, "")