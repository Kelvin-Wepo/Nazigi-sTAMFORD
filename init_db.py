"""Initialize database tables

Run this script to create all database tables
"""

from app import create_app
from models import db

def init_db():
    """Initialize database tables"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        # Print table information
        print("\nCreated tables:")
        print("- passengers")
        print("- conductor_messages")
        print("- passenger_responses")
        print("- sms_logs")

if __name__ == '__main__':
    init_db()
