#!/usr/bin/env python3
"""
Clear all registered passengers from the database
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models import Passenger, PassengerResponse, SMSLog, ConductorMessage

app = create_app()

with app.app_context():
    print("🗑️  DATABASE CLEANUP TOOL")
    print("="*60)
    
    # Count current records
    passengers_count = Passenger.query.count()
    responses_count = PassengerResponse.query.count()
    sms_logs_count = SMSLog.query.count()
    messages_count = ConductorMessage.query.count()
    
    print(f"\n📊 Current Database Stats:")
    print(f"   Passengers: {passengers_count}")
    print(f"   Passenger Responses: {responses_count}")
    print(f"   SMS Logs: {sms_logs_count}")
    print(f"   Conductor Messages: {messages_count}")
    
    if passengers_count == 0:
        print("\n✅ Database is already empty!")
        sys.exit(0)
    
    # Show current passengers
    print(f"\n👥 Registered Passengers:")
    print("-"*60)
    passengers = Passenger.query.all()
    for p in passengers:
        status = "✅ Opted In" if p.opted_in else "❌ Not Opted In"
        print(f"   {p.phone_number} | {status}")
    
    # Confirm deletion
    print("\n" + "="*60)
    print("⚠️  WARNING: This will permanently delete:")
    print(f"   - {passengers_count} passengers")
    print(f"   - {responses_count} passenger responses")
    print(f"   - {sms_logs_count} SMS logs")
    print(f"   - {messages_count} conductor messages")
    print("="*60)
    
    confirm = input("\n❓ Are you sure you want to clear ALL data? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        print("\n🗑️  Deleting all records...")
        
        # Delete in correct order (to respect foreign keys)
        PassengerResponse.query.delete()
        print(f"   ✅ Deleted {responses_count} passenger responses")
        
        SMSLog.query.delete()
        print(f"   ✅ Deleted {sms_logs_count} SMS logs")
        
        ConductorMessage.query.delete()
        print(f"   ✅ Deleted {messages_count} conductor messages")
        
        Passenger.query.delete()
        print(f"   ✅ Deleted {passengers_count} passengers")
        
        db.session.commit()
        
        print("\n✅ Database cleared successfully!")
        print("="*60)
        
        # Verify
        remaining = Passenger.query.count()
        print(f"\n📊 Remaining passengers: {remaining}")
        
    else:
        print("\n❌ Deletion cancelled. Database unchanged.")
