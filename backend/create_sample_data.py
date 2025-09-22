#!/usr/bin/env python
"""
Create sample data for testing
"""
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.chatbot.models import (
    Venue, VenueImage, PriceTier, Applicant, Booking, BookingSlot,
    AdditionalService, JTCCHistory, JTCCFunder, JTCCFacility, JTCCMilestone, Contact
)
from django.contrib.auth.models import User

def create_sample_data():
    print("Creating sample data...")
    
    # Create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('password123')
        user.save()
        print("✅ Created test user")
    
    # Create venues
    venues_data = [
        {
            'venue_name': 'Main Auditorium',
            'capacity': 600,
            'description': 'Large auditorium with modern sound system and lighting',
            'status': 'active'
        },
        {
            'venue_name': 'Conference Hall',
            'capacity': 100,
            'description': 'Medium-sized conference room with projection facilities',
            'status': 'active'
        },
        {
            'venue_name': 'Pond Amphitheatre',
            'capacity': 300,
            'description': 'Open-air amphitheatre with natural ambiance',
            'status': 'active'
        }
    ]
    
    for venue_data in venues_data:
        venue, created = Venue.objects.get_or_create(
            venue_name=venue_data['venue_name'],
            defaults=venue_data
        )
        if created:
            print(f"✅ Created venue: {venue.venue_name}")
            
            # Create price tiers for each venue
            price_tiers = [
                {'duration': 2, 'price': 5000.00},
                {'duration': 4, 'price': 9000.00},
                {'duration': 6, 'price': 12000.00},
                {'duration': 8, 'price': 15000.00},
            ]
            
            for tier_data in price_tiers:
                PriceTier.objects.create(
                    venue=venue,
                    duration=tier_data['duration'],
                    price=tier_data['price']
                )
    
    # Create additional services
    services_data = [
        {'service_name': 'Sound System', 'basic_rate': 2000.00, 'extra_hourly_rate': 500.00, 'is_mandatory': False},
        {'service_name': 'Lighting Setup', 'basic_rate': 1500.00, 'extra_hourly_rate': 300.00, 'is_mandatory': False},
        {'service_name': 'Security', 'basic_rate': 1000.00, 'extra_hourly_rate': 200.00, 'is_mandatory': True},
        {'service_name': 'Cleaning Service', 'basic_rate': 800.00, 'extra_hourly_rate': 100.00, 'is_mandatory': True},
    ]
    
    for service_data in services_data:
        service, created = AdditionalService.objects.get_or_create(
            service_name=service_data['service_name'],
            defaults=service_data
        )
        if created:
            print(f"✅ Created service: {service.service_name}")
    
    # Create JTCC history
    history, created = JTCCHistory.objects.get_or_create(
        history_id=1,
        defaults={
            'official_name': 'Jaffna Thiruvalluvar Cultural Centre',
            'common_name': 'JTCC',
            'location': 'Jaffna, Sri Lanka',
            'inauguration_date': '2023-02-11',
            'inaugurated_by': 'President Ranil Wickremesinghe and other Indian and Sri Lankan dignitaries',
            'description': 'Officially named as Jaffna Thiruvalluvar Cultural Centre, is a cultural centre in Jaffna, Sri Lanka. It was opened on 11 February 2023 by President Ranil Wickremesinghe and other Indian and Sri Lankan dignitaries. The centre includes an auditorium, conference hall, amphitheatre and a digital library.',
            'facilities': 'Auditorium, Conference Hall, Amphitheatre, Digital Library, Exhibition Space, Open Areas',
            'renaming_date': '2025-01-18',
            'renaming_announced_by': 'Indian Government',
            'renaming_occasion': 'Pongal Celebrations',
            'status': 'Active'
        }
    )
    if created:
        print("✅ Created JTCC history")
    
    # Create JTCC funders
    funders_data = [
        {'funder_name': 'Government of Sri Lanka', 'funder_type': 'Government', 'country': 'Sri Lanka'},
        {'funder_name': 'High Commissioner of India to Sri Lanka', 'funder_type': 'Organization', 'country': 'India'},
        {'funder_name': 'Minister of Buddhasasana', 'funder_type': 'Government', 'country': 'Sri Lanka'},
    ]
    
    for funder_data in funders_data:
        funder, created = JTCCFunder.objects.get_or_create(
            funder_name=funder_data['funder_name'],
            defaults=funder_data
        )
        if created:
            print(f"✅ Created funder: {funder.funder_name}")
    
    # Create JTCC facilities
    facilities_data = [
        {'facility_name': 'Main Auditorium', 'facility_type': 'Auditorium', 'capacity': 600, 'is_available': True},
        {'facility_name': 'Conference Hall', 'facility_type': 'Conference Hall', 'capacity': 100, 'is_available': True},
        {'facility_name': 'Pond Amphitheatre', 'facility_type': 'Amphitheatre', 'capacity': 300, 'is_available': True},
        {'facility_name': 'Digital Library', 'facility_type': 'Library', 'capacity': 50, 'is_available': True},
    ]
    
    for facility_data in facilities_data:
        facility, created = JTCCFacility.objects.get_or_create(
            facility_name=facility_data['facility_name'],
            defaults=facility_data
        )
        if created:
            print(f"✅ Created facility: {facility.facility_name}")
    
    # Create contact information
    contact, created = Contact.objects.get_or_create(
        id=1,
        defaults={
            'phone_number': '+94 21 222 1234',
            'email': 'info@jtcc.lk',
            'available_time': 'Monday to Friday, 9:00 AM - 5:00 PM'
        }
    )
    if created:
        print("✅ Created contact information")
    
    print("\n🎉 Sample data creation completed!")
    print(f"   - Venues: {Venue.objects.count()}")
    print(f"   - Services: {AdditionalService.objects.count()}")
    print(f"   - Facilities: {JTCCFacility.objects.count()}")
    print(f"   - Funders: {JTCCFunder.objects.count()}")

if __name__ == "__main__":
    create_sample_data()

