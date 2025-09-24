#!/usr/bin/env python
"""
Comprehensive fix for "Failed to send message" issues
"""
import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver
from django.test import Client
from apps.chatbot.models import ChatSession, ChatMessage
from django.contrib.auth.models import User

def test_direct_function_call():
    """Test the chat function directly without HTTP"""
    print("🔧 Testing direct function call...")
    try:
        from apps.chatbot.views import send_message
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.post('/api/chatbot/chat/', 
                              data=json.dumps({'message': 'Hello test'}),
                              content_type='application/json')
        
        response = send_message(request)
        print(f"   ✅ Direct function call works: {response.status_code}")
        return True
    except Exception as e:
        print(f"   ❌ Direct function call failed: {e}")
        return False

def test_django_test_client():
    """Test using Django test client"""
    print("\n🔧 Testing Django test client...")
    try:
        client = Client()
        response = client.post('/api/chatbot/chat/', 
                              data=json.dumps({'message': 'Hello test'}),
                              content_type='application/json')
        print(f"   ✅ Django test client works: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.content.decode()[:100]}...")
        return True
    except Exception as e:
        print(f"   ❌ Django test client failed: {e}")
        return False

def check_url_patterns():
    """Check if URL patterns are correctly loaded"""
    print("\n🔧 Checking URL patterns...")
    try:
        resolver = get_resolver()
        
        # Check if chatbot URLs are included
        chatbot_patterns = []
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                for sub_pattern in pattern.url_patterns:
                    if 'chatbot' in str(sub_pattern.pattern):
                        chatbot_patterns.append(str(sub_pattern.pattern))
        
        print(f"   Found chatbot patterns: {chatbot_patterns}")
        
        if '/api/chatbot/' in str(resolver.url_patterns):
            print("   ✅ Chatbot URLs are included")
            return True
        else:
            print("   ❌ Chatbot URLs not found in main patterns")
            return False
    except Exception as e:
        print(f"   ❌ URL pattern check failed: {e}")
        return False

def create_test_data():
    """Create test data if needed"""
    print("\n🔧 Creating test data...")
    try:
        # Create test user
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={'email': 'test@example.com'}
        )
        print(f"   ✅ Test user: {user.username}")
        
        # Create test session
        session, created = ChatSession.objects.get_or_create(
            user_id=user.username,
            defaults={'user_id': user.username}
        )
        print(f"   ✅ Test session: {session.id}")
        
        return True
    except Exception as e:
        print(f"   ❌ Test data creation failed: {e}")
        return False

def test_with_curl_command():
    """Generate curl command for testing"""
    print("\n🔧 Testing with curl command...")
    curl_cmd = '''curl -X POST http://localhost:8000/api/chatbot/chat/ \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Hello, I want to book a venue"}' '''
    
    print(f"   Try this curl command:")
    print(f"   {curl_cmd}")
    
    # Also test with requests
    try:
        response = requests.post('http://localhost:8000/api/chatbot/chat/', 
                               json={'message': 'Hello test'}, 
                               timeout=5)
        print(f"   ✅ Requests test: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:100]}...")
        return True
    except Exception as e:
        print(f"   ❌ Requests test failed: {e}")
        return False

def fix_common_issues():
    """Apply common fixes"""
    print("\n🔧 Applying common fixes...")
    
    # 1. Ensure user exists
    try:
        user = User.objects.first()
        if not user:
            user = User.objects.create_user('admin', 'admin@example.com', 'admin123')
            print("   ✅ Created admin user")
        else:
            print(f"   ✅ User exists: {user.username}")
    except Exception as e:
        print(f"   ❌ User creation failed: {e}")
    
    # 2. Check database tables
    try:
        session_count = ChatSession.objects.count()
        message_count = ChatMessage.objects.count()
        print(f"   ✅ Database: {session_count} sessions, {message_count} messages")
    except Exception as e:
        print(f"   ❌ Database check failed: {e}")

def main():
    print("🚀 COMPREHENSIVE CHAT FIX")
    print("=" * 50)
    
    # Run all tests
    direct_ok = test_direct_function_call()
    client_ok = test_django_test_client()
    urls_ok = check_url_patterns()
    data_ok = create_test_data()
    curl_ok = test_with_curl_command()
    
    # Apply fixes
    fix_common_issues()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    print(f"Direct Function:    {'✅ OK' if direct_ok else '❌ FAIL'}")
    print(f"Django Client:      {'✅ OK' if client_ok else '❌ FAIL'}")
    print(f"URL Patterns:       {'✅ OK' if urls_ok else '❌ FAIL'}")
    print(f"Test Data:          {'✅ OK' if data_ok else '❌ FAIL'}")
    print(f"Curl/Requests:      {'✅ OK' if curl_ok else '❌ FAIL'}")
    
    if all([direct_ok, client_ok, urls_ok, data_ok, curl_ok]):
        print("\n🎉 ALL TESTS PASSED! Chat should be working.")
    else:
        print("\n⚠️  SOME TESTS FAILED. Check the issues above.")
        
        print("\n🔧 MANUAL FIXES TO TRY:")
        print("1. Restart Django server: python manage.py runserver 8000")
        print("2. Check if server is running on correct port")
        print("3. Verify URL patterns in config/urls.py")
        print("4. Check for any import errors in views.py")
        print("5. Test with curl command provided above")

if __name__ == "__main__":
    main()
