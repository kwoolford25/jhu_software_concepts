# Grad Cafe Data Scraper

## Programmer - Kyle Woolford - JHED: kwoolfo4@jh.edu

## Module 2 - Web Scraping - Due Date: 6/1/25 11:59PM

## Approach

This project implements a robust web scraper for The Grad Cafe website to collect graduate school admission data. The approach follows a modular design with clear separation of concerns, focusing on maintainability, scalability, and compliance with web scraping best practices.

### Architecture Overview

The project is structured into several key components:

1. **Data Acquisition (Scraping)**: Responsible for fetching raw data from The Grad Cafe website
2. **Data Processing (Cleaning)**: Handles transformation of raw data into a clean, structured format
3. **Data Storage**: Manages saving and loading data in JSON format
4. **Utilities**: Additional helper functions for tasks like checking robots.txt
5. **Exploration**: Scripts for exploring the website structure and analyzing the collected data

### Data Acquisition Process

The scraping process follows these steps:

1. **Robots.txt Verification**: Before scraping, the program checks the robots.txt file to ensure compliance with the website's scraping policies. This is handled by the `check_robots_txt()` function.

2. **Incremental Scraping**: To avoid duplicate entries, the program first loads existing data (if any) and keeps track of URLs already scraped. This allows for incremental scraping over multiple runs.

3. **Page Navigation**: The scraper starts with the Computer Science results page and navigates through pagination to collect data from multiple pages.

4. **HTML Parsing**: Each page is parsed using BeautifulSoup to extract structured data from the HTML. The extraction logic handles the complex table structure of The Grad Cafe results page, where each entry spans multiple rows.

5. **Rate Limiting**: To be respectful of the website's resources, the scraper implements a configurable delay between requests.

### Data Extraction Strategy

The data extraction uses a combination of CSS selectors, string methods, and regular expressions:

1. **Table Row Processing**: Each admission result spans 2-3 rows in the HTML table. The first row contains basic information (university, program, dates), the second row contains additional details (GRE scores, student type), and an optional third row may contain comments.

2. **CSS Selectors**: BeautifulSoup's CSS selectors are used to target specific elements, such as:
   - `td.tw-py-5.tw-pr-3.tw-text-sm.tw-pl-0` for the university name
   - `div.tw-bg-orange-400` for the program start season

3. **Regular Expressions**: Regex is used to extract structured information from text fields:
   - `r'(Accepted|Rejected|Wait listed|Interview) on (\d+ \w+)'` to parse decision status and date
   - `r'GRE (\d+)'` to extract GRE scores
   - `r'(Fall|Spring|Summer) (\d{4})'` to parse semester and year

### Data Cleaning Process

The raw scraped data undergoes several cleaning steps:

1. **HTML Removal**: Any remnant HTML tags are removed using regex (`re.sub(r'<[^>]+>', '', value)`)

2. **Date Standardization**: Dates are converted to a consistent ISO format (YYYY-MM-DD)
   - "May 28, 2025" → "2025-05-28"
   - "27 May" → "2025-05-27" (year inferred from context)

3. **Null Value Handling**: Missing values are consistently represented as empty strings

4. **Field Extraction**: Compound fields like "season" are split into separate fields (program_start_semester, program_start_year)

5. **Data Validation**: Basic validation ensures data integrity and consistency

### Data Storage Strategy

The data is stored in JSON format, which offers several advantages:

1. **Human Readability**: JSON is easy to read and inspect
2. **Language Agnostic**: Can be used by various programming languages and tools
3. **Hierarchical Structure**: Naturally represents the nested structure of the data
4. **No Schema Constraints**: Flexible for handling missing or variable fields

Two main JSON files are maintained:
- `raw_applicant_data.json`: Contains the raw scraped data before cleaning
- `applicant_data.json`: Contains the cleaned, processed data ready for analysis

### Error Handling and Resilience

The code implements comprehensive error handling to ensure resilience:

1. **Request Failures**: HTTP request failures are caught and logged
2. **Parsing Errors**: Errors in parsing HTML or extracting data are handled gracefully
3. **File I/O Errors**: Issues with reading or writing files are properly managed
4. **Logging**: Detailed logging provides visibility into the scraping and processing operations

### Performance Considerations

Several optimizations improve the performance of the scraper:

1. **Duplicate Detection**: URLs are tracked to avoid processing duplicate entries
2. **Incremental Processing**: Only new data is scraped in subsequent runs
3. **Efficient HTML Parsing**: Targeted CSS selectors minimize unnecessary DOM traversal
4. **Memory Management**: Data is processed in a streaming fashion rather than loading everything into memory

### Extensibility

The modular design allows for easy extension:

1. **Configurable Parameters**: Query terms, page limits, and delays can be configured
2. **Command-line Interface**: Arguments allow flexible usage patterns
3. **Modular Functions**: Clear separation of concerns makes it easy to modify or extend functionality
4. **Analysis-Ready Data**: The cleaned data is structured for straightforward analysis

## Known Bugs

No known bugs in the current implementation. The scraper successfully extracts all required fields from The Grad Cafe website and processes them into a clean, structured format. All edge cases, such as missing data fields, HTML remnants, and date parsing, are properly handled.

Note that the scraper is dependent on the current HTML structure of The Grad Cafe website. If the website undergoes significant redesign, the CSS selectors and parsing logic may need to be updated accordingly.

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
git clone https://github.com/kwoolford25/jhu_software_concepts.git
cd ./module_2
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

Return a single page from website to guide parsing logic:
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