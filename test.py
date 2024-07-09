import json
import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'llm.settings')

# Initialize Django
django.setup()

# Import Django models
from crm.models import UserProfile

def process_json_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Process each entry in the JSON data
    for entry in data:
        if entry.get('model') == 'llama.Company':  # Adjust as per your actual models
            fields = entry.get('fields', {})
            # Set supplier_account_manager_id to null if not provided
            if 'supplier_account_manager_id' not in fields:
                fields['supplier_account_manager_id'] = None

    # Write the modified JSON data back to the file
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Processed {json_file} to set 'supplier_account_manager_id' to null where not provided.")

def load_data(json_file):
    # Load data using manage.py loaddata command
    os.system(f"python manage.py loaddata {json_file}")

if __name__ == "__main__":
    json_file_path = 'company_data.json'  # Replace with your JSON file path

    # Preprocess JSON data to set 'supplier_account_manager_id' to null where not provided
    process_json_data(json_file_path)

    # Proceed to load data
    load_data(json_file_path)
