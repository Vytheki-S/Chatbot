#!/usr/bin/env python
"""
Simple API test script
"""
import requests
import time

def test_api():
    print("Testing API endpoints...")
    
    # Wait a moment for server to start
    time.sleep(2)
    
    base_url = "http://localhost:8000"
    
    # Test endpoints
    endpoints = [
        "/",
        "/admin/",
        "/api/chatbot/health/",
        "/api/chatbot/venues/",
        "/api/chatbot/jtcc/info/",
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            print(f"\nTesting: {url}")
            response = requests.get(url, timeout=5)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {response.text[:100]}...")
            else:
                print(f"Error: {response.text[:200]}...")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_api()

