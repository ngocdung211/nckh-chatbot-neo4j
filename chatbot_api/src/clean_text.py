import re
def clean_text(text):
    # Replace multiple newlines and spaces with a single newline
    text = re.sub(r'\n\s*\n+', '\n', text)  # Collapse multiple blank lines
    
    # Replace excessive spaces within a line
    text = re.sub(r'[ \t]+', ' ', text)  # Replace multiple spaces or tabs with a single space
    
    # Trim spaces at the beginning and end of lines
    text = "\n".join([line.strip() for line in text.splitlines()])
    
    # Remove any leading or trailing whitespace in the entire text
    return text.strip()