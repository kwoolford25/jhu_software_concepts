import json
import psycopg2
import pandas as pd
from datetime import datetime

def load_data_to_postgres():
    """
    Load the processed GradCafe data into a PostgreSQL database
    """
    print("Starting data loading process...")
    
    # Database connection parameters
    db_params = {
        'dbname': 'gradcafe_db',
        'user': 'postgres',
        'password': 'your_password',  # Change this to your password
        'host': 'localhost',
        'port': '5432'
    }
    
    # Path to your processed data
    data_path = 'data/processed_data.json'
    
    try:
        # Read the processed data
        print(f"Reading data from {data_path}...")
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Connect to PostgreSQL
        print("Connecting to PostgreSQL database...")
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        print("Creating applicants table if it doesn't exist...")
        cursor.execute("""
        DROP TABLE IF EXISTS applicants;
        CREATE TABLE applicants (
            p_id SERIAL PRIMARY KEY,
            program TEXT,
            comments TEXT,
            date_added DATE,
            url TEXT,
            status TEXT,
            term TEXT,
            us_or_international TEXT,
            gpa FLOAT,
            gre FLOAT,
            gre_v FLOAT,
            gre_aw FLOAT,
            degree TEXT
        )
        """)
        
        # Insert data into the table
        print("Inserting data into the applicants table...")
        for record in data:
            # Convert empty strings to None for numeric fields
            gpa = None if record['gpa'] == '' else record['gpa']
            gre = None if record['gre'] == '' else record['gre']
            gre_v = None if record['gre_v'] == '' else record['gre_v']
            gre_aw = None if record['gre_aw'] == '' else record['gre_aw']
            
            # Convert date string to date object
            date_added = None
            if record['date_added']:
                try:
                    date_added = datetime.strptime(record['date_added'], '%Y-%m-%d').date()
                except ValueError:
                    print(f"Warning: Invalid date format: {record['date_added']}")
            
            cursor.execute("""
            INSERT INTO applicants (program, comments, date_added, url, status, term, us_or_international, gpa, gre, gre_v, gre_aw, degree)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                record['program'],
                record['comments'],
                date_added,
                record['url'],
                record['status'],
                record['term'],
                record['us_or_international'],
                gpa,
                gre,
                gre_v,
                gre_aw,
                record['degree']
            ))
        
        # Commit changes and close connection
        conn.commit()
        print(f"Data successfully loaded into PostgreSQL database! Inserted {len(data)} records.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    load_data_to_postgres()