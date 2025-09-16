import requests
from django.conf import settings
from apps.booking.models import Venue, Booking
from apps.chatbot.models import ChatbotMessage
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
            if any(word in message_lower for word in ['venue', 'space', 'hall', 'room', 'available', 'list']):
                venues = Venue.objects.all()
                if venues.exists():
                    context.append("Available Venues:")
                    for venue in venues:
                        context.append(f"- {venue.venue_name}: Capacity {venue.capacity}")
                        context.append(f"  Rates: 2h=${venue.base_rate_2h}, 4h=${venue.base_rate_4h}, 6h=${venue.base_rate_6h}, 6h+=${venue.base_rate_6h_plus}")
                        context.append(f"  Description: {venue.description}")
                else:
                    context.append("No venues currently available.")
            
            # Get booking information
            if any(word in message_lower for word in ['booking', 'booked', 'reservation', 'schedule']):
                recent_bookings = Booking.objects.filter(
                    created_at__gte=datetime.now() - timedelta(days=7)
                ).order_by('-created_at')[:5]
                
                if recent_bookings.exists():
                    context.append("Recent Bookings:")
                    for booking in recent_bookings:
                        venue_name = booking.venue.venue_name if booking.venue else f"Venue {booking.venue_id}"
                        context.append(f"- {venue_name} on {booking.event_date} {booking.start_time}")
                        context.append(f"  Status: {booking.status}, Hours: {booking.total_hours}")
                else:
                    context.append("No recent bookings found.")
            
            # Get pricing information
            if any(word in message_lower for word in ['price', 'cost', 'rate', 'fee']):
                venues = Venue.objects.all()
                if venues.exists():
                    context.append("Venue Pricing:")
                    for venue in venues:
                        context.append(f"- {venue.venue_name}: 2h=${venue.base_rate_2h}, 4h=${venue.base_rate_4h}, 6h=${venue.base_rate_6h}, 6h+=${venue.base_rate_6h_plus}")
            
            # Get capacity information
            if any(word in message_lower for word in ['capacity', 'people', 'size', 'large', 'small']):
                venues = Venue.objects.all().order_by('capacity')
                if venues.exists():
                    context.append("Venue Capacities:")
                    for venue in venues:
                        context.append(f"- {venue.venue_name}: {venue.capacity} people")
            
        except Exception as e:
            print(f"Error getting database context: {str(e)}")
            context.append("Database information temporarily unavailable.")
        
        return "\n".join(context) if context else "No specific database information available."
    
    def _get_enhanced_fallback_response(self, message, db_context):
        """Provide enhanced fallback responses with database information"""
        message_lower = message.lower()
        
        # Venue-related queries
        if any(word in message_lower for word in ['venue', 'space', 'hall', 'room']):
            if "Available Venues:" in db_context:
                return f"I can help you with venue bookings! Here's what we have available:\n\n{db_context}\n\nWhat type of venue are you looking for?"
            else:
                return "I can help you with venue bookings! We have various spaces available. What type of venue are you looking for?"
        
        # Pricing queries
        elif any(word in message_lower for word in ['price', 'cost', 'rate', 'fee']):
            if "Venue Pricing:" in db_context:
                return f"Here are our current venue rates:\n\n{db_context}\n\nWould you like more specific pricing information for a particular venue?"
            else:
                return "Our venue pricing varies based on size, duration, and amenities. Would you like more specific pricing information?"
        
        # Booking queries
        elif any(word in message_lower for word in ['book', 'reserve', 'schedule']):
            return "Great! To book a venue, I'll need to know the date, time, number of people, and type of event. You can also check availability for specific dates. When would you like to book?"
        
        # Availability queries
        elif any(word in message_lower for word in ['availability', 'available', 'free']):
            if "Available Venues:" in db_context:
                return f"Here's our current availability:\n\n{db_context}\n\nPlease let me know the date and time you're interested in, and I can check specific availability."
            else:
                return "I can check venue availability for you. Please let me know the date and time you're interested in, and I'll show you what's available."
        
        # Capacity queries
        elif any(word in message_lower for word in ['capacity', 'people', 'size', 'large', 'small']):
            if "Venue Capacities:" in db_context:
                return f"Here are our venue capacities:\n\n{db_context}\n\nWhat size event are you planning?"
            else:
                return "Our venues have different capacities. What size event are you planning?"
        
        # Greeting
        elif any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! Welcome to EventAura. I'm here to help you with venue bookings, pricing information, and event planning. How can I assist you today?"
        
        # Default response
        else:
            return "Thank you for your message! I'm here to help with venue bookings and event planning. You can ask me about available spaces, pricing, or how to make a reservation. What would you like to know?"
    
    def _get_fallback_response(self, message):
        """Legacy fallback method - redirects to enhanced version"""
        return self._get_enhanced_fallback_response(message, "")