from django.shortcuts import render

def quiz_app_home(request):
    return render(request, 'quiz_app_home.html')