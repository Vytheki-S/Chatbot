#!/usr/bin/env python
"""
Test the chat fix
"""
import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_chat_endpoint():
    """Test the chat endpoint"""
    print("🧪 Testing Chat Endpoint Fix")
    print("=" * 40)
    
    # Test 1: Direct HTTP request
    print("\n1. Testing HTTP request...")
    try:
        data = {'message': 'Hello, I want to book a venue for my wedding'}
        response = requests.post('http://localhost:8000/api/chatbot/chat/', 
                               json=data, 
                               timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"   ✅ SUCCESS! Chat is working!")
            print(f"   Response: {response_data.get('response', '')[:200]}...")
            return True
        else:
            print(f"   ❌ FAILED! Status: {response.status_code}")
            print(f"   Error: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection failed - Server not running")
        print("   💡 Start server with: python manage.py runserver 8000")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def test_other_endpoints():
    """Test other endpoints to verify server is working"""
    print("\n2. Testing other endpoints...")
    
    endpoints = [
        ("Health", "http://localhost:8000/api/chatbot/health/"),
        ("Venues", "http://localhost:8000/api/chatbot/venues/"),
        ("Admin", "http://localhost:8000/admin/"),
    ]
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            status = "✅" if response.status_code == 200 else "⚠️"
            print(f"   {status} {name}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: Error - {str(e)}")

def main():
    print("🚀 CHAT FIX VERIFICATION")
    print("=" * 40)
    
    # Test chat endpoint
    chat_working = test_chat_endpoint()
    
    # Test other endpoints
    test_other_endpoints()
    
    print("\n" + "=" * 40)
    print("📊 FINAL RESULT")
    print("=" * 40)
    
    if chat_working:
        print("🎉 CHAT IS WORKING! ✅")
        print("\n💡 Your frontend should now be able to send messages successfully!")
        print("   The 'Failed to send message' error should be resolved.")
    else:
        print("❌ CHAT STILL NOT WORKING")
        print("\n🔧 Try these steps:")
        print("1. Make sure Django server is running: python manage.py runserver 8000")
        print("2. Check if there are any error messages in the server console")
        print("3. Verify the URL patterns are correct")
        print("4. Check database connection")

if __name__ == "__main__":
    main()
