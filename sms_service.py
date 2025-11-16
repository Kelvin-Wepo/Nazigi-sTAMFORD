import africastalking
from flask import current_app
from models import db, SMSLog

class SMSService:
    """Service for handling AfricasTalking SMS operations"""
    
    def __init__(self):
        self.username = None
        self.api_key = None
        self.sender_id = None
        self.sms = None
        
    def initialize(self, username, api_key, sender_id=None):
        """Initialize AfricasTalking SDK"""
        self.username = username
        self.api_key = api_key
        self.sender_id = sender_id
        africastalking.initialize(username, api_key)
        self.sms = africastalking.SMS
        
    def send_sms(self, recipients, message):
        """
        Send SMS to one or more recipients
        
        Args:
            recipients: List of phone numbers or single phone number string
            message: Message text to send
            
        Returns:
            Response from AfricasTalking API
        """
        try:
            # Ensure recipients is a list
            if isinstance(recipients, str):
                recipients = [recipients]
            
            current_app.logger.info(f"📤 Attempting to send SMS to: {recipients}")
            current_app.logger.info(f"📝 Message: {message[:50]}...")
            current_app.logger.info(f"🆔 Sender ID: {self.sender_id}")
            
            # Send SMS with sender ID if available
            if self.sender_id:
                current_app.logger.info(f"✉️ Sending with sender ID: {self.sender_id}")
                response = self.sms.send(message, recipients, self.sender_id)
            else:
                current_app.logger.info("✉️ Sending without sender ID")
                response = self.sms.send(message, recipients)
            
            current_app.logger.info(f"📨 AfricasTalking Response: {response}")
            
            # Check response status
            sms_data = response.get('SMSMessageData', {})
            recipients_data = sms_data.get('Recipients', [])
            
            for recipient_info in recipients_data:
                status = recipient_info.get('status', 'Unknown')
                status_code = recipient_info.get('statusCode', 'N/A')
                number = recipient_info.get('number', 'Unknown')
                
                current_app.logger.info(f"📞 {number}: Status={status}, Code={status_code}")
                
                if status == 'Success':
                    current_app.logger.info(f"✅ SMS successfully sent to {number}")
                else:
                    current_app.logger.warning(f"⚠️ SMS failed for {number}: {status} (Code: {status_code})")
            
            # Log outgoing SMS
            for recipient in recipients:
                log = SMSLog(
                    phone_number=recipient,
                    message=message,
                    direction='outgoing',
                    status='sent'
                )
                db.session.add(log)
            
            db.session.commit()
            current_app.logger.info("💾 SMS logged to database")
            
            return response
            
        except Exception as e:
            current_app.logger.error(f"❌ Error sending SMS: {str(e)}")
            current_app.logger.error(f"❌ Exception type: {type(e).__name__}")
            current_app.logger.error(f"❌ Recipients: {recipients}")
            
            # Log failed SMS
            for recipient in recipients:
                log = SMSLog(
                    phone_number=recipient,
                    message=message,
                    direction='outgoing',
                    status=f'failed: {str(e)}'
                )
                db.session.add(log)
            
            db.session.commit()
            raise
            
    def send_bulk_sms(self, recipients, message):
        """
        Send SMS to multiple recipients in bulk
        
        Args:
            recipients: List of phone numbers
            message: Message text to send
            
        Returns:
            Response from AfricasTalking API
        """
        return self.send_sms(recipients, message)
        
    def log_incoming_sms(self, phone_number, message):
        """Log incoming SMS to database"""
        try:
            log = SMSLog(
                phone_number=phone_number,
                message=message,
                direction='incoming',
                status='received'
            )
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Error logging incoming SMS: {str(e)}")

# Global SMS service instance
sms_service = SMSService()
