import requests
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def weather_view(request):
    # Make the API request
    response = requests.get(
        "https://api.meteo.lt/v1/stations/vilniaus-ams/observations/2023-06-19"
    )
    data = response.json()

    # Find the desired observation
    desired_observation = next(
        (
            obs
            for obs in data["observations"]
            if obs["observationTimeUtc"] == "2023-06-19 12:00:00"
        ),
        None,
    )

    context = {
        "observation": desired_observation,
    }

    return render(request, "weather/weather_template.html", context)
