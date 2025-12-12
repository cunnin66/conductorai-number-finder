import re

def extract_numbers(text: str):
    return [int(num) for num in re.findall(r'\d+', text)]