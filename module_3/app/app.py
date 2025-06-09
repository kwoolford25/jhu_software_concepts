from flask import Flask, render_template
from query_data import get_all_query_results

app = Flask(__name__)

@app.route('/')
def index():
    # Get all query results
    results = get_all_query_results()
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)