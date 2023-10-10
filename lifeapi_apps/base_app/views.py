from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def apps(request):
    return render(request, 'apps.html')