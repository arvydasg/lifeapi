import requests
import django
import os

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
# Configure Django settings
django.setup()

# Your RescueTime API key
api_key_ag = os.getenv("RESCUETIME_API_KEY_AG")
api_key_js = os.getenv("RESCUETIME_API_KEY_JS")

# Define the API endpoint URL
api_url = f"https://www.rescuetime.com/anapi/daily_summary_feed?key={api_key_ag}"

# Make the API request
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    
    # Define the date you want to filter for
    target_date = "2023-10-14"
    
    # Filter the data for the specific date
    # here we get a big json file, so this list comperhension takes what we need
    filtered_data = [entry for entry in data if entry['date'] == target_date] # list comprehension
    
    if filtered_data:
        # Process the filtered data as needed
        for entry in filtered_data:
            print(f"Date: {entry['date']}") # we're accessing the 'date' key in the dictionary called 'entry'
            print(f"Total hours: {entry['total_hours']}")
            print(f"All productive hours: {entry['all_productive_hours']}")
            print(f"All distracting hours: {entry['all_distracting_hours']}")
    else:
        print(f"No data found for {target_date}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
