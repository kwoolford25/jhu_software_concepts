from flask import Blueprint, render_template
from query_data import get_all_query_results

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get all query results
    results = get_all_query_results()
    return render_template('main/index.html', results=results) 