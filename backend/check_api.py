import requests
import json

try:
    url = "https://hts.usitc.gov/reststop/search?keyword=car"
    print(f"Fetching {url}...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Type: {type(data)}")
    
    if isinstance(data, list) and len(data) > 0:
        print("First Item Keys:", data[0].keys())
        print("First Item Sample:", json.dumps(data[0], indent=2))
    elif isinstance(data, dict):
        print("Keys:", data.keys())
        if 'results' in data and len(data['results']) > 0:
             print("First Result:", json.dumps(data['results'][0], indent=2))
        else:
            print("Dict Sample:", json.dumps(data, indent=2))
    else:
        print("Empty or unexpected data")

except Exception as e:
    print(f"Error: {e}")
