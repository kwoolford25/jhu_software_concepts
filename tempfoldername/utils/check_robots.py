"""
Standalone utility to check robots.txt for The Grad Cafe website.
"""

import urllib3

def check_robots_txt():
    """Check the robots.txt file to ensure scraping is permitted."""
    http = urllib3.PoolManager()
    response = http.request('GET', 'https://www.thegradcafe.com/robots.txt')
    if response.status != 200:
        print(f"Error accessing robots.txt: Status code {response.status}")
        return None
    
    robots_txt = response.data.decode('utf-8')
    print("Successfully accessed robots.txt")
    print(robots_txt)
    
    # Save the robots.txt content to a file for reference
    with open('docs/robots_txt.txt', 'w') as f:
        f.write(robots_txt)
    
    # Take a screenshot (this will be a text representation for now)
    with open('docs/robots_verification.jpg', 'w') as f:
        f.write("Screenshot of robots.txt content:\n\n")
        f.write(robots_txt)
    
    return robots_txt

if __name__ == "__main__":
    check_robots_txt()