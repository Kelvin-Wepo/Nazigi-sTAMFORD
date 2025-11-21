#!/usr/bin/env python3
"""
Test the complete opt-in registration flow
"""
import requests
import sys

# Test configuration
CALLBACK_URL = "http://localhost:5000/sms/callback"
TEST_PHONE = "+254799489045"

def send_test_sms(phone, message):
    """Simulate incoming SMS from AfricasTalking"""
    data = {
        'from': phone,
        'text': message,
        'to': '3854',
        'id': 'test-message-id',
        'date': '2025-11-20 10:00:00'
    }
    
    print(f"\n📱 Sending SMS: '{message}' from {phone}")
    print("-" * 60)
    
    try:
        response = requests.post(CALLBACK_URL, data=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🧪 TESTING OPT-IN REGISTRATION FLOW")
    print("=" * 60)
    
    # Step 1: Send STAMFORD to register
    print("\n📍 STEP 1: Initial Registration (send STAMFORD)")
    response1 = send_test_sms(TEST_PHONE, "STAMFORD")
    
    if not response1 or response1.status_code != 200:
        print("❌ Failed at Step 1")
        return
    
    input("\n⏸️  Check your phone for the opt-in message. Press Enter to continue...")
    
    # Step 2: Send YES to opt in
    print("\n📍 STEP 2: Opt-In Confirmation (send YES)")
    response2 = send_test_sms(TEST_PHONE, "YES")
    
    if not response2 or response2.status_code != 200:
        print("❌ Failed at Step 2")
        return
    
    input("\n⏸️  Check your phone for the confirmation message. Press Enter to continue...")
    
    print("\n✅ Opt-in flow test completed!")
    print("=" * 60)
    print("\n📊 Verify registration:")
    print("   1. Check Flask logs for emoji indicators")
    print("   2. Check your phone for two SMS messages:")
    print("      - Welcome message with opt-in/opt-out options")
    print("      - Confirmation message after opting in")
    print("   3. Try sending a test conductor message to verify delivery")

if __name__ == "__main__":
    main()
