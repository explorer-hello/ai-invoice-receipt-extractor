def categorize_expense(invoice_data):
    vendor = invoice_data.get('vendor', '').lower()
    amount = invoice_data.get('amount', 0)
    
    # Rule-based categorization
    food_keywords = ['restaurant', 'cafe', 'food', 'grocer', 'supermarket', 'bakery']
    travel_keywords = ['hotel', 'flight', 'airline', 'taxi', 'uber', 'lyft', 'transport']
    utilities_keywords = ['electric', 'water', 'gas', 'internet', 'phone', 'utility']
    rent_keywords = ['rent', 'lease', 'housing']
    
    if any(keyword in vendor for keyword in food_keywords):
        return "Food"
    elif any(keyword in vendor for keyword in travel_keywords):
        return "Travel"
    elif any(keyword in vendor for keyword in utilities_keywords):
        return "Utilities"
    elif any(keyword in vendor for keyword in rent_keywords):
        return "Rent"
    else:
        return "Misc"