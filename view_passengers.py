#!/usr/bin/env python3
"""
View all registered passengers
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models import Passenger

app = create_app()

with app.app_context():
    print("👥 REGISTERED PASSENGERS")
    print("="*60)
    
    passengers = Passenger.query.all()
    
    if not passengers:
        print("❌ No passengers registered yet")
    else:
        print(f"\n📊 Total: {len(passengers)} passenger(s)\n")
        for p in passengers:
            status = "✅ Opted In" if p.opted_in else "❌ Not Opted In"
            # Get latest response if any
            latest_response = p.responses[-1] if p.responses else None
            stop = f"🚏 {latest_response.selected_stop}" if latest_response and latest_response.selected_stop else "⚪ No stop selected"
            print(f"{p.phone_number}")
            print(f"   {status}")
            print(f"   {stop}")
            print(f"   📅 Registered: {p.created_at}")
            print()
