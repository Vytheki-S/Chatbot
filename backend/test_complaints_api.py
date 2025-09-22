#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_complaints_api():
    base_url = "http://127.0.0.1:8000"
    
    print("Testing Complaints API...")
    print("=" * 50)
    
    # Test 1: Get complaints (should return empty list initially)
    print("\n1. Testing GET /api/complaints/")
    try:
        response = requests.get(f"{base_url}/api/complaints/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Create a complaint
    print("\n2. Testing POST /api/complaints/create/")
    try:
        complaint_data = {
            "username": "test_user",
            "email": "test@example.com",
            "title": "Test Complaint",
            "description": "This is a test complaint",
            "complaint_category": "Technical"
        }
        response = requests.post(f"{base_url}/api/complaints/create/", json=complaint_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"Created Complaint: {json.dumps(data, indent=2)}")
            complaint_id = data['id']
        else:
            print(f"Error: {response.text}")
            complaint_id = None
    except Exception as e:
        print(f"Error: {e}")
        complaint_id = None
    
    # Test 3: Get complaints again (should now have one)
    print("\n3. Testing GET /api/complaints/ (after creation)")
    try:
        response = requests.get(f"{base_url}/api/complaints/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Create a reply (if we have a complaint)
    if complaint_id:
        print(f"\n4. Testing POST /api/replies/create/ for complaint {complaint_id}")
        try:
            reply_data = {
                "complaint_id": complaint_id,
                "message": "This is a test reply",
                "reply_type": "Admin",
                "user_name": "admin_user",
                "user_email": "admin@example.com"
            }
            response = requests.post(f"{base_url}/api/replies/create/", json=reply_data)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 201:
                data = response.json()
                print(f"Created Reply: {json.dumps(data, indent=2)}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Test 5: Get replies
    print("\n5. Testing GET /api/replies/")
    try:
        response = requests.get(f"{base_url}/api/replies/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 6: Get attachments
    print("\n6. Testing GET /api/attachments/")
    try:
        response = requests.get(f"{base_url}/api/attachments/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_complaints_api()
