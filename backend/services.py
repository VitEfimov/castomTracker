import json
import os
import requests
from fuzzywuzzy import fuzz

def load_hts_data():
    try:
        # Try to load from local JSON file
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'hts_subset.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

from hts_parser import parse_hts_row

def search_usitc(query: str):
    """
    Proxies search to USITC API and maps to standard model using central parser.
    """
    try:
        url = f"https://hts.usitc.gov/reststop/search?keyword={query}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        raw_data = response.json()
        
        # Determine if list or dict wrapper
        results = raw_data if isinstance(raw_data, list) else raw_data.get('results', [])
        
        mapped_results = []
        for item in results:
            mapped_item = parse_hts_row(item)
            mapped_results.append(mapped_item)
            
        return mapped_results

    except Exception as e:
        print(f"USITC API Error: {e}")
        return []

def fetch_hts_codes(query: str):
    """
    Fetches HTS codes with AI-like probability scores.
    """
    db = load_hts_data()
    
    if not query:
        # Return all with 100% prob if no query
        for item in db:
            item['probability'] = "100%"
            item['score'] = 100
        return db

    results = []
    query_str = query.lower()
    for item in db:
        # Search match on description, hts_code, or keywords (if present)
        # Note: new model uses 'description' instead of 'full_name'
        description = item.get('description', '')
        hts_code = item.get('hts_code', '')
        
        score_name = fuzz.partial_ratio(query_str, description.lower())
        score_code = fuzz.ratio(query_str, hts_code)
        
        # Check keywords if they exist (not strictly in new spec but good to keep if valid)
        keywords = item.get('keywords', [])
        score_kw = 0
        if keywords:
            score_kw = max([fuzz.partial_ratio(query_str, kw.lower()) for kw in keywords]) if keywords else 0
            
        score = max(score_name, score_code, score_kw)
        
        if score > 40:
            item_copy = item.copy()
            item_copy['score'] = score
            # Simulate "Probability" based on score
            prob = round((score / 100) * 0.95 * 100, 2)
            if score == 100: prob = 98.5
            item_copy['probability'] = f"{prob}%"
            results.append(item_copy)
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

def get_hts_tree():
    """
    Builds a hierarchical tree from the dataset using parent_hts.
    """
    db = load_hts_data()
    
    # optimize lookup
    node_map = {item['hts_code']: {**item, 'children': [], 'name': item.get('description')} for item in db}
    roots = []
    
    # Build tree
    for item in db:
        code = item['hts_code']
        node = node_map[code]
        parent_code = item.get('parent_hts')
        
        if parent_code and parent_code in node_map:
            node_map[parent_code]['children'].append(node)
        else:
            # If no parent or parent not found in subset, treat as root
            roots.append(node)
            
    return roots

def load_chapter99_data():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'chapter99.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def get_applicable_ch99(hts_doc: dict, country_code: str):
    """
    Finds applicable Chapter 99 duties for a given HTS document and country.
    """
    ch99_db = load_chapter99_data()
    duties = []
    
    # We rely on 'chapter99_refs' populated by the parser
    # If not present (legacy or raw data), we can't link
    refs = hts_doc.get("chapter99_refs", [])
    
    for ref in refs:
        # Find matching rule in DB
        # Optimize: could convert DB to dict for O(1) lookup if large
        match = next((item for item in ch99_db if item["hts_code"] == ref), None)
        if match:
             # Check country condition
             # If country matches the restricted country (e.g. CN)
             if match.get("country") == country_code:
                 duties.append(match)
                 
    return duties

def compare_excel(file_content: bytes, current_db_codes: list):
    """
    Reads an uploaded Excel file and compares HTS codes.
    """
    # Placeholder for Excel logic
    return {"status": "success", "rows": 0, "columns": []}
