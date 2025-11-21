#!/usr/bin/env python3
"""
Health check script for Docker container
"""
import sys
import os

try:
    # Check if app can be imported
    from app import create_app
    
    app = create_app()
    with app.app_context():
        # Try to access database
        from models import db
        db.engine.execute('SELECT 1')
    
    print("Health check passed")
    sys.exit(0)
except Exception as e:
    print(f"Health check failed: {e}")
    sys.exit(1)
