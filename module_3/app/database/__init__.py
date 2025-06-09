import psycopg2
import pandas as pd

def get_db_connection():
    """Create a connection to the PostgreSQL database"""
    conn = psycopg2.connect(
        dbname="gradcafe_db",
        user="postgres",
        password="password",  # Change this
        host="localhost",
        port="5432"
    )
    return conn

def execute_query(query, params=None):
    """Execute a query and return the results as a pandas DataFrame"""
    conn = get_db_connection()
    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    finally:
        conn.close()