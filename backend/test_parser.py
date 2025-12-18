from hts_parser import parse_hts_row
import json

def test_parser():
    print("Testing HTS Parser...")

    # Sample raw data similar to what comes from USITC API
    raw_sample = {
        "htsno": "4013.10.00.10",
        "statisticalSuffix": "10",
        "description": "<div>Inner tubes, of rubber... <br>Of a kind used on motor cars</div>",
        "indent": "2",
        "general": "3.7%",
        "special": "Free",
        "other": "25%",
        "units": ["No."],
        "footnotes": [
            {"value": "See 9903.88.03 for Section 301 duties."}
        ],
        "effectivePeriod": {"from": "2024-01-01", "to": None}
    }

    parsed = parse_hts_row(raw_sample)
    
    print("\nParsed Output:")
    print(json.dumps(parsed, indent=2, default=str))

    # Assertions
    assert parsed["hts_code"] == "4013.10.00.10"
    assert parsed["level"] == "statistical"
    assert parsed["units"] == ["No."]
    assert "9903.88.03" in parsed["chapter99_refs"]
    assert parsed["requires_ch99"] is True
    assert parsed["description"] == "Inner tubes, of rubber... Of a kind used on motor cars" # HTML stripped
    print("\nSUCCESS: Parser handled HTML stripping and Ch99 extraction correctly.")

if __name__ == "__main__":
    test_parser()
