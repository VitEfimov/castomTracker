import re

def parse_percent(value: str) -> float:
    """
    Parses a percentage string like "2.5%" or "Free" into a float (0.025 or 0.0).
    Returns 0.0 if value is Free, None, or invalid.
    Strictly requires '%' symbol for numeric values to avoid confusing specific rates.
    """
    if not value:
        return 0.0
    
    val_str = str(value).lower().strip()
    if "free" in val_str:
        return 0.0
        
    if "%" not in val_str:
        return 0.0
    
    # Extract number
    match = re.search(r"([\d\.]+)", val_str)
    if match:
        try:
            return float(match.group(1)) / 100.0
        except ValueError:
            return 0.0
            
    return 0.0

def parse_cents(value: str) -> float:
    """
    Parses a specific rate string like "6.5¢/kg" into a float dollars (0.065).
    """
    if not value:
        return 0.0
        
    val_str = str(value).lower().strip()
    # Looks for cents symbol or "¢"
    match = re.search(r"([\d\.]+)\s*(?:¢|c|cents)", val_str)
    if match:
        try:
            return float(match.group(1)) / 100.0
        except ValueError:
            return 0.0
    
    # Might handle $/kg too if needed, but per specs focused on cents
    return 0.0

def calculate_duty(
    hts_doc: dict,
    declared_value: float,
    quantity: float,
    country_code: str,
    chapter99_duties: list[dict]
) -> float:
    """
    Calculates total duty based on HTS data, transaction details, and overrides.
    
    hts_doc: The HTS data object (must contain 'duties' dict)
    declared_value: Value of goods in USD
    quantity: Quantity of goods
    country_code: ISO 2-char country code of origin (e.g. "CA", "CN")
    chapter99_duties: List of dicts e.g. [{"type": "percent", "rate": 0.25}] for Section 301
    """
    duty = 0.0
    duties_meta = hts_doc.get("duties", {})

    # 1️⃣ General duty
    general_rate = duties_meta.get("general")
    if general_rate:
        # Assuming general is usually ad valorem percent. 
        # Real world is mixed (compound duties), but we start with percent as per prompt "6.5%"
        rate = parse_percent(general_rate)
        # Check if it might be specific? 
        # Prompt examples: "6.5%", "14%". "15.4¢/kg + 40.5%" usually in 'other' or complex general
        # For this version we treat general as ad valorem primarily unless forced otherwise.
        # But wait, specs said "General duty rate... 6.5%".
        # If parse_percent returns > 0, use it.
        # Implementation note: parse_percent is safe.
        duty += declared_value * rate
        
        # If General was specific (e.g. cents/kg), parse_percent might return 0 if no %.
        # Let's check for specific if percent was 0 and string wasn't "Free"
        if rate == 0.0 and "free" not in str(general_rate).lower():
             spec_rate = parse_cents(general_rate)
             if spec_rate > 0:
                 duty += quantity * spec_rate

    # 2️⃣ Preferential duty (FTA)
    special = duties_meta.get("special") or ""
    # "Free (A,AU,BH,CL...)"
    # We check if country_code is in the parens
    if special and "free" in special.lower():
        # Simple check: is country code in the string inside parens?
        # e.g. (A, AU, ...)
        # Regex to find codes in parens
        if "(" in special and ")" in special:
            content = special[special.find("(")+1:special.find(")")]
            codes = [c.strip() for c in content.split(",")]
            # Mapping: "CA" might match 'CA' or 'MX' (USMCA uses 'S' sometimes? user spec says "Free (A,AU...)")
            # We assume direct match for now.
            if country_code in codes:
                duty = 0.0 # Override General

    # 3️⃣ Chapter 99 additional duties
    # These stack on top
    for ch99 in chapter99_duties:
        if ch99["type"] == "percent":
            duty += declared_value * ch99["rate"]
        elif ch99["type"] == "specific":
            duty += quantity * ch99["rate"]

    return round(duty, 2)
