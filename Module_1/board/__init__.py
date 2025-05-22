from flask import Flask, request

from board import pages

def create_app():
    app = Flask(__name__)  # Flask Constructor
    
    # Make request available in templates for active nav highlighting
    @app.context_processor
    def inject_request():
        return {'request': request}
    
    # Register the pages blueprint
    app.register_blueprint(pages.bp)
    
    return app