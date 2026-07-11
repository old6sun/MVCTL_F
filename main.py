import json
from analyzer import analyze_multiple_ap_properties

if __name__ == "__main__":

    file_path = "test.json"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            full_data = json.load(f)
        print(f"[*] Successfully loaded data, read {len(full_data)} trace records. Starting temporal property verification...\n")
    except FileNotFoundError:
        print(f"\n[!] Error: File '{file_path}' not found, please ensure it is in the same directory.")
        full_data = []
    except json.JSONDecodeError:
        print(f"\n[!] Error: File '{file_path}' has incorrect format, cannot be parsed as JSON.")
        full_data = []

    if full_data:
        final_stats = analyze_multiple_ap_properties(full_data)
