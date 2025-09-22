#!/usr/bin/env python
"""
Add detailed venue information for better chatbot understanding
"""
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.chatbot.models import (
    Venue, VenueImage, PriceTier, AdditionalService, 
    JTCCHistory, JTCCFunder, JTCCFacility, JTCCMilestone, Contact
)
from django.contrib.auth.models import User

def add_detailed_venue_data():
    print("Adding detailed venue information...")
    
    # Clear existing venues first
    Venue.objects.all().delete()
    PriceTier.objects.all().delete()
    
    # Create detailed venues with comprehensive information
    venues_data = [
        {
            'venue_name': 'Main Auditorium',
            'capacity': 600,
            'description': '''The Main Auditorium is our flagship venue, perfect for large conferences, cultural events, and major ceremonies. Features include:
            - State-of-the-art sound system with wireless microphones
            - Professional lighting with stage spotlights
            - Air conditioning and comfortable seating
            - Stage area: 40ft x 20ft
            - Green room and dressing rooms
            - Wheelchair accessible
            - Parking for 200+ vehicles
            - Perfect for: Weddings, conferences, cultural shows, graduation ceremonies''',
            'status': 'active',
            'image': 'https://example.com/auditorium.jpg'
        },
        {
            'venue_name': 'Conference Hall',
            'capacity': 100,
            'description': '''The Conference Hall is ideal for business meetings, seminars, and small gatherings. Features include:
            - Professional presentation equipment
            - Projector and large screen
            - Whiteboard and flipchart
            - Round table seating for 50 people
            - Theater-style seating for 100 people
            - High-speed WiFi
            - Coffee and tea service available
            - Perfect for: Business meetings, training sessions, workshops, board meetings''',
            'status': 'active',
            'image': 'https://example.com/conference.jpg'
        },
        {
            'venue_name': 'Pond Amphitheatre',
            'capacity': 300,
            'description': '''The Pond Amphitheatre offers a unique outdoor experience with natural ambiance. Features include:
            - Open-air setting with beautiful pond view
            - Natural acoustics
            - Covered stage area
            - Tiered seating with stone benches
            - Natural lighting during day
            - Evening lighting available
            - Perfect for: Cultural performances, outdoor ceremonies, music concerts, poetry readings
            - Note: Weather dependent, backup indoor option available''',
            'status': 'active',
            'image': 'https://example.com/amphitheatre.jpg'
        },
        {
            'venue_name': 'Digital Library',
            'capacity': 50,
            'description': '''The Digital Library is a modern space perfect for quiet study, research, and small academic events. Features include:
            - 20 computer workstations
            - High-speed internet
            - Quiet study areas
            - Reference materials and books
            - Printing and scanning facilities
            - Group study rooms
            - Perfect for: Study groups, research presentations, academic workshops, quiet meetings''',
            'status': 'active',
            'image': 'https://example.com/library.jpg'
        },
        {
            'venue_name': 'Exhibition Hall',
            'capacity': 200,
            'description': '''The Exhibition Hall is perfect for trade shows, art exhibitions, and product launches. Features include:
            - Large open space with high ceilings
            - Flexible layout options
            - Display panels and stands
            - Good lighting for exhibits
            - Easy loading/unloading access
            - Perfect for: Art exhibitions, trade shows, product launches, craft fairs, cultural displays''',
            'status': 'active',
            'image': 'https://example.com/exhibition.jpg'
        }
    ]
    
    for venue_data in venues_data:
        venue, created = Venue.objects.get_or_create(
            venue_name=venue_data['venue_name'],
            defaults=venue_data
        )
        if created:
            print(f"✅ Created venue: {venue.venue_name}")
            
            # Create detailed price tiers for each venue
            price_tiers = [
                {'duration': 2, 'price': 5000.00, 'description': '2 hours - Perfect for short meetings'},
                {'duration': 4, 'price': 9000.00, 'description': '4 hours - Half day events'},
                {'duration': 6, 'price': 12000.00, 'description': '6 hours - Full day events'},
                {'duration': 8, 'price': 15000.00, 'description': '8 hours - Extended events'},
                {'duration': 10, 'price': 18000.00, 'description': '10 hours - All day events'},
            ]
            
            for tier_data in price_tiers:
                PriceTier.objects.create(
                    venue=venue,
                    duration=tier_data['duration'],
                    price=tier_data['price']
                )
    
    # Add comprehensive additional services
    services_data = [
        {
            'service_name': 'Sound System & Microphones',
            'basic_rate': 2000.00,
            'extra_hourly_rate': 500.00,
            'is_mandatory': False
        },
        {
            'service_name': 'Lighting Setup',
            'basic_rate': 1500.00,
            'extra_hourly_rate': 300.00,
            'is_mandatory': False
        },
        {
            'service_name': 'Security Services',
            'basic_rate': 1000.00,
            'extra_hourly_rate': 200.00,
            'is_mandatory': True
        },
        {
            'service_name': 'Cleaning Service',
            'basic_rate': 800.00,
            'extra_hourly_rate': 100.00,
            'is_mandatory': True
        },
        {
            'service_name': 'Catering Service',
            'basic_rate': 3000.00,
            'extra_hourly_rate': 500.00,
            'is_mandatory': False
        },
        {
            'service_name': 'Photography/Videography',
            'basic_rate': 2500.00,
            'extra_hourly_rate': 400.00,
            'is_mandatory': False
        },
        {
            'service_name': 'Decoration & Flowers',
            'basic_rate': 2000.00,
            'extra_hourly_rate': 300.00,
            'is_mandatory': False
        },
        {
            'service_name': 'Air Conditioning',
            'basic_rate': 500.00,
            'extra_hourly_rate': 100.00,
            'is_mandatory': False
        }
    ]
    
    for service_data in services_data:
        service, created = AdditionalService.objects.get_or_create(
            service_name=service_data['service_name'],
            defaults=service_data
        )
        if created:
            print(f"✅ Created service: {service.service_name}")
    
    # Add JTCC comprehensive information
    jtcc_info = {
        'official_name': 'Jaffna Thiruvalluvar Cultural Centre',
        'common_name': 'JTCC',
        'location': 'Jaffna, Sri Lanka',
        'inauguration_date': '2023-02-11',
        'inaugurated_by': 'President Ranil Wickremesinghe and other Indian and Sri Lankan dignitaries',
        'description': '''The Jaffna Thiruvalluvar Cultural Centre (JTCC) is a state-of-the-art cultural facility that serves as a bridge between Indian and Sri Lankan cultures. The centre was established to promote cultural exchange, education, and community development.

Key Features:
- Modern auditorium with 600-seat capacity
- Conference facilities for business and academic events
- Beautiful outdoor amphitheatre with pond view
- Digital library with modern technology
- Exhibition spaces for cultural displays
- Multiple meeting rooms and study areas
- Professional event management services
- Parking facilities for 200+ vehicles
- Wheelchair accessible throughout

The centre hosts various events including:
- Cultural performances and concerts
- Business conferences and seminars
- Educational workshops and training
- Art exhibitions and cultural displays
- Community events and celebrations
- Wedding receptions and ceremonies''',
        'facilities': 'Auditorium, Conference Hall, Amphitheatre, Digital Library, Exhibition Space, Meeting Rooms, Study Areas, Parking',
        'renaming_date': '2025-01-18',
        'renaming_announced_by': 'Indian Government',
        'renaming_occasion': 'Pongal Celebrations',
        'status': 'Active'
    }
    
    history, created = JTCCHistory.objects.get_or_create(
        history_id=1,
        defaults=jtcc_info
    )
    if created:
        print("✅ Created comprehensive JTCC information")
    
    # Add contact information
    contact_info = {
        'phone_number': '+94 21 222 1234',
        'email': 'info@jtcc.lk',
        'available_time': 'Monday to Friday, 9:00 AM - 5:00 PM'
    }
    
    contact, created = Contact.objects.get_or_create(
        id=1,
        defaults=contact_info
    )
    if created:
        print("✅ Created contact information")
    
    print("\n🎉 Detailed venue information added successfully!")
    print(f"   - Venues: {Venue.objects.count()}")
    print(f"   - Services: {AdditionalService.objects.count()}")
    print(f"   - Price Tiers: {PriceTier.objects.count()}")

if __name__ == "__main__":
    add_detailed_venue_data()
