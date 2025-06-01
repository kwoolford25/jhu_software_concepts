# Grad Cafe Data Scraper

## Overview

The Grad Cafe Data Scraper is a tool designed to extract and process graduate school admission data from [The Grad Cafe](https://www.thegradcafe.com/) website, converting collected information into structured JSON for data analysis.

## Project Structure

```
Module_2/
├── src/                    
│   ├── scraper/            # Scraper module
│   │   └── scrape.py       # Main scraping functionality
│   └── processor/          # Data processing module
│       └── clean.py        # Data cleaning functionality
├── data/
│   ├── raw/                # Raw scraped data
│   │   └── raw_applicant_data.json
│   └── processed/          # Cleaned and processed data
│       └── applicant_data.json
├── docs/
│   ├── robots_txt.txt
│   └── robots_verification.jpg
├── tests/                  # Unit tests
├── notebooks/              # Jupyter notebooks for exploration
├── logs/                   # Log files
├── main.py                 # Entry point script
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/jhu_software_concepts.git
   cd jhu_software_concepts/Module_2
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

To scrape and process the latest Grad Cafe data, run:

```bash
python main.py
```

### Advanced Options

You can customize the scraping behavior with command-line arguments. For example:

```bash
python main.py --query "computer+science" --max-pages 100 --delay 3
```

**Available Options:**

- `--query`: Search query (default: `"computer+science"`)
- `--max-pages`: Maximum number of pages to scrape (default: `500`)
- `--delay`: Delay (in seconds) between requests (default: `2`)
- `--skip-scrape`: Only process existing raw data (skip scraping)
- `--skip-clean`: Only scrape raw data (skip cleaning)

#### Examples

- **Only Process Existing Data (Skip Scraping):**

  ```bash
  python main.py --skip-scrape
  ```

- **Only Scrape Data (Skip Cleaning):**

  ```bash
  python main.py --skip-clean
  ```

## Data Structure

The collected data includes fields such as:

- Program Name
- University
- Comments (if available)
- Date Added to Grad Café
- URL to applicant entry
- Applicant Status (Accepted, Rejected, Waitlisted, Interview)
- Decision Date
- Program Start Semester and Year
- International/American Student status
- GRE Score (if available)
- GRE V Score (if available)
- Degree Type (Masters or PhD)
- GPA (if available)
- GRE AW (if available)

## Compliance

This project parses and respects the `robots.txt` rules of The Grad Cafe website. The scraper is configured to include appropriate delays to avoid overloading their servers.

## Acknowledgments

- [The Grad Cafe](https://www.thegradcafe.com/) for providing the data source.