#!/usr/bin/env python
"""
Start server and test chat functionality
"""
import os
import django
import requests
import time
import subprocess
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def start_server():
    """Start the Django server"""
    print("🚀 Starting Django Server...")
    print("=" * 50)
    
    try:
        # Start server in background
        process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', '8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Server started in background")
        print("⏳ Waiting for server to initialize...")
        time.sleep(5)
        
        return process
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def test_server_health():
    """Test if server is responding"""
    print("\n🔍 Testing Server Health...")
    
    try:
        response = requests.get('http://localhost:8000/admin/', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responding")
            return True
        else:
            print(f"⚠️ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not responding - connection refused")
        return False
    except Exception as e:
        print(f"❌ Server health check failed: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint"""
    print("\n💬 Testing Chat Endpoint...")
    
    try:
        data = {
            'message': 'Hello, I want to book a venue for my wedding'
        }
        
        response = requests.post(
            'http://localhost:8000/api/chatbot/chat/',
            json=data,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print("✅ Chat endpoint is working!")
            print(f"Response: {response_data.get('response', '')[:200]}...")
            return True
        else:
            print(f"❌ Chat endpoint failed with status: {response.status_code}")
            print(f"Error: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - server not running")
        return False
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False

def test_other_endpoints():
    """Test other important endpoints"""
    print("\n🔗 Testing Other Endpoints...")
    
    endpoints = [
        ("Health Check", "http://localhost:8000/api/chatbot/health/"),
        ("Venues", "http://localhost:8000/api/chatbot/venues/"),
        ("Test Endpoint", "http://localhost:8000/api/chatbot/test/"),
    ]
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            status = "✅" if response.status_code == 200 else "⚠️"
            print(f"   {status} {name}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: {e}")

def provide_solution():
    """Provide step-by-step solution"""
    print("\n" + "=" * 60)
    print("🔧 SOLUTION FOR 'FAILED TO SEND MESSAGE'")
    print("=" * 60)
    
    print("\n1. **CORRECT WAY TO START SERVER:**")
    print("   Open Command Prompt or PowerShell")
    print("   Navigate to: F:\\New folder\\Chatbot\\backend")
    print("   Run: python manage.py runserver 8000")
    print("   Wait for: 'Starting development server at http://127.0.0.1:8000/'")
    
    print("\n2. **TEST THE CHAT:**")
    print("   Open another terminal")
    print("   Run: python start_server_and_test.py")
    
    print("\n3. **FRONTEND CONNECTION:**")
    print("   Your frontend is running on: http://localhost:3001")
    print("   It should connect to: http://localhost:8000/api/chatbot/chat/")
    
    print("\n4. **COMMON MISTAKES:**")
    print("   ❌ Running from wrong directory (F:\\New folder\\Chatbot)")
    print("   ✅ Run from: F:\\New folder\\Chatbot\\backend")
    print("   ❌ Server not started")
    print("   ✅ Always start server first")
    print("   ❌ Wrong URL in frontend")
    print("   ✅ Use: http://localhost:8000/api/chatbot/chat/")

def main():
    print("🚀 CHAT SERVER STARTUP AND TEST")
    print("=" * 60)
    
    # Start server
    process = start_server()
    if not process:
        provide_solution()
        return
    
    # Test server health
    if not test_server_health():
        print("\n❌ Server is not running properly")
        provide_solution()
        return
    
    # Test chat endpoint
    chat_working = test_chat_endpoint()
    
    # Test other endpoints
    test_other_endpoints()
    
    # Results
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    
    if chat_working:
        print("🎉 SUCCESS! Chat is working!")
        print("✅ Your frontend should now be able to send messages")
        print("✅ The 'Failed to send message' error is resolved")
    else:
        print("❌ Chat is still not working")
        print("🔧 Follow the solution steps below")
        provide_solution()
    
    # Clean up
    if process:
        process.terminate()
        print("\n🛑 Server stopped")

if __name__ == "__main__":
    main()
