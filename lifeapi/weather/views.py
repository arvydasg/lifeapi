import requests
from django.shortcuts import render
from datetime import datetime, timedelta


# Create your views here.
def weather_view(request):
    # Get yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")

    # Make the API request
    response = requests.get(
        f"https://api.meteo.lt/v1/stations/vilniaus-ams/observations/{date_str}"
    )
    data = response.json()

    # Find the desired observation
    desired_observation = None
    for x in data["observations"]:
        if x["observationTimeUtc"] == f"{date_str} 12:00:00":
            desired_observation = x
            break

    # # assign the desired_observation to context
    context = {
        "observation": desired_observation,
    }

    # Store only the needed values in the database
    from .models import Weather

    weather = Weather(
        date=date_str, temperature=desired_observation.get("airTemperature", "")
    )
    weather.save()

    # pass that context to the template and render it
    return render(request, "weather/weather_template.html", context)
