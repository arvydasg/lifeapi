import requests
import django
import os
from datetime import datetime, timedelta

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
# Configure Django settings
django.setup()

# Your RescueTime API key
api_key_ag = os.getenv("RESCUETIME_API_KEY_AG")
api_key_js = os.getenv("RESCUETIME_API_KEY_JS")

# Pick yesterday's date
yesterday_full = datetime.now() - timedelta(days=1)
yesterday_formatted = yesterday_full.strftime("%Y-%m-%d")


def fetch_for_user(api_key, yesterday_formatted):
    # Define the API endpoint URL
    api_url = f"https://www.rescuetime.com/anapi/daily_summary_feed?key={api_key}"

    # Make the API request
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        
        # Filter the data for the specific date
        # here we get a big json file, so this list comperhension takes what we need
        filtered_data = [entry for entry in data if entry['date'] == yesterday_formatted] # list comprehension
        
        if filtered_data:
            # Process the filtered data as needed
            for entry in filtered_data:
                chosen_date = f"Date: {entry['date']}" # we're accessing the 'date' key in the dictionary called 'entry'
                total_hours = f"Total hours: {entry['total_hours']}"
                productive_hours = f"All productive hours: {entry['all_productive_hours']}"
                distracting_hours = f"All distracting hours: {entry['all_distracting_hours']}"

                print(chosen_date) 
                print(total_hours)
                print(productive_hours)
                print(distracting_hours)
 
        else:
            print(f"No data found for {yesterday_formatted}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

fetch_for_user(api_key_ag, yesterday_formatted)
fetch_for_user(api_key_js, yesterday_formatted)