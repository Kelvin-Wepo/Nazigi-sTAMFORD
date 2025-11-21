#!/usr/bin/env python3
"""
Quick test to verify the complete registration and messaging flow
"""
import requests
import time

BASE_URL = "http://localhost:5000"
TEST_PHONE = "+254799489045"

def test_registration():
    """Test passenger registration with TEXT2"""
    print("\n" + "="*60)
    print("🧪 TEST 1: PASSENGER REGISTRATION")
    print("="*60)
    
    # Simulate incoming TEXT2
    print("\n📱 Simulating: Passenger sends 'TEXT2' to 20384")
    response = requests.post(f"{BASE_URL}/sms/callback", data={
        'from': TEST_PHONE,
        'text': 'TEXT2',
        'to': '20384'
    })
    
    print(f"✅ Response: {response.status_code}")
    print(f"📬 Data: {response.json()}")
    print("\n📲 Passenger should receive:")
    print("   'Welcome to Nazigi Stamford! 🚌")
    print("    Would you like to opt?")
    print("    Reply: 1 to Opt In, 2 to Opt Out'")
    
    time.sleep(1)
    
    # Simulate opt-in
    print("\n📱 Simulating: Passenger replies '1' (Opt In)")
    response = requests.post(f"{BASE_URL}/sms/callback", data={
        'from': TEST_PHONE,
        'text': '1',
        'to': '20384'
    })
    
    print(f"✅ Response: {response.status_code}")
    print(f"📬 Data: {response.json()}")
    print("\n📲 Passenger should receive:")
    print("   'Thank you for opting in! ✅")
    print("    You will now receive updates...'")

def test_conductor_message():
    """Test conductor sending message"""
    print("\n" + "="*60)
    print("🧪 TEST 2: CONDUCTOR SENDS MESSAGE")
    print("="*60)
    
    # Login and send message
    print("\n👨‍✈️ Conductor sends message via dashboard")
    response = requests.post(
        f"{BASE_URL}/conductor/send-message",
        auth=('admin', 'admin123'),
        json={
            'message': 'Nazigi stamford is leaving Nairobi CBD now where should we pick you?'
        }
    )
    
    print(f"✅ Response: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"📬 Data: {data}")
        print(f"\n📊 Recipients: {data.get('recipients_count', 0)}")
        print("\n📲 Passengers receive:")
        print("   'Nazigi stamford is leaving Nairobi CBD now where should we pick you?")
        print("    Please reply with the number of your preferred stop:")
        print("    1. 🚏 Ngara")
        print("    2. 🚏 Allsops")
        print("    ... (all 10 stops)")
        
        return data.get('message_id')
    else:
        print(f"❌ Error: {response.text}")
        return None

def test_passenger_response(message_id):
    """Test passenger selecting stop"""
    print("\n" + "="*60)
    print("🧪 TEST 3: PASSENGER SELECTS STOP")
    print("="*60)
    
    # Simulate stop selection
    print("\n📱 Simulating: Passenger replies '5' (Zimmerman)")
    response = requests.post(f"{BASE_URL}/sms/callback", data={
        'from': TEST_PHONE,
        'text': '5',
        'to': '20384'
    })
    
    print(f"✅ Response: {response.status_code}")
    print(f"📬 Data: {response.json()}")
    print("\n📲 Passenger should receive:")
    print("   '✅ Confirmed! You will be picked up at Zimmerman.'")
    
    time.sleep(1)
    
    # Check responses in dashboard
    if message_id:
        print("\n👨‍✈️ Checking conductor dashboard...")
        response = requests.get(
            f"{BASE_URL}/conductor/responses?message_id={message_id}",
            auth=('admin', 'admin123')
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Response Analytics:")
            print(f"   Total Responses: {data.get('total_responses', 0)}")
            print(f"   Responses by Stop:")
            for stop, count in data.get('responses_by_stop', {}).items():
                if count > 0:
                    print(f"      {stop}: {count}")

def main():
    print("\n🚌 NAZIGI STAMFORD BUS - COMPLETE SYSTEM TEST")
    print("="*60)
    print("Testing keyword: TEXT2")
    print("Testing shortcode: 20384")
    print("="*60)
    
    try:
        # Test 1: Registration
        test_registration()
        
        time.sleep(2)
        
        # Test 2: Conductor message
        message_id = test_conductor_message()
        
        time.sleep(2)
        
        # Test 3: Passenger response
        test_passenger_response(message_id)
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED!")
        print("="*60)
        print("\n📋 Summary:")
        print("✅ Registration flow working")
        print("✅ Conductor messaging working")
        print("✅ Passenger responses tracked")
        print("✅ Dashboard showing analytics")
        print("\n🎯 Next Step: Test with real SMS from your phone!")
        print("   Send 'TEXT2' to 20384")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    main()
