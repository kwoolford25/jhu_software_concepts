# Module 3: SQL Data Analysis

This project analyzes graduate school application data from GradCafe using PostgreSQL and displays the results through a Flask web application.

## Project Structure

- `app.py`: Flask application main file
- `load_data.py`: Script to load data into PostgreSQL
- `query_data.py`: Script to run queries and display results
- `limitations.pdf`: Essay on limitations of anonymously submitted data
- `templates/`: HTML templates for the Flask application
- `static/css/`: CSS stylesheets for the Flask application
- `data/`: Directory containing raw and processed data
- `tools/`: Directory containing data preprocessing tools
- `requirements.txt`: Required Python packages

## Setup Instructions

1. Install PostgreSQL if you don't have it already.

2. Create a new PostgreSQL database:
   ```
   createdb gradcafe_db
   ```

3. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

4. Update database connection parameters in `load_data.py` and `query_data.py` with your PostgreSQL credentials.

5. Preprocess the raw data (if needed):
   ```
   python tools/preprocess_data.py
   ```

6. Load data into the database:
   ```
   python load_data.py
   ```

7. Run the queries to see results in terminal:
   ```
   python query_data.py
   ```

8. Run the Flask application:
   ```
   python app.py
   ```

9. Access the web application at http://localhost:5000

## Data Analysis Questions

The application answers the following questions:
1. How many entries do you have in your database who have applied for Fall 2024?
2. What percentage of entries are from international students?
3. What is the average GPA, GRE, GRE V, GRE AW of applicants who provide these metrics?
4. What is their average GPA of American students in Fall 2024?
5. What percent of entries for Fall 2024 are Acceptances?
6. What is the average GPA of applicants who applied for Fall 2024 who are Acceptances?
7. How many entries are from applicants who applied to JHU for a masters degrees in Computer Science?