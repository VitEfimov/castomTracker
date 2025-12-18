from services import get_applicable_ch99

def test_ch99_linking():
    print("Testing Chapter 99 Linking Logic...")

    # Mock HTS document with a reference to the China Tariff (9903.88.03)
    hts_doc = {
        "hts_code": "4013.10.00.10",
        "chapter99_refs": ["9903.88.03"]
    }

    # Case 1: Country is CN (China) - Should match
    duties_cn = get_applicable_ch99(hts_doc, "CN")
    print(f"Results for CN: {len(duties_cn)}")
    assert len(duties_cn) == 1
    assert duties_cn[0]["rate"] == 0.25
    print("✅ CN triggers Section 301")

    # Case 2: Country is DE (Germany) - Should NOT match
    duties_de = get_applicable_ch99(hts_doc, "DE")
    print(f"Results for DE: {len(duties_de)}")
    assert len(duties_de) == 0
    print("✅ DE does NOT trigger Section 301")
    
    # Case 3: No refs - Should be empty
    hts_clean = {"hts_code": "1234", "chapter99_refs": []}
    duties_none = get_applicable_ch99(hts_clean, "CN")
    assert len(duties_none) == 0
    print("✅ No refs = No extra duty")

if __name__ == "__main__":
    test_ch99_linking()
