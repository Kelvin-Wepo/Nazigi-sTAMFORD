import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    # Render provides DATABASE_URL, but we need to handle postgres:// vs postgresql://
    database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/nazigi_sms')
    # Render uses postgres://, but SQLAlchemy 1.4+ requires postgresql://
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before using
        'pool_recycle': 300,     # Recycle connections after 5 minutes
        'pool_size': 10,         # Number of connections to maintain
        'max_overflow': 20,      # Max connections above pool_size
    }
    
    # AfricasTalking
    AT_USERNAME = os.getenv('AT_USERNAME', 'Kwepo')
    AT_API_KEY = os.getenv('AT_API_KEY')
    AT_SHORTCODE = os.getenv('AT_SHORTCODE', '20384')
    AT_SENDER_ID = os.getenv('AT_SENDER_ID', None)  # No default - let AT use default sender
    
    # Conductor credentials
    CONDUCTOR_USERNAME = os.getenv('CONDUCTOR_USERNAME', 'admin')
    CONDUCTOR_PASSWORD = os.getenv('CONDUCTOR_PASSWORD', 'admin123')
    
    # Bus stops
    BUS_STOPS = [
        'Ngara',
        'Allsops',
        'Homeland',
        'TRM',
        'Zimmerman',
        'Githurai 44',
        'Maziwa',
        'Kijito',
        'Kamiti',
        'Kahawa West Rounda'
    ]
