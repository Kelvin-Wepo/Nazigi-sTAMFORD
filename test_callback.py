#!/usr/bin/env python3
"""
Test script to verify SMS callback and response flow
"""
import requests
import time

# Test configuration
NGROK_URL = "https://044ad3cea41b.ngrok-free.app"
LOCAL_URL = "http://localhost:5000"
TEST_PHONE = "+254711082300"

def test_callback(base_url, phone, message):
    """Test SMS callback endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {base_url}")
    print(f"Phone: {phone}")
    print(f"Message: {message}")
    print('='*60)
    
    response = requests.post(
        f"{base_url}/sms/callback",
        data={
            'from': phone,
            'text': message,
            'to': '3854',
            'date': '2025-11-20 10:00:00',
            'id': 'test123',
            'linkId': 'testLink'
        }
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response

def main():
    print("\n🧪 SMS Callback Test Suite")
    print("="*60)
    
    # Test 1: Local endpoint with STAMFORD
    print("\n✅ Test 1: Local endpoint - STAMFORD")
    test_callback(LOCAL_URL, TEST_PHONE, "STAMFORD")
    time.sleep(1)
    
    # Test 2: Local endpoint with YES
    print("\n✅ Test 2: Local endpoint - YES")
    test_callback(LOCAL_URL, TEST_PHONE, "YES")
    time.sleep(1)
    
    # Test 3: Ngrok endpoint with new phone
    print("\n✅ Test 3: Ngrok endpoint - STAMFORD")
    test_callback(NGROK_URL, "+254722999888", "STAMFORD")
    time.sleep(1)
    
    print("\n" + "="*60)
    print("✅ Tests completed!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Check Flask terminal for logs with emojis")
    print("2. Verify ngrok URL in AfricasTalking dashboard:")
    print(f"   {NGROK_URL}/sms/callback")
    print("3. Check if your phone number is whitelisted in AT sandbox")
    print("4. Verify AT_USERNAME and AT_API_KEY in .env")

if __name__ == "__main__":
    main()
