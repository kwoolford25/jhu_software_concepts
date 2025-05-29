import urllib3

def check_robots_txt():
    """Check the robots.txt file to ensure scraping is permitted."""
    http = urllib3.PoolManager()
    response = http.request('GET', 'https://www.thegradcafe.com/robots.txt')
    robots_txt = response.data.decode('utf-8')
    print(robots_txt)
    return robots_txt

if __name__ == "__main__":
    robots = check_robots_txt()
    # Save the robots.txt content to a file for reference
    with open('robots_txt_content.txt', 'w') as f:
        f.write(robots)