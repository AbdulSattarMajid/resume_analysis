import re
from datetime import datetime

def calculate_experience(text):
    """
    Rule-based No-AI logic to calculate total years of experience.
    Looks for year pairs (e.g., 2018 - 2021) or (2022 - Present).
    """
    current_year = datetime.now().year
    total_years = 0
    
    # Clean the text slightly to make matching easier
    text = text.lower()
    
    # Regex Pattern: Looks for "YYYY - YYYY" or "YYYY to Present/Current"
    # Matches: 2018-2020, 2019 to 2021, 2022 - present
    pattern = r'(20\d{2})\s*[-to]+\s*(20\d{2}|present|current)'
    
    matches = re.findall(pattern, text)
    
    # Keep track of years we've already counted to avoid double counting 
    # overlapping jobs (e.g., two side hustles in the same year)
    counted_years = set()
    
    for start_str, end_str in matches:
        start_year = int(start_str)
        
        if end_str in ['present', 'current']:
            end_year = current_year
        else:
            end_year = int(end_str)
            
        # Ensure logic doesn't break if someone types "2024 - 2020" by mistake
        if start_year <= end_year and start_year >= 1990:
            for y in range(start_year, end_year + 1):
                counted_years.add(y)
                
    # Calculate the total unique years worked
    # If the length is 0, but they have skills, they might be an entry-level candidate
    total_years = len(counted_years)
    
    # Adjust for partial years (if they only worked 1 year, we count it as 1)
    if total_years > 0:
        total_years -= 1 
        
    return total_years