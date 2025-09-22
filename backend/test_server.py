#!/usr/bin/env python
"""
Test server endpoints
"""
import requests
import time

def test_server():
    base_url = "http://localhost:8000"
    
    print("Testing server endpoints...")
    
    # Test different URLs
    test_urls = [
        "/",
        "/admin/",
        "/api/",
        "/api/chatbot/",
        "/api/chatbot/health/",
        "/api/chatbot/venues/",
    ]
    
    for url in test_urls:
        try:
            full_url = f"{base_url}{url}"
            print(f"\nTesting: {full_url}")
            response = requests.get(full_url, timeout=5)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Success! Response: {response.text[:100]}...")
            else:
                print(f"Error response: {response.text[:200]}...")
        except Exception as e:
            print(f"Connection error: {str(e)}")

if __name__ == "__main__":
    test_server()
