# Configure Django settings for script execution outside of a Django project
# This enables the proper functioning of Django-related features, including database access via models

import os
import django
# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
# Configure Django settings
django.setup()

import requests
from datetime import datetime, timedelta
from lifeapi_apps.weather_app.models import Weather

def save_weather_to_db(date_str, desired_observation):
    # Save the weather data to the database
    weather = Weather(
        date=date_str,
        temperature=desired_observation.get("airTemperature", "")
    )
    weather.save()
    print(f"{date_str} and {desired_observation.get('airTemperature', '')} are saved to the database")

# Get the date. Write days=1 to get yesterdays date/weather
yesterday = datetime.now() - timedelta(days=0)
date_str = yesterday.strftime("%Y-%m-%d")

# Make the API request to fetch weather data
api_url = f"https://api.meteo.lt/v1/stations/vilniaus-ams/observations/{date_str}"
response = requests.get(api_url)
data_fetched_from_api = response.json()

# Retrieve desired observation from the fetched data
desired_observation = None
for observation in data_fetched_from_api["observations"]:
    # if you try to fetch data for 12:00 at 09:00 - it will fail, 
    # because 12:00 data is not yet present in the api
    if observation["observationTimeUtc"] == f"{date_str} 12:00:00":
        desired_observation = observation
        break

# Save the weather data to the database
save_weather_to_db(date_str, desired_observation)