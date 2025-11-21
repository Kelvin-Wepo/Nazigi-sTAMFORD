#!/usr/bin/env python3
"""
Quick test - Send SMS without sender ID
"""
import requests
import time

CONDUCTOR_URL = "http://localhost:5000/conductor/send-message"
TEST_MESSAGE = "TEST: Nazigi bus leaving CBD. Reply with your stop number. No sender ID test."

print("🧪 TESTING SMS WITHOUT SENDER ID")
print("="*60)
print(f"📝 Message: {TEST_MESSAGE}")
print("="*60)

# Login credentials
auth = ('admin', 'admin123')

data = {
    'message': TEST_MESSAGE
}

print("\n📤 Sending via conductor dashboard...")
try:
    response = requests.post(CONDUCTOR_URL, auth=auth, data=data)
    print(f"✅ Status Code: {response.status_code}")
    print(f"📬 Response: {response.json()}")
    
    print("\n" + "="*60)
    print("📱 CHECK YOUR PHONE NOW!")
    print("="*60)
    print("\nYou should receive the test message WITHOUT sender ID 20880.")
    print("This means it will use AfricasTalking's default sender.")
    print("\n⏱️  Messages typically arrive within 5-10 seconds")
    print("\n🔍 Also check:")
    print("   1. Flask logs for emoji indicators")
    print("   2. AfricasTalking SMS Logs → Outgoing")
    print("   3. Look for Status Code 101 (delivered) instead of 100 (queued)")
    
except Exception as e:
    print(f"❌ Error: {e}")
