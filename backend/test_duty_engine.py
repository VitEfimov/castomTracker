from duty_engine import calculate_duty, parse_percent, parse_cents

def test_duty_calculation():
    print("Testing Duty Calculation Logic...")
    
    # 1. Standard General Duty
    item1 = {
        "duties": {
            "general": "2.5%",
            "special": "Free",
            "other": None
        }
    }
    # 2.5% of $1000 = $25
    d1 = calculate_duty(item1, 1000.0, 1, "CN", [])
    assert d1 == 25.0
    print("✅ General Duty (2.5%)")

    # 2. Free Duty
    item2 = {
        "duties": {
            "general": "Free",
            "special": "Free",
            "other": None
        }
    }
    d2 = calculate_duty(item2, 1000.0, 1, "CN", [])
    assert d2 == 0.0
    print("✅ Free Duty")

    # 3. Special Preference Override (e.g. CA for Canada)
    item3 = {
        "duties": {
            "general": "6.5%",
            "special": "Free (CA, MX, AU)",
            "other": None
        }
    }
    # If Country is CA, should be 0 instead of $65
    d3 = calculate_duty(item3, 1000.0, 1, "CA", [])
    assert d3 == 0.0
    print("✅ Special Override (CA -> Free)")

    # 4. Special Preference Fail (Country not in list)
    # If Country is CN (China), should pay 6.5% ($65)
    d4 = calculate_duty(item3, 1000.0, 1, "CN", [])
    assert d4 == 65.0
    print("✅ Special Override Fail (CN -> General)")

    # 5. Chapter 99 (Section 301) Addition
    # 2.5% General ($25) + 25% Section 301 ($250) = $275
    ch99 = [{"type": "percent", "rate": 0.25}]
    d5 = calculate_duty(item1, 1000.0, 1, "CN", ch99)
    assert d5 == 275.0
    print("✅ Chapter 99 Addition (25%)")

    # 6. Specific Rate (cents/kg)
    # 1.9¢/kg. Value=$1000, Qty=100kg. Duty = 100 * 0.019 = 1.90
    item_spec = {
        "duties": {
            "general": "1.9¢/kg", 
            "special": "Free",
            "other": None
        }
    }
    d6 = calculate_duty(item_spec, 1000.0, 100, "CN", [])
    assert d6 == 1.90
    print("✅ Specific Rate (1.9¢/kg)")
    
    print("\nAll Tests Passed!")

if __name__ == "__main__":
    test_duty_calculation()
