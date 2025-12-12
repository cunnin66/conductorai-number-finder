import re

def extract_numbers(text: str):
    # Match negative numbers, decimals, and comma-formatted numbers
    pattern = r'-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?'
    matches = re.findall(pattern, text)
    
    results = []
    for num in matches:
        # Remove commas for parsing
        clean_num = num.replace(',', '')
        # Use float if decimal point present, otherwise int
        if '.' in clean_num:
            results.append(float(clean_num))
        else:
            results.append(int(clean_num))
    return results