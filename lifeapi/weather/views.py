import requests
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Weather


def weather_view(request):
    # Get yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")

    # Make the API request to fetch weather data
    api_url = f"https://api.meteo.lt/v1/stations/vilniaus-ams/observations/{date_str}"
    response = requests.get(api_url)
    data_fetched_from_api = response.json()

    # Retrieve desired observation from the fetched data
    desired_observation = None
    for observation in data_fetched_from_api["observations"]:
        if observation["observationTimeUtc"] == f"{date_str} 12:00:00":
            desired_observation = observation
            break

    # Save the weather data to the database
    save_weather_to_db(date_str, desired_observation)

    # Retrieve the latest weather data from the database
    weather_from_db = retrieve_latest_weather()

    # Prepare the context to pass to the template
    context = {
        "observation": desired_observation,
        "weather_from_db": weather_from_db,
    }

    # Render the template with the context
    return render(request, "weather/weather_template.html", context)


def save_weather_to_db(date_str, desired_observation):
    # Save the weather data to the database
    weather = Weather(
        date=date_str,
        temperature=desired_observation.get("airTemperature", "")
    )
    weather.save()


def retrieve_latest_weather():
    # Retrieve the latest weather data from the database
    weather_from_db = Weather.objects.last()
    return weather_from_db
