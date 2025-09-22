#!/usr/bin/env python
"""
Test script to check all connections:
1. Database connection
2. OpenRouter API connection
3. Frontend API endpoints
"""

import os
import sys
import django
import requests
from dotenv import load_dotenv

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.chatbot.models import Venue, Booking, ChatbotMessage
from apps.chatbot.services import OpenRouterService
from django.conf import settings

def test_database_connection():
    """Test database connection and basic queries"""
    print("🔍 Testing Database Connection...")
    try:
        # Test basic model queries
        venue_count = Venue.objects.count()
        booking_count = Booking.objects.count()
        message_count = ChatbotMessage.objects.count()
        
        print(f"✅ Database connection successful!")
        print(f"   - Venues: {venue_count}")
        print(f"   - Bookings: {booking_count}")
        print(f"   - Chat Messages: {message_count}")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def test_openrouter_api():
    """Test OpenRouter API connection"""
    print("\n🔍 Testing OpenRouter API Connection...")
    
    # Check if API key is set
    api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
    if not api_key:
        print("⚠️  OPENROUTER_API_KEY not set in environment variables")
        print("   Using fallback responses (no API calls)")
        return True
    
    try:
        service = OpenRouterService()
        response = service.generate_response("Hello, test message")
        
        if response and len(response) > 0:
            print("✅ OpenRouter API connection successful!")
            print(f"   Response preview: {response[:100]}...")
            return True
        else:
            print("❌ OpenRouter API returned empty response")
            return False
    except Exception as e:
        print(f"❌ OpenRouter API connection failed: {str(e)}")
        return False

def test_api_endpoints():
    """Test key API endpoints"""
    print("\n🔍 Testing API Endpoints...")
    
    base_url = "http://localhost:8000"
    endpoints = [
        "/api/chatbot/health/",
        "/api/chatbot/venues/",
        "/api/chatbot/jtcc/info/",
        "/api/chatbot/analytics/bookings/",
    ]
    
    success_count = 0
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint} - Status: {response.status_code}")
                success_count += 1
            else:
                print(f"⚠️  {endpoint} - Status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {endpoint} - Connection refused (server not running)")
        except Exception as e:
            print(f"❌ {endpoint} - Error: {str(e)}")
    
    print(f"\n   API Endpoints Status: {success_count}/{len(endpoints)} working")
    return success_count > 0

def test_frontend_connection():
    """Test if frontend can connect to backend"""
    print("\n🔍 Testing Frontend-Backend Connection...")
    
    try:
        # Test CORS headers
        response = requests.options(
            "http://localhost:8000/api/chatbot/health/",
            headers={
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'GET',
            },
            timeout=5
        )
        
        if response.status_code in [200, 204]:
            print("✅ CORS configuration working")
            return True
        else:
            print(f"⚠️  CORS test returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend connection test failed: {str(e)}")
        return False

def main():
    """Run all connection tests"""
    print("🚀 EventAura Connection Test")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Run tests
    db_ok = test_database_connection()
    api_ok = test_openrouter_api()
    endpoints_ok = test_api_endpoints()
    frontend_ok = test_frontend_connection()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CONNECTION TEST SUMMARY")
    print("=" * 50)
    print(f"Database:        {'✅ OK' if db_ok else '❌ FAIL'}")
    print(f"OpenRouter API:  {'✅ OK' if api_ok else '❌ FAIL'}")
    print(f"API Endpoints:   {'✅ OK' if endpoints_ok else '❌ FAIL'}")
    print(f"Frontend CORS:   {'✅ OK' if frontend_ok else '❌ FAIL'}")
    
    all_ok = db_ok and api_ok and endpoints_ok and frontend_ok
    print(f"\nOverall Status:  {'✅ ALL SYSTEMS GO!' if all_ok else '⚠️  SOME ISSUES DETECTED'}")
    
    if not all_ok:
        print("\n🔧 TROUBLESHOOTING TIPS:")
        if not db_ok:
            print("   - Check MySQL server is running")
            print("   - Verify database credentials in settings.py")
        if not api_ok:
            print("   - Set OPENROUTER_API_KEY in .env file")
            print("   - Check internet connection")
        if not endpoints_ok:
            print("   - Start Django server: python manage.py runserver")
            print("   - Check if port 8000 is available")
        if not frontend_ok:
            print("   - Verify CORS settings in settings.py")
            print("   - Check frontend is running on port 3000")

if __name__ == "__main__":
    main()

