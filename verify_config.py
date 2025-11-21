#!/usr/bin/env python3
"""
Verify current SMS configuration
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

with app.app_context():
    print("🔍 CURRENT SMS CONFIGURATION")
    print("="*60)
    print(f"Username:    {app.config.get('AT_USERNAME')}")
    print(f"Shortcode:   {app.config.get('AT_SHORTCODE')}")
    print(f"Sender ID:   {app.config.get('AT_SENDER_ID')}")
    print(f"API Key:     {'*' * 20}...{app.config.get('AT_API_KEY')[-10:] if app.config.get('AT_API_KEY') else 'Not Set'}")
    print("="*60)
    
    sender_id = app.config.get('AT_SENDER_ID')
    
    if sender_id is None:
        print("\n✅ PERFECT! Sender ID is None")
        print("   Messages will be sent WITHOUT a sender ID")
        print("   AfricasTalking will use their default sender")
        print("\n📱 This should fix your SMS delivery issue!")
    elif sender_id == '':
        print("\n✅ GOOD! Sender ID is empty string")
        print("   Messages will be sent without a specific sender ID")
    else:
        print(f"\n⚠️  WARNING! Sender ID is still set to: {sender_id}")
        print("   This may block SMS delivery if not approved")
        print("\n🔧 To fix:")
        print("   1. Comment out AT_SENDER_ID in .env")
        print("   2. Set default to None in config.py")
        print("   3. Restart Flask app")
