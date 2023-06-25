from django.shortcuts import render

def weather(request):
    return render(request, 'weather__index.html')