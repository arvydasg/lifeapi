from django.shortcuts import render

def weather_app_home(request):
    return render(request, 'weather_app_home.html')