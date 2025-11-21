#!/usr/bin/env python3
"""
Diagnostic script to check AfricasTalking SMS sending
"""
import os
from dotenv import load_dotenv
import africastalking

# Load environment variables
load_dotenv()

# Configuration
USERNAME = os.getenv('AT_USERNAME')
API_KEY = os.getenv('AT_API_KEY')
SENDER_ID = os.getenv('AT_SENDER_ID')
SHORTCODE = os.getenv('AT_SHORTCODE')

print("🔍 AfricasTalking Configuration Diagnostic")
print("="*60)
print(f"Username: {USERNAME}")
print(f"API Key: {API_KEY[:20]}..." if API_KEY else "API Key: NOT SET")
print(f"Sender ID: {SENDER_ID}")
print(f"Shortcode: {SHORTCODE}")
print("="*60)

# Initialize AfricasTalking
try:
    africastalking.initialize(USERNAME, API_KEY)
    sms = africastalking.SMS
    print("✅ AfricasTalking initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    exit(1)

# Test phone number (replace with your actual phone)
test_phone = input("\n📱 Enter your phone number (e.g., +254711082300): ").strip()
if not test_phone:
    test_phone = "+254711082300"

print(f"\n📤 Attempting to send test SMS to {test_phone}...")
print("="*60)

# Test 1: Send with sender ID
print("\n🧪 Test 1: Sending with Sender ID")
try:
    message = "Test message from Nazigi Bus Service. If you receive this, SMS is working! ✅"
    response = sms.send(message, [test_phone], SENDER_ID)
    print(f"✅ Response: {response}")
    
    # Parse response
    sms_data = response.get('SMSMessageData', {})
    recipients = sms_data.get('Recipients', [])
    
    if recipients:
        for recipient in recipients:
            status = recipient.get('status')
            status_code = recipient.get('statusCode')
            number = recipient.get('number')
            cost = recipient.get('cost', 'N/A')
            
            print(f"\n📊 Result for {number}:")
            print(f"   Status: {status}")
            print(f"   Status Code: {status_code}")
            print(f"   Cost: {cost}")
            
            if status_code == 100:
                print("   ✅ Message queued successfully")
            elif status_code == 101:
                print("   ✅ Message sent successfully")
            elif status_code == 102:
                print("   ✅ Message delivered")
            elif status_code == 401:
                print("   ❌ Unauthorized - Check your API key")
            elif status_code == 406:
                print("   ⚠️  User in blacklist (sandbox restriction)")
                print("   💡 Solution: Add phone to sandbox whitelist in AT dashboard")
            else:
                print(f"   ⚠️  Unknown status code: {status_code}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"   Error type: {type(e).__name__}")

# Test 2: Send without sender ID
print("\n" + "="*60)
print("\n🧪 Test 2: Sending without Sender ID")
try:
    message = "Test 2: No sender ID. Testing AfricasTalking connection."
    response = sms.send(message, [test_phone])
    print(f"✅ Response: {response}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("\n📋 Troubleshooting Guide:")
print("="*60)
print("""
1. ❌ Status Code 406 (Blacklist):
   - Your number is not whitelisted in sandbox
   - Go to: AT Dashboard → Sandbox → Phone Numbers
   - Add your phone number to the whitelist
   
2. ❌ Status Code 401 (Unauthorized):
   - Wrong API key or username
   - Verify credentials in .env file
   
3. ❌ No response/timeout:
   - Check internet connection
   - Verify AT_USERNAME is correct
   - Try using 'sandbox' for testing
   
4. ✅ Status Code 100-102:
   - Message sent successfully!
   - If not received, check:
     * Phone signal
     * Message center settings
     * Wait a few minutes
     
5. 🔍 Still not working?
   - Check AfricasTalking SMS Logs in dashboard
   - Verify callback URL is correct
   - Make sure shortcode matches (3854 or 20880)
""")

print("\n🌐 Important URLs:")
print("="*60)
print("AT Dashboard: https://account.africastalking.com/")
print("SMS Logs: https://account.africastalking.com/sms/logs")
print("Sandbox: https://account.africastalking.com/sandbox")
print(f"Your ngrok URL: https://044ad3cea41b.ngrok-free.app/sms/callback")
