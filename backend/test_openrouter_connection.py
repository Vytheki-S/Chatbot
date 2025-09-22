#!/usr/bin/env python
"""
Test OpenRouter API connection and configuration
"""
import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from apps.chatbot.services import OpenRouterService

def test_openrouter_configuration():
    print("🔍 Testing OpenRouter Configuration")
    print("=" * 50)
    
    # Check environment variables
    api_key = os.getenv('OPENROUTER_API_KEY')
    print(f"Environment Variable OPENROUTER_API_KEY: {'✅ SET' if api_key else '❌ NOT SET'}")
    
    # Check Django settings
    django_api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
    print(f"Django Settings OPENROUTER_API_KEY: {'✅ SET' if django_api_key else '❌ NOT SET'}")
    
    django_api_url = getattr(settings, 'OPENROUTER_API_URL', None)
    print(f"Django Settings OPENROUTER_API_URL: {django_api_url}")
    
    return api_key is not None or django_api_key is not None

def test_openrouter_service():
    print("\n🤖 Testing OpenRouter Service")
    print("=" * 50)
    
    try:
        service = OpenRouterService()
        
        print(f"API Key configured: {'✅ YES' if service.api_key else '❌ NO'}")
        print(f"API URL: {service.api_url}")
        print(f"Model: {service.default_model}")
        print(f"Temperature: {service.temperature}")
        print(f"Max Tokens: {service.max_tokens}")
        
        if not service.api_key:
            print("\n⚠️  WARNING: No API key configured. Service will use fallback responses.")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing OpenRouterService: {str(e)}")
        return False

def test_openrouter_api_connection():
    print("\n🌐 Testing OpenRouter API Connection")
    print("=" * 50)
    
    try:
        service = OpenRouterService()
        
        if not service.api_key:
            print("❌ Cannot test API connection - No API key configured")
            return False
        
        # Test with a simple message
        test_message = "Hello, this is a test message"
        print(f"Testing with message: '{test_message}'")
        
        response = service.generate_response(test_message)
        
        if response:
            print(f"✅ API Connection Successful!")
            print(f"Response: {response[:200]}...")
            return True
        else:
            print("❌ API Connection Failed - No response received")
            return False
            
    except Exception as e:
        print(f"❌ API Connection Error: {str(e)}")
        return False

def test_fallback_responses():
    print("\n🔄 Testing Fallback Responses")
    print("=" * 50)
    
    try:
        service = OpenRouterService()
        
        # Test various queries
        test_queries = [
            "Hello, I want to book a venue",
            "What are your prices?",
            "Tell me about your venues",
            "How can I contact you?"
        ]
        
        for query in test_queries:
            print(f"\nTesting: '{query}'")
            response = service.generate_response(query)
            if response:
                print(f"✅ Response: {response[:100]}...")
            else:
                print("❌ No response")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback Response Error: {str(e)}")
        return False

def test_database_integration():
    print("\n🗄️ Testing Database Integration")
    print("=" * 50)
    
    try:
        from apps.chatbot.models import Venue, PriceTier, AdditionalService
        
        # Check if we have data
        venues_count = Venue.objects.count()
        price_tiers_count = PriceTier.objects.count()
        services_count = AdditionalService.objects.count()
        
        print(f"Venues in database: {venues_count}")
        print(f"Price tiers in database: {price_tiers_count}")
        print(f"Additional services in database: {services_count}")
        
        if venues_count > 0:
            print("✅ Database has venue data")
            
            # Test database context generation
            service = OpenRouterService()
            context = service._get_database_context("Tell me about your venues")
            print(f"Database context generated: {len(context)} characters")
            print(f"Context preview: {context[:200]}...")
            return True
        else:
            print("❌ No venue data in database")
            return False
            
    except Exception as e:
        print(f"❌ Database Integration Error: {str(e)}")
        return False

def main():
    print("🚀 OpenRouter Connection Test Suite")
    print("=" * 60)
    
    # Run all tests
    config_ok = test_openrouter_configuration()
    service_ok = test_openrouter_service()
    api_ok = test_openrouter_api_connection()
    fallback_ok = test_fallback_responses()
    db_ok = test_database_integration()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Configuration: {'✅ OK' if config_ok else '❌ FAIL'}")
    print(f"Service Init: {'✅ OK' if service_ok else '❌ FAIL'}")
    print(f"API Connection: {'✅ OK' if api_ok else '❌ FAIL'}")
    print(f"Fallback Responses: {'✅ OK' if fallback_ok else '❌ FAIL'}")
    print(f"Database Integration: {'✅ OK' if db_ok else '❌ FAIL'}")
    
    print("\n🎯 OVERALL STATUS:")
    if api_ok:
        print("🏆 EXCELLENT! OpenRouter API is connected and working!")
    elif fallback_ok and db_ok:
        print("✅ GOOD! Using fallback responses with database integration.")
        print("💡 To enable OpenRouter API, set the OPENROUTER_API_KEY environment variable.")
    else:
        print("⚠️  ISSUES DETECTED! Check the errors above.")
    
    print("\n💡 To set up OpenRouter API key:")
    print("1. Get an API key from https://openrouter.ai/")
    print("2. Set environment variable: set OPENROUTER_API_KEY=your_key_here")
    print("3. Or add to your .env file: OPENROUTER_API_KEY=your_key_here")

if __name__ == "__main__":
    main()
