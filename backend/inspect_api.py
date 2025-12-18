import requests
import json
import os

def fetch_and_save():
    url = "https://hts.usitc.gov/reststop/search?keyword=laptop"
    print(f"Fetching data from {url}...")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = data if isinstance(data, list) else data.get('results', [])
        
        output_lines = []
        output_lines.append(f"Source URL: {url}")
        output_lines.append(f"Total Results: {len(results)}")
        output_lines.append("-" * 40)
        
        if results:
            # Pick the first result that looks like a stat line (indent 0 or deep)
            # Actually just show the first result for now
            item = results[0]
            output_lines.append("FIRST RESULT DETAIL:\n")
            
            def format_node(node, indent=0):
                lines = []
                spacing = "  " * indent
                if isinstance(node, dict):
                    for k, v in node.items():
                        if isinstance(v, (dict, list)):
                            lines.append(f"{spacing}{k}:")
                            lines.extend(format_node(v, indent + 1))
                        else:
                            val_str = str(v) if v is not None else "null"
                            lines.append(f"{spacing}{k}: {val_str}")
                elif isinstance(node, list):
                    for i, v in enumerate(node):
                        if isinstance(v, (dict, list)):
                            lines.append(f"{spacing}- [{i}]:")
                            lines.extend(format_node(v, indent + 1))
                        else:
                            val_str = str(v) if v is not None else "null"
                            lines.append(f"{spacing}- {val_str}")
                else:
                    lines.append(f"{spacing}{node}")
                return lines

            output_lines.extend(format_node(item))
        else:
            output_lines.append("No results found.")
            
        # Write to file
        file_path = os.path.join(os.path.dirname(__file__), 'api_response.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
            
        print(f"Saved formatted output to {file_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_save()
