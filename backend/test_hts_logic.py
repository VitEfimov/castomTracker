from services import get_hts_tree, fetch_hts_codes
import json

def test_tree():
    print("Testing Tree Generation...")
    tree = get_hts_tree()
    print(f"Root nodes count: {len(tree)}")
    
    # Check hierarchy
    # Expect 8471 to be a root, and have children
    found_laptop_root = False
    for node in tree:
        if node['hts_code'] == '8471':
            found_laptop_root = True
            print("Found Root 8471")
            if len(node['children']) > 0:
                print(f"  Root has {len(node['children'])} children.")
                child = node['children'][0]
                print(f"  Child: {child['hts_code']}")
                if len(child['children']) > 0:
                    print(f"    Grandchild: {child['children'][0]['hts_code']}")
            else:
                print("  ERROR: Root 8471 has no children")
                
    if not found_laptop_root:
        print("ERROR: Did not find root 8471")

    # Check for correct nesting of 8703 -> 8703.23.01.00
    # In my data, 8703 is root. 8703.23.01.00 has parent 8703.
    # So 8703 should have direct child 8703.23.01.00
    found_car_root = False
    for node in tree:
        if node['hts_code'] == '8703':
            found_car_root = True
            print("Found Root 8703")
            if len(node['children']) > 0:
                print(f"  Root has {len(node['children'])} children.")
                print(f"  Child HTS: {node['children'][0]['hts_code']}")
            else:
                print("  ERROR: Root 8703 has no children")

def test_search():
    print("\nTesting Search...")
    # Search for "Laptop" - should hit description
    results = fetch_hts_codes("Laptop")
    print(f"Search 'Laptop' found {len(results)} results")
    if len(results) > 0:
        print(f"  Top Match: {results[0]['hts_code']} - {results[0]['description']} (Score: {results[0]['score']})")
        
    # Search for "Motor car"
    results = fetch_hts_codes("Motor car")
    print(f"Search 'Motor car' found {len(results)} results")
    if len(results) > 0:
        print(f"  Top Match: {results[0]['hts_code']} - {results[0]['description']}")

if __name__ == "__main__":
    test_tree()
    test_search()
