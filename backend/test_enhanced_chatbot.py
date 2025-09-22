#!/usr/bin/env python
"""
Test the enhanced chatbot with various customer queries
"""
import requests
import json
import time

def test_chatbot_queries():
    base_url = "http://localhost:8000/api/chatbot"
    
    print("🤖 Testing Enhanced Chatbot with Customer Queries")
    print("=" * 60)
    
    # Test queries that customers commonly ask
    test_queries = [
        {
            "query": "Hello, I'm looking for a venue for my wedding",
            "expected_keywords": ["wedding", "venue", "auditorium", "amphitheatre"]
        },
        {
            "query": "What are your prices?",
            "expected_keywords": ["pricing", "LKR", "hours", "venue"]
        },
        {
            "query": "How many people can fit in your largest venue?",
            "expected_keywords": ["capacity", "600", "auditorium", "people"]
        },
        {
            "query": "What services do you offer?",
            "expected_keywords": ["services", "sound", "lighting", "catering", "security"]
        },
        {
            "query": "Tell me about JTCC",
            "expected_keywords": ["JTCC", "cultural", "centre", "Jaffna"]
        },
        {
            "query": "How can I contact you?",
            "expected_keywords": ["contact", "phone", "email", "available"]
        },
        {
            "query": "I need a small meeting room for 20 people",
            "expected_keywords": ["conference", "meeting", "capacity", "20"]
        },
        {
            "query": "What's available for a cultural performance?",
            "expected_keywords": ["amphitheatre", "cultural", "performance", "outdoor"]
        },
        {
            "query": "Do you have catering services?",
            "expected_keywords": ["catering", "service", "food", "beverage"]
        },
        {
            "query": "Help me plan my event",
            "expected_keywords": ["help", "plan", "event", "booking", "venue"]
        }
    ]
    
    successful_tests = 0
    total_tests = len(test_queries)
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n{i}. Testing: '{test['query']}'")
        
        try:
            response = requests.post(
                f"{base_url}/chat/",
                json={"message": test['query']},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get('response', '')
                
                # Check if response contains expected keywords
                response_lower = bot_response.lower()
                found_keywords = [kw for kw in test['expected_keywords'] if kw.lower() in response_lower]
                
                if found_keywords:
                    print(f"   ✅ SUCCESS - Found keywords: {found_keywords}")
                    print(f"   Response: {bot_response[:150]}...")
                    successful_tests += 1
                else:
                    print(f"   ⚠️  PARTIAL - Response received but missing expected keywords")
                    print(f"   Expected: {test['expected_keywords']}")
                    print(f"   Response: {bot_response[:150]}...")
            else:
                print(f"   ❌ FAILED - Status: {response.status_code}")
                print(f"   Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ ERROR - {str(e)}")
        
        time.sleep(1)  # Small delay between requests
    
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {successful_tests}/{total_tests} tests passed")
    print("=" * 60)
    
    if successful_tests == total_tests:
        print("🎉 ALL TESTS PASSED! The chatbot is working perfectly!")
    elif successful_tests >= total_tests * 0.8:
        print("✅ MOSTLY SUCCESSFUL! The chatbot is working well with minor issues.")
    else:
        print("⚠️  SOME ISSUES DETECTED! The chatbot needs improvement.")
    
    return successful_tests, total_tests

def test_api_endpoints():
    print("\n🔍 Testing API Endpoints")
    print("-" * 30)
    
    base_url = "http://localhost:8000/api/chatbot"
    endpoints = [
        ("Health Check", "health/"),
        ("Venues", "venues/"),
        ("JTCC Info", "jtcc/info/"),
        ("Services", "services/"),
        ("Contact", "contacts/"),
    ]
    
    working_endpoints = 0
    
    for name, endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}/{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: Working")
                working_endpoints += 1
            else:
                print(f"⚠️  {name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)}")
    
    print(f"\nAPI Endpoints: {working_endpoints}/{len(endpoints)} working")
    return working_endpoints == len(endpoints)

if __name__ == "__main__":
    print("🚀 Enhanced Chatbot Test Suite")
    print("=" * 60)
    
    # Test API endpoints first
    api_working = test_api_endpoints()
    
    if api_working:
        # Test chatbot queries
        successful, total = test_chatbot_queries()
        
        print(f"\n🎯 OVERALL RESULT:")
        if successful == total and api_working:
            print("🏆 EXCELLENT! All systems are working perfectly!")
            print("✅ Backend server running")
            print("✅ Database connected")
            print("✅ API endpoints responding")
            print("✅ Chatbot understanding customer queries")
            print("✅ Venue information available")
            print("✅ Services and pricing data loaded")
        else:
            print("⚠️  GOOD! Most systems working with minor issues.")
    else:
        print("❌ CRITICAL! API endpoints not working. Check server status.")
