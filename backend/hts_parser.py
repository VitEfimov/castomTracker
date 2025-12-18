import re
from datetime import datetime

CH99_REGEX = re.compile(r"\b99\d{2}\.\d{2}\.\d{2}\b")

def clean_html(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"<.*?>", "", text).strip()

def infer_parent(htsno: str) -> str | None:
    if not htsno:
        return None
    parts = htsno.split(".")
    if len(parts) <= 2:
        # e.g. "8471" (len 1) or "8471.30" (len 2) -> debatable if 8471.30 has parent 8471. 
        # User said "Parent -> child relationship is implied by length + indent"
        # The prompt code says: if len <= 2 return None. 
        # But wait, 8471.30 usually implies parent 8471. 
        # Let's stick strictly to the User's provided code first.
        return None
    return ".".join(parts[:-1])

def parse_hts_row(row: dict) -> dict:
    # Handle both input keys if they vary (htsno vs hts_code)
    # The API returns 'htsno'.
    hts_code = row.get("htsno") or row.get("hts_code")
    
    description = clean_html(row.get("description", ""))

    footnotes = row.get("footnotes", [])
    ch99_refs = []

    for fn in footnotes:
        value = fn.get("value", "")
        ch99_refs.extend(CH99_REGEX.findall(value))
    
    # Safely handle units if it's not a list
    raw_units = row.get("units")
    units_list = []
    if isinstance(raw_units, list):
        units_list = raw_units
    elif isinstance(raw_units, str):
        units_list = [raw_units]
    
    # Normalize duty keys if coming from different source? 
    # USITC API has 'general', 'special', 'other' at top level.
    
    # Determine level
    stat_suffix = row.get("statisticalSuffix")
    level = "statistical" if stat_suffix else "heading" # Simplistic, could be subheading
    
    return {
        "hts_code": hts_code,
        "stat_suffix": stat_suffix or None,
        "level": level,
        "indent": int(row.get("indent", 0)),
        "description": description,
        "description_clean": description.lower(),
        "parent_hts": infer_parent(hts_code) if hts_code else None,
        "units": units_list,
        "duties": {
            "general": row.get("general"),
            "special": row.get("special"),
            "other": row.get("other"),
        },
        "chapter99_refs": list(set(ch99_refs)),
        "requires_ch99": bool(ch99_refs),
        "effective": row.get("effectivePeriod"),
        "source": "USITC",
        "created_at": datetime.utcnow().isoformat(), # JSON serializable
        "updated_at": datetime.utcnow().isoformat(),
    }
