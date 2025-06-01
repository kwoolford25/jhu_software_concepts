# Grad Cafe Data Scraper

## Overview
This project scrapes graduate school admission data from The Grad Cafe website and processes it into a structured JSON format for analysis.

## Project Structure
```
Module_2/
├── src/                      # Source code directory
│   ├── scraper/              # Scraper module
│   │   └── scrape.py         # Main scraping functionality
│   └── processor/            # Data processing module
│       └── clean.py          # Data cleaning functionality
├── data/                     # Data directory
│   ├── raw/                  # Raw data
│   │   └── raw_applicant_data.json
│   └── processed/            # Processed data
│       └── applicant_data.json
├── docs/                     # Documentation
│   ├── robots_txt.txt
│   └── robots_verification.jpg
├── exploration/              # Site exploration scripts
│   ├── site_structure_exploration.py
│   └── cs_results_page.html
├── logs/                     # Log files
├── utils/                    # Utility scripts
│   └── check_robots.py       # Standalone robots.txt checker
├── main.py                   # Entry point script
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/jhu_software_concepts.git
cd jhu_software_concepts/Module_2
```

### 2. Create and activate a virtual environment:

#### For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
Run the main script to scrape and process data:
```bash
python main.py
```

### Advanced Options
The script supports several command-line arguments:
```bash
python main.py --query "computer+science" --max-pages 100 --delay 3
```

Options:
- `--query`: Search query (default: "computer+science")
- `--max-pages`: Maximum number of pages to scrape (default: 500)
- `--delay`: Delay between requests in seconds (default: 2)
- `--skip-scrape`: Skip scraping and only process existing data
- `--skip-clean`: Skip cleaning and only scrape data

### Only Clean Existing Data
```bash
python main.py --skip-scrape
```

### Only Scrape Without Cleaning
```bash
python main.py --skip-clean
```

### Utility Scripts
Check robots.txt directly:
```bash
python utils/check_robots.py
```

Explore site structure:
```bash
python exploration/site_structure_exploration.py
```

## Data Structure
The collected data includes the following fields:
- Program Name
- University
- Comments (if available)
- Date Added to Grad Café
- URL link to applicant entry
- Applicant Status (Accepted, Rejected, Wait listed, Interview)
- Decision Date
- Program Start Semester and Year
- International/American Student status
- GRE Score (if available)
- GRE V Score (if available)
- Degree Type (Masters or PhD)
- GPA (if available)
- GRE AW (if available)

## Compliance
This scraper checks and complies with the robots.txt file from The Grad Cafe website. Scraping is performed with reasonable delays to avoid overloading the server.