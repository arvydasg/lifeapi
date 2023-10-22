import requests
import django
import os
from datetime import datetime, timedelta

# appending the path of the project's root directory to sys.path, 
# ensuring that Python can locate the settings module when you run the script from a different directory.
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")
# Configure Django settings
django.setup()

from django.contrib.auth.models import User
from lifeapi_apps.members_app.models import Profile
from lifeapi_apps.rescuetime_app.models import Rescuetime

# Pick yesterday's date
yesterday_full = datetime.now() - timedelta(days=1)
yesterday_formatted = yesterday_full.strftime("%Y-%m-%d")


def fetch_from_api(rescuetime_api_key, yesterday_formatted):
    """
    A function that simply does a call to the api with the provided api key.
    Api key is gotten from when "fetch_for_all_users" function is used, which has 
    the user information from User django model. It returns productive and distracting
    hours, which later are used in "save_to_db" function.
    """

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
                productive_hours = entry['all_productive_hours']
                distracting_hours = entry['all_distracting_hours']

                return productive_hours, distracting_hours
 
        else:
            print(f"No data found for {yesterday_formatted}")
            return None
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


def save_to_db(date_str, user, productive_hours, distracting_hours):
    """
    A function responsible for saving received data to the DB. We get data from the above,
    productivity/distracting hours - from "fetch_from_api) function, user - when doing a for loop
    over users in "fetch_fro_all_users" function.

    """
    rescuetime_entry = Rescuetime(
        date=date_str,
        productive_hours = productive_hours,
        distracting_hours = distracting_hours,
        user = user,
    )
    rescuetime_entry.save()


def fetch_for_all_users():
    """
    Function that loops over all users, getting profile information of each user(api key as well),
    for "fetch_from_api" function, and user for "save_to_db" function.
    """

    users = User.objects.all()

    for user in users:
        try:
            profile = Profile.objects.get(user=user)
            productive_hours, distracting_hours = fetch_from_api(profile.rescuetime_api_key, yesterday_formatted)
            save_to_db(yesterday_formatted, user, productive_hours, distracting_hours)
            print(f"{yesterday_formatted} - fetch and save for {user} is successful! Productive time: {productive_hours}, distracting time: {distracting_hours}.")
        except Profile.DoesNotExist:
            # basically if user does not have "rescuetime_api_key" entry assigned
            print(f"Profile for {user} does not exist.")
            return None

fetch_for_all_users()