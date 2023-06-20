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
    desired_observation = next(
        (
            obs
            for obs in data["observations"]
            if obs["observationTimeUtc"] == f"{date_str} 12:00:00"
        ),
        None,
    )

    # assign the desired_observation to context
    context = {
        "observation": desired_observation,
    }

    # pass that context to the template and render it
    return render(request, "weather/weather_template.html", context)
