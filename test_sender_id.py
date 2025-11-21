#!/usr/bin/env python3
"""
Test SMS delivery with different sender ID configurations
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from sms_service import sms_service

app = create_app()

with app.app_context():
    print("🧪 TESTING SMS DELIVERY")
    print("="*60)
    
    test_phone = "+254799489045"
    test_message = "Test message from Nazigi Stamford Bus - Reply OK if received"
    
    print(f"\n📱 Test Phone: {test_phone}")
    print(f"💬 Message: {test_message}")
    print(f"🆔 Current Sender ID: {app.config.get('AT_SENDER_ID')}")
    print(f"📞 Current Shortcode: {app.config.get('AT_SHORTCODE')}")
    print("="*60)
    
    print("\n🔍 Test 1: Send with current configuration")
    print("-"*60)
    response1 = sms_service.send_sms(test_phone, test_message)
    print(f"Result: {response1}")
    
    print("\n" + "="*60)
    print("📊 ANALYSIS")
    print("="*60)
    
    if response1 and 'SMSMessageData' in response1:
        recipients = response1['SMSMessageData'].get('Recipients', [])
        if recipients:
            recipient = recipients[0]
            status = recipient.get('status')
            code = recipient.get('statusCode')
            cost = recipient.get('cost')
            
            print(f"\n✅ Status: {status}")
            print(f"🔢 Status Code: {code}")
            print(f"💰 Cost: {cost}")
            
            if code == 100:
                print("\n⚠️  WARNING: Status Code 100 = Message Queued")
                print("   This means AfricasTalking accepted it but it may not deliver.")
                print("\n🔍 POSSIBLE ISSUES:")
                print("   1. Sender ID '20880' is not approved")
                print("   2. Sender ID needs verification from AfricasTalking")
                print("   3. Numeric sender IDs require special approval")
                print("\n💡 SOLUTIONS:")
                print("   Option 1: Remove sender ID (let AT use default)")
                print("   Option 2: Use your shortcode (20384) as sender ID")
                print("   Option 3: Request sender ID approval from AfricasTalking")
                print("   Option 4: Use an alphanumeric sender ID (e.g., 'NAZIGI')")
            elif code == 101:
                print("\n✅ Status Code 101 = Successfully Delivered!")
            else:
                print(f"\n❌ Unexpected status code: {code}")
    
    print("\n" + "="*60)
    print("🔧 RECOMMENDED ACTIONS:")
    print("="*60)
    print("\n1. Check AfricasTalking Dashboard:")
    print("   → Go to SMS Logs → Outgoing")
    print("   → Search for +254799489045")
    print("   → Check delivery status")
    
    print("\n2. Check Sender ID Approval:")
    print("   → Go to Settings → Sender IDs")
    print("   → Verify if '20880' is approved")
    print("   → If not approved, request approval or use different sender")
    
    print("\n3. Test without Sender ID:")
    print("   → Comment out AT_SENDER_ID in .env")
    print("   → Restart Flask app")
    print("   → Send test message again")
    
    print("\n4. Alternative Sender IDs to try:")
    print("   → Use shortcode: 20384")
    print("   → Use alphanumeric: NAZIGI, STAMFORD")
    print("   → Leave blank (default)")
