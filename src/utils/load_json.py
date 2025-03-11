import json

def load_json(filepath):
    """Opens a JSON file, ensures it's properly formatted, and returns its content."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)  # Load JSON data
        
        return json.dumps(data)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading JSON: {e}")
        return None