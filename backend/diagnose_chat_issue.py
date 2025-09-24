#!/usr/bin/env python
"""
Diagnose and fix "Failed to send message" issues
"""
import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver
from apps.chatbot.views import send_message
from apps.chatbot.models import ChatSession, ChatMessage

def diagnose_server_status():
    print("🔍 DIAGNOSING CHAT MESSAGE ISSUES")
    print("=" * 50)
    
    # 1. Check if server is running
    print("\n1. Checking server status...")
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        print(f"   ✅ Server is running (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("   ❌ Server is NOT running")
        print("   💡 Solution: Run 'python manage.py runserver 8000'")
        return False
    except Exception as e:
        print(f"   ⚠️  Server issue: {str(e)}")
        return False
    
    return True

def diagnose_url_routing():
    print("\n2. Checking URL routing...")
    try:
        resolver = get_resolver()
        print("   📋 Available URL patterns:")
        
        # Check main URLs
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                print(f"   - {pattern.pattern} (includes sub-patterns)")
                for sub_pattern in pattern.url_patterns:
                    if 'chatbot' in str(sub_pattern.pattern):
                        print(f"     └─ {sub_pattern.pattern} -> {sub_pattern.name}")
            else:
                if 'chatbot' in str(pattern.pattern):
                    print(f"   - {pattern.pattern} -> {pattern.name}")
        
        return True
    except Exception as e:
        print(f"   ❌ URL routing error: {str(e)}")
        return False

def test_api_endpoints():
    print("\n3. Testing API endpoints...")
    
    endpoints = [
        ("Root API", "http://localhost:8000/api/"),
        ("Chatbot Health", "http://localhost:8000/api/chatbot/health/"),
        ("Chat Endpoint", "http://localhost:8000/api/chatbot/chat/"),
        ("Venues", "http://localhost:8000/api/chatbot/venues/"),
    ]
    
    working_endpoints = 0
    
    for name, url in endpoints:
        try:
            if "chat/" in url:
                # Test POST request for chat
                response = requests.post(url, json={'message': 'test'}, timeout=5)
            else:
                # Test GET request for others
                response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"   ✅ {name}: Working")
                working_endpoints += 1
            else:
                print(f"   ⚠️  {name}: Status {response.status_code}")
                if response.status_code == 404:
                    print(f"      URL not found: {url}")
        except Exception as e:
            print(f"   ❌ {name}: Error - {str(e)}")
    
    print(f"\n   📊 Working endpoints: {working_endpoints}/{len(endpoints)}")
    return working_endpoints > 0

def test_database_connection():
    print("\n4. Testing database connection...")
    try:
        # Test creating a session
        session = ChatSession.objects.create(user_id='test_user')
        print(f"   ✅ Database connection working")
        print(f"   ✅ Created test session: {session.id}")
        
        # Test creating a message
        message = ChatMessage.objects.create(
            session=session,
            sender_type='user',
            content='Test message'
        )
        print(f"   ✅ Created test message: {message.id}")
        
        # Clean up
        message.delete()
        session.delete()
        print("   ✅ Test data cleaned up")
        
        return True
    except Exception as e:
        print(f"   ❌ Database error: {str(e)}")
        return False

def test_chat_function_directly():
    print("\n5. Testing chat function directly...")
    try:
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        
        # Create a test user
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={'email': 'test@example.com'}
        )
        
        # Create a mock request
        factory = RequestFactory()
        request = factory.post('/api/chatbot/chat/', 
                              data=json.dumps({'message': 'Hello test'}),
                              content_type='application/json')
        request.user = user
        
        # Test the function
        from apps.chatbot.views import send_message
        response = send_message(request)
        
        print(f"   ✅ Chat function works directly")
        print(f"   ✅ Response status: {response.status_code}")
        return True
        
    except Exception as e:
        print(f"   ❌ Chat function error: {str(e)}")
        return False

def check_cors_settings():
    print("\n6. Checking CORS settings...")
    try:
        from django.conf import settings
        
        cors_installed = 'corsheaders' in settings.INSTALLED_APPS
        print(f"   CORS Headers installed: {'✅ Yes' if cors_installed else '❌ No'}")
        
        if cors_installed:
            cors_allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
            cors_allow_all = getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', False)
            print(f"   CORS Allow All Origins: {'✅ Yes' if cors_allow_all else '❌ No'}")
            print(f"   CORS Allowed Origins: {cors_allowed_origins}")
        
        return True
    except Exception as e:
        print(f"   ❌ CORS check error: {str(e)}")
        return False

def provide_solutions():
    print("\n" + "=" * 50)
    print("🔧 SOLUTIONS FOR 'FAILED TO SEND MESSAGE'")
    print("=" * 50)
    
    print("\n1. **Server Not Running**")
    print("   Solution: Start the Django server")
    print("   Command: python manage.py runserver 8000")
    
    print("\n2. **URL Routing Issues**")
    print("   Solution: Check URL configuration")
    print("   - Verify config/urls.py includes chatbot URLs")
    print("   - Verify apps/chatbot/urls.py has chat endpoint")
    
    print("\n3. **Database Issues**")
    print("   Solution: Run migrations")
    print("   Commands:")
    print("   - python manage.py makemigrations")
    print("   - python manage.py migrate")
    
    print("\n4. **CORS Issues (Frontend)**")
    print("   Solution: Configure CORS for frontend")
    print("   - Add frontend URL to CORS_ALLOWED_ORIGINS")
    print("   - Or set CORS_ALLOW_ALL_ORIGINS = True (development only)")
    
    print("\n5. **Authentication Issues**")
    print("   Solution: Check user authentication")
    print("   - Ensure user is logged in")
    print("   - Check authentication middleware")
    
    print("\n6. **OpenRouter API Issues**")
    print("   Solution: Check API configuration")
    print("   - Verify OPENROUTER_API_KEY is set")
    print("   - Check API endpoint accessibility")

def main():
    print("🚀 CHAT MESSAGE DIAGNOSTIC TOOL")
    print("=" * 50)
    
    # Run all diagnostics
    server_ok = diagnose_server_status()
    if not server_ok:
        provide_solutions()
        return
    
    url_ok = diagnose_url_routing()
    api_ok = test_api_endpoints()
    db_ok = test_database_connection()
    chat_ok = test_chat_function_directly()
    cors_ok = check_cors_settings()
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC RESULTS")
    print("=" * 50)
    print(f"Server Running:     {'✅ OK' if server_ok else '❌ FAIL'}")
    print(f"URL Routing:        {'✅ OK' if url_ok else '❌ FAIL'}")
    print(f"API Endpoints:      {'✅ OK' if api_ok else '❌ FAIL'}")
    print(f"Database:           {'✅ OK' if db_ok else '❌ FAIL'}")
    print(f"Chat Function:      {'✅ OK' if chat_ok else '❌ FAIL'}")
    print(f"CORS Settings:      {'✅ OK' if cors_ok else '❌ FAIL'}")
    
    if all([server_ok, url_ok, api_ok, db_ok, chat_ok, cors_ok]):
        print("\n🎉 ALL SYSTEMS WORKING! Chat should be functional.")
    else:
        print("\n⚠️  ISSUES DETECTED! See solutions below.")
        provide_solutions()

if __name__ == "__main__":
    main()
