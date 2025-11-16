import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/nazigi_sms')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AfricasTalking
    AT_USERNAME = os.getenv('AT_USERNAME', 'sandbox')
    AT_API_KEY = os.getenv('AT_API_KEY')
    AT_SHORTCODE = os.getenv('AT_SHORTCODE', '3854')
    AT_SENDER_ID = os.getenv('AT_SENDER_ID', 'AFTKNG')
    
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
