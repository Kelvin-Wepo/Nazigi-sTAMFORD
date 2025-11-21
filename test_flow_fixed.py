#!/usr/bin/env python3
"""
Test SMS flow end-to-end with current configuration
"""
import requests
import time
import json

NGROK_URL = "https://044ad3cea41b.ngrok-free.app"
LOCAL_URL = "http://localhost:5000"

def test_sms_flow():
    print("🧪 TESTING SMS FLOW WITH NEW CONFIGURATION")
    print("="*70)
    print("Configuration: Sender ID removed (blank)")
    print("="*70)
    
    # Test with the phone numbers from your AT logs
    test_numbers = [
        "+254799489045",
        "+254711082300"
    ]
    
    for phone in test_numbers:
        print(f"\n📱 Testing with: {phone}")
        print("-"*70)
        
        # Simulate incoming SMS
        print("1️⃣  Simulating incoming SMS: 'STAMFORD'")
        response = requests.post(
            f"{LOCAL_URL}/sms/callback",
            data={
                'from': phone,
                'text': 'STAMFORD',
                'to': '3854',
                'date': '2025-11-20 10:00:00',
                'id': f'test_{int(time.time())}',
                'linkId': f'link_{int(time.time())}'
            }
        )
        
        print(f"   Response Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Callback processed successfully")
            print("   📋 Check Flask logs for:")
            print("      - 🆔 Sender ID: (should be blank/None)")
            print("      - ✉️ Sending without sender ID")
            print("      - ✅ SMS successfully sent")
        else:
            print(f"   ❌ Error: {response.status_code}")
        
        time.sleep(2)
    
    print("\n" + "="*70)
    print("🔍 WHAT TO CHECK NOW:")
    print("="*70)
    print("""
1. Check Flask logs (flask_output.log or terminal):
   Look for these indicators:
   ✅ 🆔 Sender ID: None  (or blank)
   ✅ ✉️ Sending without sender ID
   ✅ 📨 AfricasTalking Response with StatusCode 100 or 101
   ✅ ✅ SMS successfully sent

2. Check AfricasTalking Dashboard OUTGOING logs:
   Go to: https://account.africastalking.com/sms/logs
   Switch to "OUTGOING" or "SENT" tab
   Search for: +254799489045 or +254711082300
   
   Look for messages sent in the last few minutes with text:
   "Welcome to Nazigi Stamford Bus Service..."
   
   Check the STATUS column:
   ✅ "Delivered" or "Sent" = GOOD
   ❌ "Failed" or "Rejected" = Still an issue

3. Check your actual phone:
   - Wait 1-2 minutes for message
   - Check spam/blocked messages
   - Try sending from different number

4. If AfricasTalking shows "Delivered" but you don't receive:
   - Phone/carrier issue
   - Try different phone number
   - Check phone message center settings
   - Contact your mobile carrier

5. If no OUTGOING messages appear in AT:
   - Callback URL might be wrong
   - Check ngrok is running: https://044ad3cea41b.ngrok-free.app
   - Verify callback in AT dashboard
    """)

if __name__ == "__main__":
    test_sms_flow()
