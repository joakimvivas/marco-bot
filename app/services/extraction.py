import spacy
import re

# Load the spaCy language model for Spanish
nlp = spacy.load("es_core_news_sm")

# Regular expressions to detect common name patterns
name_patterns = [
    r"me llamo (\w+)",  # Detect patterns like "Me llamo Pedro"
    r"mi nombre es (\w+)",  # Detect patterns like "Mi nombre es Pedro"
    r"soy (\w+)"  # Detect patterns like "Soy Pedro"
]

# Function to extract the name from the user's input
def extract_name(user_input):
    doc = nlp(user_input)
    for ent in doc.ents:
        if ent.label_ == "PER":  # Look for entities labeled as PERSON
            return ent.text
        
    # If spaCy does not detect the name, try with regular expressions
    for pattern in name_patterns:
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            return match.group(1)  # Return the first group (the name)

    return None  # Return None if no name is found

# Function to extract a phone number from the user's input
def extract_phone(user_input):
    phone_regex = r'\b\d{9}\b'  # Regex pattern for a 9-digit phone number
    match = re.search(phone_regex, user_input)
    return match.group(0) if match else None  # Return the phone number or None

# Function to extract an email from the user's input
def extract_email(user_input):
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'  # Regex pattern for an email address
    match = re.search(email_regex, user_input)
    return match.group(0) if match else None  # Return the email or None

# Function to extract the city from the user's input
def extract_city(user_input):
    doc = nlp(user_input)
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:  # Look for entities labeled as GPE (geopolitical) or LOC (location)
            return ent.text
    return None  # Return None if no city is found
