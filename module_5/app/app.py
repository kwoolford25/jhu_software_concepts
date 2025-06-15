from flask import Flask, render_template
from query_data import get_all_query_results

"""
Flask application for displaying GradCafe data analysis results.

This module provides a web interface to view the results of SQL queries
on graduate school application data from GradCafe.
"""

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application instance.
    """
    flask_app = Flask(__name__)
    
    @flask_app.route('/')
    def index():
        """
        Render the main page with query results.
        
        Returns:
            str: Rendered HTML template with query results.
        """
        results = get_all_query_results()
        return render_template('index.html', results=results)
    
    return flask_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)