import requests
import django
import os
from datetime import datetime, timedelta

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
# Configure Django settings
django.setup()

from django.contrib.auth.models import User
from lifeapi_apps.members_app.models import Profile

# Pick yesterday's date
yesterday_full = datetime.now() - timedelta(days=1)
yesterday_formatted = yesterday_full.strftime("%Y-%m-%d")

def fetch_from_api(rescuetime_api_key, yesterday_formatted):
    # Define the API endpoint URL
    api_url = f"https://www.rescuetime.com/anapi/daily_summary_feed?key={rescuetime_api_key}"

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
                total_hours = f"Total hours: {entry['total_duration_formatted']}"
                productive_hours = f"All productive hours: {entry['all_productive_duration_formatted']}"
                distracting_hours = f"All distracting hours: {entry['all_distracting_duration_formatted']}"
                uncategorized_hours = f"All uncategorized hours: {entry['uncategorized_duration_formatted']}"

                print(chosen_date) 
                print(total_hours)
                print(productive_hours)
                print(distracting_hours)
                print(uncategorized_hours)
                print("-----------------------------------------")
 
        else:
            print(f"No data found for {yesterday_formatted}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

def fetch_for_all_users():
    users = User.objects.all()

    for user in users:
        try:
            profile = Profile.objects.get(user=user)  # Get the user's profile
            print(f"Username: {user.username}")
            print(f"RescueTime API Key: {profile.rescuetime_api_key}")
            fetch_from_api(profile.rescuetime_api_key, yesterday_formatted)
        except Profile.DoesNotExist:
            # basically if user does not have "rescuetime_api_key" entry assigned
            print(f"Username: {user.username}")
            print("No profile found for this user.")

fetch_for_all_users()