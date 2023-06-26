from django.shortcuts import render
from .models import Weather

def weather_app_home(request):
    return render(request, 'weather_app_home.html')


def weather_app_display_from_db(request):
    # Retrieve the latest weather data from the database
    weather_from_db = retrieve_latest_weather()

    # Prepare the context to pass to the template
    context = {
        "weather_from_db": weather_from_db,
    }

    # Render the template with the context
    return render(request, "weather_template.html", context)

def retrieve_latest_weather():
    # Retrieve the latest weather data from the database
    weather_from_db = Weather.objects.last()
    return weather_from_db