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
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Nazigi Stamford Bus SMS Service</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }
                .container {
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    text-align: center;
                }
                h1 { color: #333; margin-bottom: 20px; }
                p { color: #666; margin-bottom: 30px; }
                .btn {
                    display: inline-block;
                    padding: 15px 30px;
                    background: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                }
                .btn:hover { background: #764ba2; }
                .info { margin-top: 20px; font-size: 14px; color: #999; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚌 Nazigi Stamford Bus SMS Service</h1>
                <p>Welcome to the conductor control panel</p>
                <a href="/conductor/dashboard" class="btn">Access Dashboard</a>
                <div class="info">
                    <p>Default credentials: admin / admin123</p>
                </div>
            </div>
        </body>
        </html>
        '''
    
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
