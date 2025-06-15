"""
Database query module for GradCafe data analysis.

This module provides functions to query the PostgreSQL database
containing GradCafe application data and analyze various metrics.
"""

import psycopg2
import pandas as pd
from psycopg2 import sql

def get_db_connection():
    """
    Create a connection to the PostgreSQL database.
    
    Returns:
        connection: A PostgreSQL database connection.
    """
    conn = psycopg2.connect(
        dbname="gradcafe_db",
        user="postgres",
        password="password",  # Change this to your password
        host="localhost",
        port="5432"
    )
    return conn

def execute_query(query, params=None):
    """
    Execute a query and return the results as a pandas DataFrame.
    
    Args:
        query: SQL query string or sql.Composed object
        params: Parameters for the query (optional)
        
    Returns:
        DataFrame: Query results as a pandas DataFrame
    """
    conn = get_db_connection()
    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    finally:
        conn.close()

def get_fall_2024_count():
    """
    How many entries do you have in your database who have applied for Fall 2024?
    
    Returns:
        int: Count of Fall 2024 applications
    """
    query = sql.SQL("""
    SELECT COUNT(*) as count
    FROM applicants
    WHERE term LIKE %s
    LIMIT 1000
    """)
    
    result = execute_query(query, params=['%Fall 2024%'])
    return result.iloc[0]['count']

def get_international_percentage():
    """
    What percentage of entries are from international students?
    
    Returns:
        float: Percentage of international students
    """
    query = sql.SQL("""
    SELECT 
        ROUND(
            (COUNT(*) FILTER (WHERE us_or_international = %s) * 100.0) / 
            NULLIF(COUNT(*), 0)::numeric, 
            2
        ) as international_percentage
    FROM applicants
    WHERE us_or_international IS NOT NULL
    LIMIT 1000
    """)
    
    result = execute_query(query, params=['International'])
    return result.iloc[0]['international_percentage']

def get_average_metrics():
    """
    What is the average GPA, GRE, GRE V, GRE AW of applicants who provide these metrics?
    
    Returns:
        dict: Dictionary containing average metrics
    """
    query = sql.SQL("""
    SELECT 
        ROUND(AVG(CASE WHEN gpa BETWEEN 0 AND 4 THEN gpa ELSE NULL END)::numeric, 2) as avg_gpa,
        ROUND(AVG(gre)::numeric, 2) as avg_gre,
        ROUND(AVG(gre_v)::numeric, 2) as avg_gre_v,
        ROUND(AVG(gre_aw)::numeric, 2) as avg_gre_aw
    FROM applicants
    WHERE gpa IS NOT NULL OR gre IS NOT NULL OR gre_v IS NOT NULL OR gre_aw IS NOT NULL
    LIMIT 1000
    """)
    
    return execute_query(query).iloc[0].to_dict()

def get_american_fall_2024_avg_gpa():
    """
    What is their average GPA of American students in Fall 2024?
    
    Returns:
        float: Average GPA of American students in Fall 2024
    """
    query = sql.SQL("""
    SELECT ROUND(AVG(CASE WHEN gpa BETWEEN 0 AND 4 THEN gpa ELSE NULL END)::numeric, 2) as avg_gpa
    FROM applicants
    WHERE us_or_international = %s AND term LIKE %s AND gpa IS NOT NULL
    LIMIT 1000
    """)
    
    result = execute_query(query, params=['American', '%Fall 2024%'])
    return result.iloc[0]['avg_gpa']

def get_fall_2024_acceptance_percentage():
    """
    What percent of entries for Fall 2024 are Acceptances?
    
    Returns:
        float: Percentage of Fall 2024 entries that are acceptances
    """
    query = sql.SQL("""
    SELECT 
        ROUND(
            (COUNT(*) FILTER (WHERE status = %s OR status LIKE %s) * 100.0) / 
            NULLIF(COUNT(*), 0)::numeric, 
            2
        ) as acceptance_percentage
    FROM applicants
    WHERE term LIKE %s
    LIMIT 1000
    """)
    
    result = execute_query(query, params=['Accepted', '%Accept%', '%Fall 2024%'])
    return result.iloc[0]['acceptance_percentage']

def get_fall_2024_accepted_avg_gpa():
    """
    What is the average GPA of applicants who applied for Fall 2024 who are Acceptances?
    
    Returns:
        float: Average GPA of accepted Fall 2024 applicants
    """
    query = sql.SQL("""
    SELECT ROUND(AVG(CASE WHEN gpa BETWEEN 0 AND 4 THEN gpa ELSE NULL END)::numeric, 2) as avg_gpa
    FROM applicants
    WHERE (status = %s OR status LIKE %s) 
    AND term LIKE %s 
    AND gpa IS NOT NULL
    LIMIT 1000
    """)
    
    result = execute_query(query, params=['Accepted', '%Accept%', '%Fall 2024%'])
    return result.iloc[0]['avg_gpa']

def get_jhu_cs_masters_count():
    """
    How many entries are from applicants who applied to JHU for a masters degrees in Computer Science?
    
    Returns:
        int: Count of JHU CS Masters applications
    """
    query = sql.SQL("""
    SELECT COUNT(*) as count
    FROM applicants
    WHERE (program LIKE %s OR 
           program LIKE %s OR 
           program LIKE %s OR
           program LIKE %s) 
    AND program LIKE %s 
    AND degree LIKE %s
    LIMIT 1000
    """)
    
    params = [
        '%JHU%', 
        '%Johns Hopkins%', 
        '%John Hopkins%', 
        '%Hopkins University%',
        '%Computer Science%',
        '%Master%'
    ]
    
    result = execute_query(query, params=params)
    return result.iloc[0]['count']

def get_all_query_results():
    """
    Run all queries and return results as a dictionary.
    
    Returns:
        dict: Dictionary containing all query results
    """
    query_results = {
        "fall_2024_count": get_fall_2024_count(),
        "international_percentage": get_international_percentage(),
        "average_metrics": get_average_metrics(),
        "american_fall_2024_avg_gpa": get_american_fall_2024_avg_gpa(),
        "fall_2024_acceptance_percentage": get_fall_2024_acceptance_percentage(),
        "fall_2024_accepted_avg_gpa": get_fall_2024_accepted_avg_gpa(),
        "jhu_cs_masters_count": get_jhu_cs_masters_count()
    }
    return query_results

if __name__ == "__main__":
    results = get_all_query_results()
    
    print("\n===== GradCafe Data Analysis Results =====\n")
    
    print("1. Fall 2024 Applications:")
    print(f"   {results['fall_2024_count']} entries\n")
    
    print("2. International Student Percentage:")
    print(f"   {results['international_percentage']}%\n")
    
    print("3. Average Metrics:")
    print(f"   GPA: {results['average_metrics']['avg_gpa']}")
    print(f"   GRE Quant: {results['average_metrics']['avg_gre']}")
    print(f"   GRE Verbal: {results['average_metrics']['avg_gre_v']}")
    print(f"   GRE AW: {results['average_metrics']['avg_gre_aw']}\n")
    
    print("4. American Fall 2024 Average GPA:")
    print(f"   {results['american_fall_2024_avg_gpa']}\n")
    
    print("5. Fall 2024 Acceptance Percentage:")
    print(f"   {results['fall_2024_acceptance_percentage']}%\n")
    
    print("6. Fall 2024 Accepted Average GPA:")
    print(f"   {results['fall_2024_accepted_avg_gpa']}\n")
    
    print("7. JHU CS Masters Applications:")
    print(f"   {results['jhu_cs_masters_count']} entries\n")
    
    print("==========================================")