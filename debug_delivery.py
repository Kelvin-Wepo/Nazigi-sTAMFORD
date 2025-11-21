#!/usr/bin/env python3
"""
Check recent SMS logs and test sending with different configurations
"""
import os
import sys
from dotenv import load_dotenv
import africastalking

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models import SMSLog, Passenger

load_dotenv()

app = create_app()

with app.app_context():
    print("📊 Recent SMS Logs")
    print("="*80)
    
    logs = SMSLog.query.order_by(SMSLog.created_at.desc()).limit(10).all()
    
    for log in logs:
        direction_icon = "📤" if log.direction == "outgoing" else "📥"
        print(f"{direction_icon} {log.phone_number} | {log.status} | {log.created_at}")
        print(f"   Message: {log.message[:60]}...")
        print()
    
    print("\n👥 Recent Passengers")
    print("="*80)
    passengers = Passenger.query.order_by(Passenger.created_at.desc()).limit(5).all()
    
    for p in passengers:
        opt_status = "✅ Opted In" if p.opted_in else "❌ Not Opted In"
        print(f"{p.phone_number} | {opt_status} | Created: {p.created_at}")
    
    print("\n" + "="*80)
    print("\n🧪 Testing SMS Send with Different Configurations")
    print("="*80)
    
    # Get credentials
    USERNAME = os.getenv('AT_USERNAME')
    API_KEY = os.getenv('AT_API_KEY')
    SENDER_ID = os.getenv('AT_SENDER_ID')
    SHORTCODE = os.getenv('AT_SHORTCODE')
    
    print(f"\nCurrent Config:")
    print(f"  Username: {USERNAME}")
    print(f"  Sender ID: {SENDER_ID}")
    print(f"  Shortcode: {SHORTCODE}")
    
    # Initialize AT
    africastalking.initialize(USERNAME, API_KEY)
    sms = africastalking.SMS
    
    test_phone = "+254799489045"  # From your logs
    
    print(f"\n📱 Test Phone: {test_phone}")
    print("="*80)
    
    # Test 1: With Sender ID
    print("\n🧪 Test 1: Sending with Sender ID (20880)")
    try:
        message = "TEST 1: Message with sender ID 20880. Reply YES if received."
        response = sms.send(message, [test_phone], SENDER_ID)
        
        recipients = response.get('SMSMessageData', {}).get('Recipients', [])
        if recipients:
            r = recipients[0]
            print(f"   Status: {r.get('status')}")
            print(f"   Status Code: {r.get('statusCode')}")
            print(f"   Cost: {r.get('cost')}")
            print(f"   Message ID: {r.get('messageId')}")
            
            if r.get('statusCode') == 100:
                print("   ✅ Message queued successfully")
            elif r.get('statusCode') == 101:
                print("   ✅ Message sent successfully")
            elif r.get('statusCode') == 406:
                print("   ⚠️  User in blacklist!")
                print("   💡 SOLUTION: This number needs to be whitelisted in AT")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Without Sender ID
    print("\n🧪 Test 2: Sending WITHOUT Sender ID")
    try:
        message = "TEST 2: Message without sender ID. Reply YES if received."
        response = sms.send(message, [test_phone])
        
        recipients = response.get('SMSMessageData', {}).get('Recipients', [])
        if recipients:
            r = recipients[0]
            print(f"   Status: {r.get('status')}")
            print(f"   Status Code: {r.get('statusCode')}")
            print(f"   Cost: {r.get('cost')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: With Shortcode as Sender
    print("\n🧪 Test 3: Sending with Shortcode (3854) as Sender")
    try:
        message = "TEST 3: Message from shortcode 3854. Reply YES if received."
        response = sms.send(message, [test_phone], SHORTCODE)
        
        recipients = response.get('SMSMessageData', {}).get('Recipients', [])
        if recipients:
            r = recipients[0]
            print(f"   Status: {r.get('status')}")
            print(f"   Status Code: {r.get('statusCode')}")
            print(f"   Cost: {r.get('cost')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "="*80)
    print("\n🔍 DIAGNOSIS:")
    print("="*80)
    print("""
Status Code 100 means the message was QUEUED successfully by AfricasTalking.
However, you're not receiving it. Here are the possible reasons:

1. ⚠️  SENDER ID NOT APPROVED (Most Likely!)
   - Sender ID "20880" may not be approved by AfricasTalking
   - Alphanumeric sender IDs need approval
   - Shortcode sender IDs must match your account
   
   SOLUTIONS:
   a) Leave sender ID blank (let AT use default)
   b) Use your shortcode (3854) as sender ID
   c) Apply for sender ID approval in AT dashboard
   d) For testing, use no sender ID

2. ⚠️  PHONE NUMBER IN BLACKLIST (Sandbox)
   - Status Code 406 would show if blacklisted
   - You got 100, so this might not be the issue
   - But still check: AT Dashboard → Sandbox → Phone Numbers

3. ⚠️  MESSAGE FILTERING
   - Mobile carrier blocking messages
   - Try sending to different number
   - Check if other numbers receive

4. ⚠️  DELIVERY DELAY
   - Sometimes takes 1-5 minutes
   - Check AT SMS Logs for delivery status
   - Go to: https://account.africastalking.com/sms/logs

RECOMMENDED FIXES:

Fix 1: Remove or change sender ID
   Edit .env:
   AT_SENDER_ID=           # Leave blank
   # OR
   AT_SENDER_ID=3854       # Use your shortcode

Fix 2: Check AT SMS Logs
   Go to: https://account.africastalking.com/sms/logs
   Search for: +254799489045
   Check: Delivery status

Fix 3: Test with another number
   If other numbers receive, it's carrier/number specific
    """)
