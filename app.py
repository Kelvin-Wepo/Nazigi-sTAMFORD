from flask import Flask, render_template
from flask_migrate import Migrate
from config import Config
from models import db
from sms_service import sms_service
from routes.sms_routes import sms_bp
from routes.conductor_routes import conductor_bp

def create_app(config_class=Config):
    """Application factory for creating Flask app"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Add Content Security Policy for inline scripts
    @app.after_request
    def add_security_headers(response):
        response.headers['Content-Security-Policy'] = "script-src 'self' 'unsafe-inline';"
        return response
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Initialize SMS service
    with app.app_context():
        sms_service.initialize(
            app.config['AT_USERNAME'],
            app.config['AT_API_KEY'],
            app.config.get('AT_SENDER_ID')
        )
    
    # Register blueprints
    app.register_blueprint(sms_bp)
    app.register_blueprint(conductor_bp)
    
    # Web interface routes
    @app.route('/')
    def index():
        return render_template('conductor.html')
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    @app.route('/api')
    def api_info():
        return {
            'status': 'running',
            'service': 'Nazigi Stamford Bus SMS Service',
            'version': '1.0.0',
            'endpoints': {
                'sms_callback': '/sms/callback',
                'conductor_dashboard': '/conductor/dashboard',
                'send_message': '/conductor/send-message',
                'get_passengers': '/conductor/passengers',
                'get_responses': '/conductor/responses'
            }
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
