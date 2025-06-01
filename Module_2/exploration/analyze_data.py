"""
Simple data analysis script to test the load_data function.
"""

import os
import sys
import logging
from collections import Counter

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Import the load_data function
from src.processor.clean import load_data

def analyze_acceptance_rates(data):
    """Analyze acceptance rates by program, university, and degree."""
    if not data:
        logger.error("No data to analyze")
        return
    
    logger.info(f"Analyzing {len(data)} application records")
    
    # Overall acceptance rate
    accepted = sum(1 for item in data if item.get('status') == 'Accepted')
    total = len(data)
    acceptance_rate = accepted / total if total > 0 else 0
    
    logger.info(f"Overall acceptance rate: {acceptance_rate:.2%} ({accepted}/{total})")
    
    # Acceptance rate by degree
    degree_counts = {}
    for item in data:
        degree = item.get('degree', 'Unknown')
        if not degree:
            degree = 'Unknown'
        
        if degree not in degree_counts:
            degree_counts[degree] = {'accepted': 0, 'total': 0}
        
        degree_counts[degree]['total'] += 1
        if item.get('status') == 'Accepted':
            degree_counts[degree]['accepted'] += 1
    
    logger.info("\nAcceptance rates by degree:")
    for degree, counts in degree_counts.items():
        rate = counts['accepted'] / counts['total'] if counts['total'] > 0 else 0
        logger.info(f"{degree}: {rate:.2%} ({counts['accepted']}/{counts['total']})")
    
    # Top programs by number of applications
    program_counter = Counter(item.get('program_name', 'Unknown') for item in data if item.get('program_name'))
    
    logger.info("\nTop 10 programs by number of applications:")
    for program, count in program_counter.most_common(10):
        logger.info(f"{program}: {count} applications")
    
    # Acceptance rate by international/domestic status
    status_counts = {}
    for item in data:
        status = item.get('student_type', 'Unknown')
        if not status:
            status = 'Unknown'
        
        if status not in status_counts:
            status_counts[status] = {'accepted': 0, 'total': 0}
        
        status_counts[status]['total'] += 1
        if item.get('status') == 'Accepted':
            status_counts[status]['accepted'] += 1
    
    logger.info("\nAcceptance rates by student status:")
    for status, counts in status_counts.items():
        rate = counts['accepted'] / counts['total'] if counts['total'] > 0 else 0
        logger.info(f"{status}: {rate:.2%} ({counts['accepted']}/{counts['total']})")

def main():
    """Main function to load and analyze data."""
    # Define the path to the processed data
    # Use relative path from the exploration directory
    processed_data_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      'data', 'processed', 'applicant_data.json')
    
    # Load the data
    logger.info(f"Loading data from {processed_data_file}")
    data = load_data(processed_data_file)
    
    if data:
        logger.info(f"Successfully loaded {len(data)} records")
        analyze_acceptance_rates(data)
    else:
        logger.error("Failed to load data or no data available")

if __name__ == "__main__":
    main()