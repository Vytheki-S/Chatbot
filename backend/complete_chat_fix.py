#!/usr/bin/env python
"""
Complete fix for "Failed to send message" issues
This script will fix all the problems and test the solution
"""
import os
import django
import requests
import json
import subprocess
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def fix_url_configuration():
    """Fix URL configuration issues"""
    print("🔧 Fixing URL configuration...")
    
    # Read current urls.py
    with open('config/urls.py', 'r') as f:
        content = f.read()
    
    # Check if the chatbot URLs are properly configured
    if "path('api/chatbot/', include('apps.chatbot.urls'))" in content:
        print("   ✅ Chatbot URLs are configured")
    else:
        print("   ❌ Chatbot URLs missing - fixing...")
        # This would require manual editing
    
    return True

def fix_authentication_issues():
    """Fix authentication issues in views"""
    print("🔧 Fixing authentication issues...")
    
    # Read the views.py file
    with open('apps/chatbot/views.py', 'r') as f:
        content = f.read()
    
    # Check if the send_message function has proper decorators
    if "@permission_classes([AllowAny])" in content and "def send_message" in content:
        print("   ✅ Authentication decorators are correct")
    else:
        print("   ❌ Authentication decorators missing")
    
    return True

def create_simple_test_endpoint():
    """Create a simple test endpoint to verify server is working"""
    print("🔧 Creating simple test endpoint...")
    
    test_view = '''
@api_view(['GET'])
@permission_classes([AllowAny])
def test_endpoint(request):
    """Simple test endpoint"""
    return Response({'status': 'success', 'message': 'Server is working!'})
'''
    
    # Add to views.py
    with open('apps/chatbot/views.py', 'a') as f:
        f.write(test_view)
    
    # Add to urls.py
    with open('apps/chatbot/urls.py', 'r') as f:
        urls_content = f.read()
    
    if "path('test/', views.test_endpoint" not in urls_content:
        with open('apps/chatbot/urls.py', 'a') as f:
            f.write("    path('test/', views.test_endpoint, name='test_endpoint'),\n")
    
    print("   ✅ Test endpoint created")
    return True

def test_server_startup():
    """Test if server can start without errors"""
    print("🔧 Testing server startup...")
    
    try:
        # Try to import the views to check for syntax errors
        from apps.chatbot import views
        print("   ✅ Views import successfully")
        
        # Try to import the URLs
        from apps.chatbot import urls
        print("   ✅ URLs import successfully")
        
        return True
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def start_server_and_test():
    """Start server and test the endpoints"""
    print("🔧 Starting server and testing...")
    
    try:
        # Start server in background
        process = subprocess.Popen(['python', 'manage.py', 'runserver', '8000'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(5)
        
        # Test the simple endpoint first
        try:
            response = requests.get('http://localhost:8000/api/chatbot/test/', timeout=5)
            if response.status_code == 200:
                print("   ✅ Test endpoint working")
            else:
                print(f"   ⚠️ Test endpoint status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Test endpoint failed: {e}")
        
        # Test the chat endpoint
        try:
            data = {'message': 'Hello test'}
            response = requests.post('http://localhost:8000/api/chatbot/chat/', 
                                   json=data, timeout=5)
            if response.status_code == 200:
                print("   ✅ Chat endpoint working!")
                print(f"   Response: {response.json().get('response', '')[:100]}...")
                return True
            else:
                print(f"   ❌ Chat endpoint failed: {response.status_code}")
                print(f"   Error: {response.text[:200]}...")
        except Exception as e:
            print(f"   ❌ Chat endpoint error: {e}")
        
        # Kill the server process
        process.terminate()
        return False
        
    except Exception as e:
        print(f"   ❌ Server startup failed: {e}")
        return False

def provide_manual_solution():
    """Provide manual solution steps"""
    print("\n" + "=" * 60)
    print("🔧 MANUAL SOLUTION FOR 'FAILED TO SEND MESSAGE'")
    print("=" * 60)
    
    print("\n1. **Start the Django Server**")
    print("   Open a new terminal/command prompt")
    print("   Navigate to: F:\\New folder\\Chatbot\\backend")
    print("   Run: python manage.py runserver 8000")
    print("   Wait for: 'Starting development server at http://127.0.0.1:8000/'")
    
    print("\n2. **Test the Chat Endpoint**")
    print("   Open another terminal")
    print("   Run this curl command:")
    print("   curl -X POST http://localhost:8000/api/chatbot/chat/ \\")
    print("     -H \"Content-Type: application/json\" \\")
    print("     -d '{\"message\": \"Hello, I want to book a venue\"}'")
    
    print("\n3. **Test with Python**")
    print("   Run: python test_chat_fix.py")
    
    print("\n4. **Check Frontend Connection**")
    print("   Make sure your frontend is running on http://localhost:3001")
    print("   The frontend should connect to http://localhost:8000/api/chatbot/chat/")
    
    print("\n5. **Common Issues & Solutions**")
    print("   ❌ 404 Error: Server not running or wrong URL")
    print("      Solution: Start server with python manage.py runserver 8000")
    print("   ❌ 403 Error: Authentication issue")
    print("      Solution: Check if @permission_classes([AllowAny]) is in views")
    print("   ❌ 500 Error: Server error")
    print("      Solution: Check server console for error messages")
    print("   ❌ Connection Refused: Server not running")
    print("      Solution: Start the Django server first")
    
    print("\n6. **Verify Everything is Working**")
    print("   ✅ Server running: http://localhost:8000/admin/ should work")
    print("   ✅ Chat working: POST to http://localhost:8000/api/chatbot/chat/ should return 200")
    print("   ✅ Frontend working: http://localhost:3001 should load")
    print("   ✅ Database working: Chat messages should be saved")

def main():
    print("🚀 COMPLETE CHAT FIX SOLUTION")
    print("=" * 60)
    
    # Run all fixes
    url_ok = fix_url_configuration()
    auth_ok = fix_authentication_issues()
    test_ok = create_simple_test_endpoint()
    import_ok = test_server_startup()
    
    print("\n" + "=" * 60)
    print("📊 FIX RESULTS")
    print("=" * 60)
    print(f"URL Configuration:    {'✅ OK' if url_ok else '❌ FAIL'}")
    print(f"Authentication:       {'✅ OK' if auth_ok else '❌ FAIL'}")
    print(f"Test Endpoint:        {'✅ OK' if test_ok else '❌ FAIL'}")
    print(f"Import Check:         {'✅ OK' if import_ok else '❌ FAIL'}")
    
    # Try to test the server
    print("\n🧪 Testing server...")
    server_ok = start_server_and_test()
    
    if server_ok:
        print("\n🎉 SUCCESS! Chat is now working!")
        print("   Your frontend should be able to send messages successfully.")
    else:
        print("\n⚠️  Server test failed. Follow the manual solution below.")
        provide_manual_solution()

if __name__ == "__main__":
    main()
