from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Passenger(db.Model):
    """Model for passengers who opt-in to receive SMS"""
    __tablename__ = 'passengers'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    opted_in = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to responses
    responses = db.relationship('PassengerResponse', backref='passenger', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Passenger {self.phone_number} - {"Opted In" if self.opted_in else "Opted Out"}>'


class ConductorMessage(db.Model):
    """Model for messages sent by conductors"""
    __tablename__ = 'conductor_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    recipients_count = db.Column(db.Integer, default=0)
    
    # Relationship to responses
    responses = db.relationship('PassengerResponse', backref='conductor_message', lazy=True)
    
    def __repr__(self):
        return f'<ConductorMessage {self.id} sent at {self.sent_at}>'


class PassengerResponse(db.Model):
    """Model for tracking passenger responses to conductor messages"""
    __tablename__ = 'passenger_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('conductor_messages.id'), nullable=True)
    response_text = db.Column(db.Text, nullable=False)
    selected_stop = db.Column(db.String(100), nullable=True)
    responded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PassengerResponse from {self.passenger_id} - {self.selected_stop}>'


class SMSLog(db.Model):
    """Model for logging all SMS interactions"""
    __tablename__ = 'sms_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    direction = db.Column(db.String(10), nullable=False)  # 'incoming' or 'outgoing'
    status = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SMSLog {self.direction} - {self.phone_number}>'
