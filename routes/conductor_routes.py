from flask import Blueprint, request, jsonify, current_app
from functools import wraps
from models import db, Passenger, ConductorMessage, PassengerResponse
from sms_service import sms_service

conductor_bp = Blueprint('conductor', __name__)

def check_auth(username, password):
    """Verify conductor credentials"""
    return (username == current_app.config['CONDUCTOR_USERNAME'] and 
            password == current_app.config['CONDUCTOR_PASSWORD'])

def authenticate():
    """Send 401 response for failed authentication"""
    from flask import make_response
    response = make_response(jsonify({'error': 'Authentication required'}), 401)
    response.headers['WWW-Authenticate'] = 'Basic realm="Nazigi Stamford Bus - Conductor Login"'
    return response

def requires_auth(f):
    """Decorator for routes that require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@conductor_bp.route('/conductor/send-message', methods=['POST'])
@requires_auth
def send_message():
    """
    Send bulk message to all opted-in passengers
    Expects JSON: {"message": "Your message text"}
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message text is required'}), 400
        
        message_text = data['message']
        
        # Get all opted-in passengers
        opted_in_passengers = Passenger.query.filter_by(opted_in=True).all()
        
        if not opted_in_passengers:
            return jsonify({'error': 'No opted-in passengers found'}), 404
        
        # Prepare recipients list
        recipients = [p.phone_number for p in opted_in_passengers]
        
        # Format message with stops
        stops = current_app.config['BUS_STOPS']
        full_message = f"{message_text}\n\nAvailable stops:\n"
        for idx, stop in enumerate(stops, 1):
            full_message += f"{idx}. {stop}\n"
        full_message += "\nReply with the number or name of your preferred stop."
        
        # Send bulk SMS
        response = sms_service.send_bulk_sms(recipients, full_message)
        
        # Save conductor message
        conductor_msg = ConductorMessage(
            message_text=message_text,
            recipients_count=len(recipients)
        )
        db.session.add(conductor_msg)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Bulk SMS sent successfully',
            'recipients_count': len(recipients),
            'message_id': conductor_msg.id,
            'at_response': response
        })
        
    except Exception as e:
        current_app.logger.error(f"Error sending conductor message: {str(e)}")
        return jsonify({'error': str(e)}), 500

@conductor_bp.route('/conductor/send-custom', methods=['POST'])
@requires_auth
def send_custom_message():
    """
    Send custom message without stop options
    Expects JSON: {"message": "Your message text"}
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message text is required'}), 400
        
        message_text = data['message']
        
        # Get all opted-in passengers
        opted_in_passengers = Passenger.query.filter_by(opted_in=True).all()
        
        if not opted_in_passengers:
            return jsonify({'error': 'No opted-in passengers found'}), 404
        
        # Prepare recipients list
        recipients = [p.phone_number for p in opted_in_passengers]
        
        # Send bulk SMS
        response = sms_service.send_bulk_sms(recipients, message_text)
        
        # Save conductor message
        conductor_msg = ConductorMessage(
            message_text=message_text,
            recipients_count=len(recipients)
        )
        db.session.add(conductor_msg)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Custom message sent successfully',
            'recipients_count': len(recipients),
            'message_id': conductor_msg.id
        })
        
    except Exception as e:
        current_app.logger.error(f"Error sending custom message: {str(e)}")
        return jsonify({'error': str(e)}), 500

@conductor_bp.route('/conductor/passengers', methods=['GET'])
@requires_auth
def get_passengers():
    """Get list of all passengers with their opt-in status"""
    try:
        passengers = Passenger.query.all()
        
        passengers_list = [{
            'id': p.id,
            'phone_number': p.phone_number,
            'opted_in': p.opted_in,
            'created_at': p.created_at.isoformat(),
            'updated_at': p.updated_at.isoformat()
        } for p in passengers]
        
        opted_in_count = sum(1 for p in passengers if p.opted_in)
        
        return jsonify({
            'total_passengers': len(passengers),
            'opted_in': opted_in_count,
            'opted_out': len(passengers) - opted_in_count,
            'passengers': passengers_list
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting passengers: {str(e)}")
        return jsonify({'error': str(e)}), 500

@conductor_bp.route('/conductor/responses', methods=['GET'])
@requires_auth
def get_responses():
    """Get passenger responses to conductor messages"""
    try:
        # Optional: filter by message_id
        message_id = request.args.get('message_id', type=int)
        
        if message_id:
            responses = PassengerResponse.query.filter_by(message_id=message_id).all()
        else:
            # Get recent responses (last 100)
            responses = PassengerResponse.query.order_by(
                PassengerResponse.responded_at.desc()
            ).limit(100).all()
        
        responses_list = [{
            'id': r.id,
            'passenger_phone': r.passenger.phone_number,
            'message_id': r.message_id,
            'response_text': r.response_text,
            'selected_stop': r.selected_stop,
            'responded_at': r.responded_at.isoformat()
        } for r in responses]
        
        # Group by stop
        stop_counts = {}
        for r in responses:
            if r.selected_stop:
                stop_counts[r.selected_stop] = stop_counts.get(r.selected_stop, 0) + 1
        
        return jsonify({
            'total_responses': len(responses_list),
            'responses': responses_list,
            'stop_summary': stop_counts
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting responses: {str(e)}")
        return jsonify({'error': str(e)}), 500

@conductor_bp.route('/conductor/messages', methods=['GET'])
@requires_auth
def get_messages():
    """Get history of conductor messages"""
    try:
        messages = ConductorMessage.query.order_by(
            ConductorMessage.sent_at.desc()
        ).limit(50).all()
        
        messages_list = [{
            'id': m.id,
            'message_text': m.message_text,
            'recipients_count': m.recipients_count,
            'sent_at': m.sent_at.isoformat(),
            'responses_count': len(m.responses)
        } for m in messages]
        
        return jsonify({
            'total_messages': len(messages_list),
            'messages': messages_list
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting messages: {str(e)}")
        return jsonify({'error': str(e)}), 500

@conductor_bp.route('/conductor/dashboard', methods=['GET'])
@requires_auth
def dashboard():
    """Get dashboard HTML page"""
    try:
        from flask import render_template
        # Always return HTML page for GET requests
        return render_template('conductor.html')
        
    except Exception as e:
        current_app.logger.error(f"Error getting dashboard: {str(e)}")
        return jsonify({'error': str(e)}), 500

@conductor_bp.route('/conductor/api/stats', methods=['GET'])
@requires_auth
def dashboard_stats():
    """Get dashboard statistics as JSON"""
    try:
        total_passengers = Passenger.query.count()
        opted_in = Passenger.query.filter_by(opted_in=True).count()
        total_messages = ConductorMessage.query.count()
        total_responses = PassengerResponse.query.count()
        
        # Recent message
        latest_message = ConductorMessage.query.order_by(
            ConductorMessage.sent_at.desc()
        ).first()
        
        return jsonify({
            'statistics': {
                'total_passengers': total_passengers,
                'opted_in': opted_in,
                'opted_out': total_passengers - opted_in,
                'total_messages_sent': total_messages,
                'total_responses': total_responses
            },
            'latest_message': {
                'id': latest_message.id if latest_message else None,
                'text': latest_message.message_text if latest_message else None,
                'sent_at': latest_message.sent_at.isoformat() if latest_message else None,
                'recipients': latest_message.recipients_count if latest_message else 0
            } if latest_message else None
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting dashboard stats: {str(e)}")
        return jsonify({'error': str(e)}), 500
