from flask import Blueprint, request, jsonify, current_app
from models import db, Passenger, ConductorMessage, PassengerResponse
from sms_service import sms_service
import re

sms_bp = Blueprint('sms', __name__)

def normalize_phone_number(phone):
    """Normalize phone number format"""
    # Remove spaces and special characters
    phone = re.sub(r'[^\d+]', '', phone)
    
    # Ensure it starts with country code
    if phone.startswith('0'):
        phone = '+254' + phone[1:]
    elif not phone.startswith('+'):
        phone = '+' + phone
        
    return phone

def format_stops_message():
    """Format bus stops into numbered message"""
    stops = current_app.config['BUS_STOPS']
    message = "Please reply with the number of your preferred stop:\n\n"
    for idx, stop in enumerate(stops, 1):
        message += f"{idx}. {stop}\n"
    return message

@sms_bp.route('/sms/callback', methods=['GET', 'POST'])
def sms_callback():
    """
    Handle incoming SMS from AfricasTalking
    This endpoint receives all incoming messages
    """
    # Handle GET requests (for testing)
    if request.method == 'GET':
        return jsonify({
            'status': 'ready',
            'message': 'SMS callback endpoint is active',
            'endpoint': '/sms/callback',
            'method': 'POST',
            'expected_params': ['from', 'to', 'text', 'date', 'id', 'linkId']
        }), 200
    
    try:
        # Get data from AfricasTalking
        from_number = request.values.get('from', '')
        text = request.values.get('text', '').strip()
        
        current_app.logger.info(f"📥 ========== INCOMING SMS ==========")
        current_app.logger.info(f"📱 From: {from_number}")
        current_app.logger.info(f"💬 Text: {text}")
        current_app.logger.info(f"📋 All request data: {dict(request.values)}")
        
        # Normalize phone number
        from_number = normalize_phone_number(from_number)
        current_app.logger.info(f"📞 Normalized number: {from_number}")
        
        # Log incoming SMS
        sms_service.log_incoming_sms(from_number, text)
        
        # Check if passenger exists
        passenger = Passenger.query.filter_by(phone_number=from_number).first()
        
        if passenger:
            current_app.logger.info(f"👤 Passenger found: opted_in={passenger.opted_in}")
        else:
            current_app.logger.info(f"👤 New passenger, not in database yet")
        
        # Handle opt-in request (TEST2 keyword - case insensitive)
        # AfricasTalking might send just the keyword or the full message
        text_lower = text.lower().strip()
        if text_lower == 'test2' or text_lower.startswith('test2'):
            current_app.logger.info(f"🎯 Detected keyword: TEST2 - routing to opt-in handler")
            return handle_opt_in_request(from_number, passenger)
        
        # If passenger is NOT opted in yet, treat "1" and "2" as opt-in/opt-out responses
        if passenger and passenger.opted_in == False:
            # Handle opt-in confirmation for pending passengers
            if text.strip() == '1' or text.lower() in ['yes', 'y', 'opt in', 'optin']:
                current_app.logger.info(f"✅ Pending passenger confirming opt-in - routing to confirmation handler")
                return handle_opt_in_confirmation(from_number, passenger)
            
            # Handle opt-out for pending passengers
            elif text.strip() == '2' or text.lower() in ['no', 'n', 'opt out', 'optout', 'stop']:
                current_app.logger.info(f"🚫 Pending passenger declining - routing to opt-out handler")
                return handle_opt_out(from_number, passenger)
        
        # If passenger IS opted in, handle stop selection and other commands
        # Handle opt-in confirmation for already registered users
        if text.lower() in ['yes', 'y', 'opt in', 'optin']:
            current_app.logger.info(f"✅ Detected opt-in confirmation - routing to confirmation handler")
            return handle_opt_in_confirmation(from_number, passenger)
        
        # Handle opt-out
        elif text.lower() in ['no', 'n', 'opt out', 'optout', 'stop']:
            current_app.logger.info(f"🚫 Detected opt-out - routing to opt-out handler")
            return handle_opt_out(from_number, passenger)
        
        # Handle stop selection (number 1-10)
        elif text.isdigit():
            current_app.logger.info(f"🔢 Detected numeric input - routing to stop selection handler")
            return handle_stop_selection(from_number, passenger, int(text))
        
        # Handle stop selection by name
        else:
            current_app.logger.info(f"📝 Detected text input - routing to stop name handler")
            return handle_stop_name_selection(from_number, passenger, text)
        
    except Exception as e:
        current_app.logger.error(f"❌ CRITICAL ERROR in SMS callback: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

def handle_opt_in_request(phone_number, passenger):
    """Handle initial opt-in request when user sends 'stamford'"""
    try:
        current_app.logger.info(f"🎯 Processing opt-in request for {phone_number}")
        
        if not passenger:
            # Create new passenger
            current_app.logger.info(f"👤 Creating new passenger: {phone_number}")
            passenger = Passenger(phone_number=phone_number, opted_in=False)
            db.session.add(passenger)
            db.session.commit()
        else:
            current_app.logger.info(f"👤 Existing passenger found: {phone_number}")
        
        # Send opt-in/opt-out question
        message = ("Welcome to Nazigi Stamford! \n\n"
                  "Would you like to opt?\n\n"
                  "Reply:\n"
                  "1 to Opt In\n"
                  "2 to Opt Out")
        
        current_app.logger.info(f"📲 Sending opt-in message to {phone_number}")
        response = sms_service.send_sms(phone_number, message)
        current_app.logger.info(f"📬 Response from send_sms: {response}")
        
        return jsonify({'status': 'success', 'message': 'Opt-in request sent'}), 200
        
    except Exception as e:
        current_app.logger.error(f"❌ Error handling opt-in request: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

def handle_opt_in_confirmation(phone_number, passenger):
    """Handle opt-in confirmation"""
    try:
        current_app.logger.info(f"✅ Processing opt-in confirmation for {phone_number}")
        
        if not passenger:
            current_app.logger.info(f"👤 Creating new passenger with opt-in: {phone_number}")
            passenger = Passenger(phone_number=phone_number, opted_in=True)
            db.session.add(passenger)
        else:
            current_app.logger.info(f"👤 Updating existing passenger to opted-in: {phone_number}")
            passenger.opted_in = True
        
        db.session.commit()
        
        message = ("Thank you for opting in! \n\n"
                  "You will now receive updates from Nazigi Stamford Bus conductors.\n\n"
                  "To opt out anytime, send STOP to 20384.")
        
        current_app.logger.info(f"📲 Sending confirmation message to {phone_number}")
        response = sms_service.send_sms(phone_number, message)
        current_app.logger.info(f"📬 Response from send_sms: {response}")
        
        return jsonify({'status': 'success', 'message': 'User opted in'}), 200
        
    except Exception as e:
        current_app.logger.error(f"❌ Error handling opt-in confirmation: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

def handle_opt_out(phone_number, passenger):
    """Handle opt-out request"""
    try:
        current_app.logger.info(f"🚫 Processing opt-out request for {phone_number}")
        
        if passenger:
            passenger.opted_in = False
            db.session.commit()
            current_app.logger.info(f"👤 Passenger {phone_number} opted out")
            
            message = ("You have been opted out from Nazigi Stamford Bus Service.\n\n"
                      "To opt in again, send TEST2 to 20384.")
        else:
            current_app.logger.info(f"👤 Passenger {phone_number} not registered")
            message = "You are not registered in our service."
        
        current_app.logger.info(f"📲 Sending opt-out confirmation to {phone_number}")
        response = sms_service.send_sms(phone_number, message)
        current_app.logger.info(f"📬 Response from send_sms: {response}")
        
        return jsonify({'status': 'success', 'message': 'User opted out'}), 200
        
        return jsonify({'status': 'success', 'message': 'User opted out'})
        
    except Exception as e:
        current_app.logger.error(f"❌ Error handling opt-out: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

def handle_stop_selection(phone_number, passenger, stop_number):
    """Handle when passenger selects a stop by number"""
    try:
        current_app.logger.info(f"🚏 Processing stop selection for {phone_number}: #{stop_number}")
        
        if not passenger or not passenger.opted_in:
            current_app.logger.warning(f"⚠️ Passenger {phone_number} not opted in, rejecting stop selection")
            message = "Please opt in first by sending TEST2 to 20384."
            sms_service.send_sms(phone_number, message)
            return jsonify({'status': 'error', 'message': 'User not opted in'})
        
        stops = current_app.config['BUS_STOPS']
        
        if 1 <= stop_number <= len(stops):
            selected_stop = stops[stop_number - 1]
            current_app.logger.info(f"✅ Valid stop selected: {selected_stop}")
            
            # Save response
            response = PassengerResponse(
                passenger_id=passenger.id,
                response_text=str(stop_number),
                selected_stop=selected_stop
            )
            db.session.add(response)
            db.session.commit()
            
            message = f"✅ Confirmed! You will be picked up at {selected_stop}.\n\nThank you for using Nazigi Stamford Bus Service!"
            current_app.logger.info(f"📲 Sending confirmation to {phone_number}")
            response_sms = sms_service.send_sms(phone_number, message)
            current_app.logger.info(f"📬 Response from send_sms: {response_sms}")
            
            return jsonify({'status': 'success', 'message': f'Stop selected: {selected_stop}'})
        else:
            current_app.logger.warning(f"⚠️ Invalid stop number: {stop_number} (valid: 1-{len(stops)})")
            message = f"Invalid stop number. Please select a number between 1 and {len(stops)}."
            sms_service.send_sms(phone_number, message)
            return jsonify({'status': 'error', 'message': 'Invalid stop number'})
        
    except Exception as e:
        current_app.logger.error(f"❌ Error handling stop selection: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

def handle_stop_name_selection(phone_number, passenger, text):
    """Handle when passenger types stop name"""
    try:
        if not passenger or not passenger.opted_in:
            message = "Please opt in first by sending TEST2 to 20384."
            sms_service.send_sms(phone_number, message)
            return jsonify({'status': 'error', 'message': 'User not opted in'})
        
        stops = current_app.config['BUS_STOPS']
        text_lower = text.lower()
        
        # Try to match stop name
        matched_stop = None
        for stop in stops:
            if stop.lower() in text_lower or text_lower in stop.lower():
                matched_stop = stop
                break
        
        if matched_stop:
            # Save response
            response = PassengerResponse(
                passenger_id=passenger.id,
                response_text=text,
                selected_stop=matched_stop
            )
            db.session.add(response)
            db.session.commit()
            
            message = f"✅ Confirmed! You will be picked up at {matched_stop}.\n\nThank you for using Nazigi Stamford Bus Service!"
            sms_service.send_sms(phone_number, message)
            
            return jsonify({'status': 'success', 'message': f'Stop selected: {matched_stop}'})
        else:
            # Send available stops
            message = "Sorry, I didn't understand that stop.\n\n" + format_stops_message()
            sms_service.send_sms(phone_number, message)
            return jsonify({'status': 'error', 'message': 'Stop not recognized'})
        
    except Exception as e:
        current_app.logger.error(f"Error handling stop name selection: {str(e)}")
        return jsonify({'error': str(e)}), 500
