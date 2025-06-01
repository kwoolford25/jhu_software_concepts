from flask import Flask, request, session
from dotenv import load_dotenv
from board import pages

import os
import secrets

def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Configure secret key for sessions
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "development-temporary-key")
    
    # Generate a random session version ID at app startup
    app_session_id = secrets.token_hex(8)
    
    @app.before_request
    def clear_session_on_restart():
        # Check if the session was created with the current app instance
        if session.get('app_id') != app_session_id:
            session.clear()
            session['app_id'] = app_session_id
    
    # Make request available in templates
    @app.context_processor
    def inject_request():
        return {'request': request}
    
    # Register blueprints
    app.register_blueprint(pages.bp)
    
    return app