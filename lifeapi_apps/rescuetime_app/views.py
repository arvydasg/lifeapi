from django.shortcuts import render

def rescuetime_app_home(request):
    return render(request, 'rescuetime_app_home.html')