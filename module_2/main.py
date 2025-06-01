"""
Main entry point for the Grad Cafe data scraper.

This script orchestrates the scraping and processing of graduate school
admission data from The Grad Cafe website.
"""

import os
import argparse
import logging
from datetime import datetime

# Import project modules
from src.scraper.scrape import check_robots_txt, load_existing_data, scrape_data, save_raw_data, merge_with_existing_data
from src.processor.clean import load_raw_data, clean_data, save_data

# Set up logging
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f'gradcafe_scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Scrape and process graduate school admission data from The Grad Cafe')
    parser.add_argument('--query', type=str, default='computer+science', help='Search query (default: computer+science)')
    parser.add_argument('--max-pages', type=int, default=500, help='Maximum number of pages to scrape (default: 500)')
    parser.add_argument('--delay', type=float, default=2, help='Delay between requests in seconds (default: 2)')
    parser.add_argument('--skip-scrape', action='store_true', help='Skip scraping and only process existing data')
    parser.add_argument('--skip-clean', action='store_true', help='Skip cleaning and only scrape data')
    
    args = parser.parse_args()
    
    # Define file paths
    raw_data_dir = os.path.join(os.path.dirname(__file__), 'data', 'raw')
    processed_data_dir = os.path.join(os.path.dirname(__file__), 'data', 'processed')
    docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
    
    # Ensure directories exist
    for directory in [raw_data_dir, processed_data_dir, docs_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    raw_data_file = os.path.join(raw_data_dir, 'raw_applicant_data.json')
    processed_data_file = os.path.join(processed_data_dir, 'applicant_data.json')
    robots_txt_file = os.path.join(docs_dir, 'robots_txt.txt')
    robots_screenshot_file = os.path.join(docs_dir, 'robots_verification.jpg')
    
    if not args.skip_scrape:
        # Check robots.txt first
        logger.info("Checking robots.txt...")
        robots = check_robots_txt(robots_txt_file, robots_screenshot_file)
        
        # If robots.txt allows scraping, proceed
        if robots and "/survey/" not in robots:
            logger.info("Robots.txt allows scraping. Proceeding...")
            
            # Load existing data to avoid duplicates
            existing_data, existing_urls = load_existing_data(processed_data_file)
            
            # Scrape new data
            logger.info(f"Scraping data with query: {args.query}, max_pages: {args.max_pages}, delay: {args.delay}...")
            new_data = scrape_data(query=args.query, max_pages=args.max_pages, delay=args.delay, existing_urls=existing_urls)
            
            if new_data:
                # Merge with existing data
                all_data = merge_with_existing_data(new_data, existing_data)
                
                # Save the combined raw data
                logger.info(f"Saving {len(all_data)} total entries to {raw_data_file}...")
                save_raw_data(all_data, raw_data_file)
                
                logger.info(f"Successfully scraped {len(new_data)} new entries. Total entries: {len(all_data)}")
            else:
                logger.info("No new data was scraped.")
        else:
            logger.error("Scraping is not allowed by robots.txt or couldn't access it.")
    
    if not args.skip_clean:
        # Load raw data
        logger.info(f"Loading raw data from {raw_data_file}...")
        raw_data = load_raw_data(raw_data_file)
        
        if raw_data:
            # Clean the data
            logger.info("Cleaning data...")
            cleaned_data = clean_data(raw_data)
            
            # Save the cleaned data
            logger.info(f"Saving cleaned data to {processed_data_file}...")
            save_data(cleaned_data, processed_data_file)
            
            logger.info(f"Successfully cleaned and saved {len(cleaned_data)} entries.")
        else:
            logger.error("No raw data to clean.")
    
    logger.info("Process completed.")

if __name__ == "__main__":
    main()