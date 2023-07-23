from django.shortcuts import render

# Create your views here.

def members_app_home(request):
    return render(request, 'members/members_app_home.html')