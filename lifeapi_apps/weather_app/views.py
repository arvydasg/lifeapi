from django.shortcuts import render
from .models import Weather
from django.contrib.auth.decorators import login_required


def weather_app_home(request):
    return render(request, 'weather_app_home.html')


@login_required
def weather_app_display_from_db(request):
    weather_from_db = Weather.objects.last()
    context = {
        "weather_from_db": weather_from_db,
    }
    return render(request, "weather_template.html", context)