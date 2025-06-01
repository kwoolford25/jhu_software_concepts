"""
Script to explore the structure of The Grad Cafe website.
"""

import urllib3
from bs4 import BeautifulSoup
import os
import sys

def explore_cs_results_page():
    """Explore the Computer Science results page structure."""
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    http = urllib3.PoolManager()
    
    # Access the Computer Science results page
    url = "https://www.thegradcafe.com/survey/?q=computer+science"
    print(f"Accessing {url}...")
    response = http.request('GET', url)
    
    if response.status != 200:
        print(f"Error accessing CS results page: Status code {response.status}")
        return None
    
    print("Successfully accessed CS results page")
    
    # Save the page for inspection
    output_file = os.path.join(output_dir, 'cs_results_page.html')
    with open(output_file, 'wb') as f:
        f.write(response.data)
    print(f"Saved page to {output_file}")
    
    # Parse the page to understand its structure
    soup = BeautifulSoup(response.data, 'html.parser')
    
    # Check for pagination
    pagination = soup.find_all(class_="pagination")
    if pagination:
        print("Found pagination element")
        print(pagination)
    
    # Look for the table or elements containing the admission results
    results_table = soup.find('table')
    if results_table:
        print("Found results table")
        # Print the first few rows to understand the structure
        rows = results_table.find_all('tr')[:3]  # Get first 3 rows
        for row in rows:
            print(row)
    
    # Check for robots.txt
    robots_response = http.request('GET', 'https://www.thegradcafe.com/robots.txt')
    if robots_response.status == 200:
        print("Successfully accessed robots.txt")
        print(robots_response.data.decode('utf-8'))
        
        # Create docs directory if it doesn't exist
        docs_dir = os.path.join(os.path.dirname(os.path.dirname(output_dir)), 'module_2/docs')
        os.makedirs(docs_dir, exist_ok=True)
        
        # Save robots.txt for reference
        robots_file = os.path.join(docs_dir, 'robots_txt.txt')
        with open(robots_file, 'w') as f:
            f.write(robots_response.data.decode('utf-8'))
        print(f"Saved robots.txt to {robots_file}")
    else:
        print(f"Failed to access robots.txt: Status code {robots_response.status}")
    
    return soup

if __name__ == "__main__":
    explore_cs_results_page()