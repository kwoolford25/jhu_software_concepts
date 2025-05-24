from flask import Flask, request
import os
from dotenv import load_dotenv

from board import pages

def create_app():
    app = Flask(__name__)  # Flask Constructor
    
    # Load environment variables
    load_dotenv()
    
    # Configure secret key for sessions
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    
    # Make request available in templates for active nav highlighting
    @app.context_processor
    def inject_request():
        return {'request': request}
    
    # Register the pages blueprint
    app.register_blueprint(pages.bp)
    
    return app