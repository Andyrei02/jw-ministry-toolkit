import re

def extract_time(text):
    pattern = r'\((\d+ min\.)\)'
    match = re.search(pattern, text)
    
    if match:
        return match.group(1)
    else:
        return None

