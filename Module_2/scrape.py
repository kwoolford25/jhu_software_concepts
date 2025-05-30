import urllib3
from bs4 import BeautifulSoup
import time
import json
import re
import os

def check_robots_txt():
    """Check the robots.txt file to ensure scraping is permitted."""
    http = urllib3.PoolManager()
    response = http.request('GET', 'https://www.thegradcafe.com/robots.txt')
    if response.status != 200:
        print(f"Error accessing robots.txt: Status code {response.status}")
        return None
    
    robots_txt = response.data.decode('utf-8')
    print(f"Successfully accessed robots.txt")
    
    # Save the robots.txt content to a file for reference
    with open('robots_txt.txt', 'w') as f:
        f.write(robots_txt)
    
    # Take a screenshot (this will be a text representation for now)
    with open('screenshot.jpg', 'w') as f:
        f.write("Screenshot of robots.txt content:\n\n")
        f.write(robots_txt)
    
    return robots_txt

def load_existing_data(filename="applicant_data.json"):
    """
    Load existing data to prevent duplicate scraping.
    
    Returns:
        List of dictionaries containing previously scraped data
        Set of URLs already scraped
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            print(f"Loaded {len(existing_data)} existing entries from {filename}")
            # Extract URLs for quick duplicate checking
            existing_urls = set(item['url'] for item in existing_data if 'url' in item and item['url'])
            return existing_data, existing_urls
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"No existing data found in {filename} or file is invalid.")
        return [], set()

def scrape_data(query="computer+science", max_pages=500, delay=1, existing_urls=None):
    """
    Scrape graduate school admission data from thegradcafe.com.
    
    Args:
        query: Search query (default: "computer+science")
        max_pages: Maximum number of pages to scrape (default: 500)
        delay: Delay between requests in seconds (default: 1)
        existing_urls: Set of URLs already scraped to avoid duplicates
    
    Returns:
        List of dictionaries containing admission data
    """
    if existing_urls is None:
        existing_urls = set()
        
    http = urllib3.PoolManager()
    base_url = "https://www.thegradcafe.com/survey/"
    all_results = []
    
    for page in range(1, max_pages + 1):
        url = f"{base_url}?q={query}&page={page}"
        print(f"Scraping page {page}: {url}")
        
        response = http.request('GET', url)
        if response.status != 200:
            print(f"Error accessing page {page}: Status code {response.status}")
            break
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check if we've reached the end of results
        if "No results found" in soup.text:
            print("No more results found.")
            break
        
        # Extract results from the current page
        results = extract_results(soup, existing_urls)
        if not results:
            print("No new results extracted from this page.")
            # Continue to next page instead of breaking - there might be more results
            # on later pages that aren't in our existing data
            time.sleep(delay)
            continue
        
        all_results.extend(results)
        print(f"Total new results so far: {len(all_results)}")
        
        # Stop if we have enough entries (including existing ones)
        if len(all_results) + len(existing_urls) >= 10000:
            print(f"Reached target number of entries: {len(all_results) + len(existing_urls)}")
            break
        
        # Be nice to the server
        time.sleep(delay)
    
    return all_results

def extract_results(soup, existing_urls=None):
    """
    Extract admission results from a BeautifulSoup object.
    
    Args:
        soup: BeautifulSoup object containing HTML to parse
        existing_urls: Set of URLs already scraped to avoid duplicates
    
    Returns:
        List of dictionaries containing extracted admission data
    """
    if existing_urls is None:
        existing_urls = set()
        
    results = []
    
    # Find all result rows in the table
    rows = soup.find_all('tr')
    
    # Process rows in pairs (each entry has two rows)
    i = 0
    while i < len(rows) - 1:
        # Skip non-data rows
        if not rows[i].find('td'):
            i += 1
            continue
        
        # First row contains school, program, dates, and decision
        row1 = rows[i]
        
        # Check if we have a valid result row
        school_cell = row1.find('td', class_='tw-py-5 tw-pr-3 tw-text-sm tw-pl-0')
        if not school_cell:
            i += 1
            continue
        
        # Get the URL for this result first to check for duplicates
        result_url = None
        url_link = row1.find('a', href=True)
        if url_link:
            result_url = f"https://www.thegradcafe.com{url_link['href']}"
            
            # Skip if we already have this URL
            if result_url in existing_urls:
                # Skip to next entry
                # Find how many rows to skip
                rows_to_skip = 2  # Default: main row + info row
                
                # Check if there's a comment row
                if i+2 < len(rows):
                    next_row = rows[i+2]
                    if 'tw-border-none' in next_row.get('class', []) and next_row.find('p', class_='tw-text-gray-500 tw-text-sm tw-my-0'):
                        rows_to_skip = 3  # main row + info row + comment row
                
                i += rows_to_skip
                continue
        
        # Extract data from the first row
        school = school_cell.text.strip() if school_cell else None
        
        program_cell = row1.find('td', class_='tw-px-3 tw-py-5 tw-text-sm tw-text-gray-500')
        program = None
        degree = None
        if program_cell:
            program_text = program_cell.text.strip()
            # Split program and degree
            if '•' in program_text:
                parts = program_text.split('•')
                program = parts[0].strip()
                degree = parts[1].strip()
            else:
                program = program_text
        
        # Extract date added
        date_cell = row1.find_all('td')[2] if len(row1.find_all('td')) > 2 else None
        date_added = date_cell.text.strip() if date_cell else None
        
        # Extract decision and date
        decision_cell = row1.find_all('td')[3] if len(row1.find_all('td')) > 3 else None
        decision_text = decision_cell.text.strip() if decision_cell else None
        
        decision = None
        decision_date = None
        if decision_text:
            # Parse decision and date
            decision_match = re.search(r'(Accepted|Rejected|Wait listed|Interview) on (\d+ \w+)', decision_text)
            if decision_match:
                decision = decision_match.group(1)
                decision_date = decision_match.group(2)
        
        # Second row contains additional info like season, student type, GRE scores, etc.
        row2 = rows[i+1] if i+1 < len(rows) else None
        
        # Extract data from the second row
        season = None
        student_type = None
        gre = None
        gre_v = None
        gpa = None
        gre_aw = None
        comments = None
        
        if row2:
            # Extract season
            season_div = row2.find('div', class_=lambda c: c and 'tw-bg-orange-400' in c)
            if season_div:
                season = season_div.text.strip()
            
            # Extract student type (International/American)
            student_type_div = row2.find('div', string=lambda s: s and ('International' in s or 'American' in s))
            if student_type_div:
                student_type = student_type_div.text.strip()
            
            # Extract GRE scores
            gre_div = row2.find('div', string=lambda s: s and 'GRE' in s and 'V' not in s and 'AW' not in s)
            if gre_div:
                gre_match = re.search(r'GRE (\d+)', gre_div.text)
                if gre_match:
                    gre = gre_match.group(1)
            
            # Extract GRE V score
            gre_v_div = row2.find('div', string=lambda s: s and 'GRE V' in s)
            if gre_v_div:
                gre_v_match = re.search(r'GRE V (\d+)', gre_v_div.text)
                if gre_v_match:
                    gre_v = gre_v_match.group(1)
            
            # Extract GPA
            gpa_div = row2.find('div', string=lambda s: s and 'GPA' in s)
            if gpa_div:
                gpa_match = re.search(r'GPA ([\d\.]+)', gpa_div.text)
                if gpa_match:
                    gpa = gpa_match.group(1)
            
            # Extract GRE AW score
            gre_aw_div = row2.find('div', string=lambda s: s and 'GRE AW' in s)
            if gre_aw_div:
                gre_aw_match = re.search(r'GRE AW ([\d\.]+)', gre_aw_div.text)
                if gre_aw_match:
                    gre_aw = gre_aw_match.group(1)
            
            # Check for comments in the next row
            comment_row = None
            if i+2 < len(rows):
                next_row = rows[i+2]
                if 'tw-border-none' in next_row.get('class', []) and next_row.find('p', class_='tw-text-gray-500 tw-text-sm tw-my-0'):
                    comment_row = next_row
            
            if comment_row:
                comment_cell = comment_row.find('p', class_='tw-text-gray-500 tw-text-sm tw-my-0')
                if comment_cell:
                    comments = comment_cell.text.strip()
        
        # Create a dictionary with all the extracted data
        result = {
            'program_name': program,
            'university': school,
            'comments': comments,
            'date_added': date_added,
            'url': result_url,
            'status': decision,
            'decision_date': decision_date,
            'season': season,
            'student_type': student_type,
            'gre_score': gre,
            'gre_v_score': gre_v,
            'degree': degree,
            'gpa': gpa,
            'gre_aw': gre_aw
        }
        
        results.append(result)
        
        # Move to the next result (skip the second row of the current result)
        i += 2
        
        # Skip comment row if it exists
        if comment_row:
            i += 1
    
    return results

def save_raw_data(data, filename="raw_applicant_data.json"):
    """Save raw data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Raw data saved to {filename}")

def merge_with_existing_data(new_data, existing_data):
    """
    Merge newly scraped data with existing data.
    
    Args:
        new_data: List of newly scraped data entries
        existing_data: List of existing data entries
    
    Returns:
        Combined list of data entries
    """
    return existing_data + new_data

if __name__ == "__main__":
    # Check robots.txt first
    robots = check_robots_txt()
    
    # If robots.txt allows scraping, proceed
    if robots and "/survey/" not in robots:
        # Load existing data to avoid duplicates
        existing_data, existing_urls = load_existing_data()
        
        # Scrape new data
        new_data = scrape_data(query="computer+science", max_pages=500, delay=2, existing_urls=existing_urls)
        
        # Save raw data (just the new data)
        save_raw_data(new_data, "raw_applicant_data.json")
        
        # Merge with existing data
        all_data = merge_with_existing_data(new_data, existing_data)
        
        # Save the combined raw data for cleaning
        save_raw_data(all_data, "all_raw_applicant_data.json")
        
        print(f"Successfully scraped {len(new_data)} new entries.")
        print(f"Total entries: {len(all_data)}")
    else:
        print("Scraping is not allowed by robots.txt or couldn't access it.")