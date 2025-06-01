import json
import re
import os
from datetime import datetime

def load_raw_data(filename="raw_applicant_data.json"):
    """Load raw data from a JSON file."""
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} entries from {filename}")
    return data

def clean_data(data):
    """Clean and standardize the scraped data."""
    cleaned_data = []
    
    for item in data:
        cleaned_item = {}
        
        # Clean and standardize each field
        for key, value in item.items():
            # Replace None with empty string
            if value is None:
                cleaned_item[key] = ""
            # Remove HTML tags and clean strings
            elif isinstance(value, str):
                # Remove HTML tags
                value = re.sub(r'<[^>]+>', '', value)
                # Remove extra whitespace
                value = re.sub(r'\s+', ' ', value).strip()
                cleaned_item[key] = value
            else:
                cleaned_item[key] = value
        
        # Parse dates into a consistent format
        if cleaned_item['date_added']:
            try:
                # Convert "May 28, 2025" to "2025-05-28"
                date_parts = cleaned_item['date_added'].replace(',', '').split()
                if len(date_parts) == 3:
                    month_dict = {
                        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                    }
                    month = month_dict.get(date_parts[0], '01')
                    day = date_parts[1].zfill(2)
                    year = date_parts[2]
                    cleaned_item['date_added'] = f"{year}-{month}-{day}"
            except:
                # Keep original if parsing fails
                pass
        
        # Clean decision date
        if cleaned_item['decision_date']:
            try:
                # Convert "27 May" to a standardized format
                date_parts = cleaned_item['decision_date'].split()
                if len(date_parts) == 2:
                    day = date_parts[0].zfill(2)
                    month_dict = {
                        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                    }
                    month = month_dict.get(date_parts[1], '01')
                    # Extract year from date_added if available
                    year = ""
                    if cleaned_item['date_added'] and len(cleaned_item['date_added']) >= 4:
                        year = cleaned_item['date_added'][:4]
                    else:
                        year = str(datetime.now().year)
                    
                    cleaned_item['decision_date'] = f"{year}-{month}-{day}"
            except:
                # Keep original if parsing fails
                pass
        
        # Extract program start year and semester from season
        if cleaned_item['season']:
            season_match = re.search(r'(Fall|Spring|Summer) (\d{4})', cleaned_item['season'])
            if season_match:
                cleaned_item['program_start_semester'] = season_match.group(1)
                cleaned_item['program_start_year'] = season_match.group(2)
            else:
                cleaned_item['program_start_semester'] = ""
                cleaned_item['program_start_year'] = ""
        else:
            cleaned_item['program_start_semester'] = ""
            cleaned_item['program_start_year'] = ""
        
        # Ensure all required fields are present
        required_fields = [
            'program_name', 'university', 'comments', 'date_added', 'url', 
            'status', 'decision_date', 'program_start_semester', 'program_start_year',
            'student_type', 'gre_score', 'gre_v_score', 'degree', 'gpa', 'gre_aw'
        ]
        
        for field in required_fields:
            if field not in cleaned_item:
                cleaned_item[field] = ""
        
        cleaned_data.append(cleaned_item)
    
    return cleaned_data

def save_data(data, filename="applicant_data.json"):
    """Save cleaned data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Cleaned data saved to {filename}")

if __name__ == "__main__":
    # Load raw data
    raw_data = load_raw_data()
    
    if raw_data:
        # Clean the data
        cleaned_data = clean_data(raw_data)
        
        # Save the cleaned data
        save_data(cleaned_data)
        
        print(f"Successfully cleaned and saved {len(cleaned_data)} entries.")
    else:
        print("No raw data to clean.")