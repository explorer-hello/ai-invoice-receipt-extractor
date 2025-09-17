import spacy
import re
from datetime import datetime

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Please download the spaCy model first: python -m spacy download en_core_web_sm")
    nlp = None

def extract_date(text):
    date_patterns = [
        r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
        r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}',
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}'
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            try:
                # Try to parse the first date found
                return datetime.strptime(matches[0], "%m/%d/%Y").date().isoformat()
            except:
                try:
                    return datetime.strptime(matches[0], "%d-%m-%Y").date().isoformat()
                except:
                    continue
    return None

def extract_amounts(text):
    # Find currency amounts
    amount_pattern = r'\$?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+(?:\.\d{2})?'
    amounts = re.findall(amount_pattern, text)
    
    # Convert to floats and sort to find the largest (likely the total)
    amounts_float = []
    for amt in amounts:
        try:
            clean_amt = amt.replace('$', '').replace(',', '').strip()
            amounts_float.append(float(clean_amt))
        except:
            continue
    
    if amounts_float:
        amounts_float.sort(reverse=True)
        return amounts_float[0]  # Return the largest amount
    
    return None

def extract_vendor(text):
    # Simple vendor extraction - first line often contains vendor name
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line and not any(char.isdigit() for char in line) and len(line) > 3:
            return line
    return "Unknown Vendor"

def extract_invoice_data(text):
    if nlp is None:
        # Fallback if spaCy isn't available
        return {
            "vendor": extract_vendor(text),
            "date": extract_date(text),
            "amount": extract_amounts(text),
            "tax": None,
            "invoice_number": None,
            "raw_text": text
        }
    
    doc = nlp(text)
    
    # Extract entities
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    money = [ent.text for ent in doc.ents if ent.label_ == "MONEY"]
    
    # Get the most relevant data
    vendor = orgs[0] if orgs else extract_vendor(text)
    date = dates[0] if dates else extract_date(text)
    amount = money[0] if money else extract_amounts(text)
    
    # Extract invoice number
    inv_pattern = r'(?:invoice|inv)\.?\s*#?\s*[:]?\s*([A-Z0-9-]+)'
    inv_match = re.search(inv_pattern, text, re.IGNORECASE)
    invoice_number = inv_match.group(1) if inv_match else None
    
    return {
        "vendor": vendor,
        "date": date,
        "amount": amount,
        "tax": None,  # Could be enhanced
        "invoice_number": invoice_number,
        "raw_text": text
    }