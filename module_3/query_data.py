import psycopg2
import pandas as pd

def get_db_connection():
    """Create a connection to the PostgreSQL database"""
    conn = psycopg2.connect(
        dbname="gradcafe_db",
        user="postgres",
        password="your_password",  # Change this to your password
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

def get_fall_2024_count():
    """How many entries do you have in your database who have applied for Fall 2024?"""
    query = """
    SELECT COUNT(*) as count
    FROM applicants
    WHERE term LIKE '%Fall 2024%'
    """
    result = execute_query(query)
    return result.iloc[0]['count']

def get_international_percentage():
    """What percentage of entries are from international students?"""
    query = """
    SELECT 
        ROUND(
            (COUNT(*) FILTER (WHERE us_or_international = 'International') * 100.0) / 
            NULLIF(COUNT(*), 0), 
            2
        ) as international_percentage
    FROM applicants
    WHERE us_or_international IS NOT NULL
    """
    result = execute_query(query)
    return result.iloc[0]['international_percentage']

def get_average_metrics():
    """What is the average GPA, GRE, GRE V, GRE AW of applicants who provide these metrics?"""
    query = """
    SELECT 
        ROUND(AVG(gpa), 2) as avg_gpa,
        ROUND(AVG(gre), 2) as avg_gre,
        ROUND(AVG(gre_v), 2) as avg_gre_v,
        ROUND(AVG(gre_aw), 2) as avg_gre_aw
    FROM applicants
    WHERE gpa IS NOT NULL OR gre IS NOT NULL OR gre_v IS NOT NULL OR gre_aw IS NOT NULL
    """
    return execute_query(query).iloc[0].to_dict()

def get_american_fall_2024_avg_gpa():
    """What is their average GPA of American students in Fall 2024?"""
    query = """
    SELECT ROUND(AVG(gpa), 2) as avg_gpa
    FROM applicants
    WHERE us_or_international = 'American' AND term LIKE '%Fall 2024%' AND gpa IS NOT NULL
    """
    result = execute_query(query)
    return result.iloc[0]['avg_gpa']

def get_fall_2024_acceptance_percentage():
    """What percent of entries for Fall 2024 are Acceptances?"""
    query = """
    SELECT 
        ROUND(
            (COUNT(*) FILTER (WHERE status = 'Accepted' OR status LIKE '%Accept%') * 100.0) / 
            NULLIF(COUNT(*), 0), 
            2
        ) as acceptance_percentage
    FROM applicants
    WHERE term LIKE '%Fall 2024%'
    """
    result = execute_query(query)
    return result.iloc[0]['acceptance_percentage']

def get_fall_2024_accepted_avg_gpa():
    """What is the average GPA of applicants who applied for Fall 2024 who are Acceptances?"""
    query = """
    SELECT ROUND(AVG(gpa), 2) as avg_gpa
    FROM applicants
    WHERE (status = 'Accepted' OR status LIKE '%Accept%') 
    AND term LIKE '%Fall 2024%' 
    AND gpa IS NOT NULL
    """
    result = execute_query(query)
    return result.iloc[0]['avg_gpa']

def get_jhu_cs_masters_count():
    """How many entries are from applicants who applied to JHU for a masters degrees in Computer Science?"""
    query = """
    SELECT COUNT(*) as count
    FROM applicants
    WHERE program LIKE '%JHU%' AND program LIKE '%Computer Science%' 
    AND degree LIKE '%Master%'
    """
    result = execute_query(query)
    return result.iloc[0]['count']

def get_all_query_results():
    """Run all queries and return results as a dictionary"""
    results = {
        "fall_2024_count": get_fall_2024_count(),
        "international_percentage": get_international_percentage(),
        "average_metrics": get_average_metrics(),
        "american_fall_2024_avg_gpa": get_american_fall_2024_avg_gpa(),
        "fall_2024_acceptance_percentage": get_fall_2024_acceptance_percentage(),
        "fall_2024_accepted_avg_gpa": get_fall_2024_accepted_avg_gpa(),
        "jhu_cs_masters_count": get_jhu_cs_masters_count()
    }
    return results

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