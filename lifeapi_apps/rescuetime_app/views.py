import requests
from dotenv import load_dotenv
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os

load_dotenv()

def rescuetime_app_home(request):
    return render(request, 'rescuetime_app_home.html')


@login_required
def rescuetime_app_dsf(request):
    # take the api key from environment variables
    rescuetime_api_key_ag = os.getenv("RESCUETIME_API_KEY_AG")

    # Define the URL
    url = f'https://www.rescuetime.com/anapi/daily_summary_feed?key={rescuetime_api_key_ag}'
    url2 = f'https://www.rescuetime.com/anapi/data?key={rescuetime_api_key_ag}&perspective=rank&restrict_kind=overview&restrict_begin=2023-10-10&restrict_end=2023-10-10&format=json'

    try:
        # Make an HTTP GET request to the URL
        response = requests.get(url)
        response2 = requests.get(url2)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            data2 = response2.json()

            # Pass the data to the template for rendering

            context = {
                'data': data,
                'data2': data2
            }
            
            return render(request, 'rescuetime_app_dsf.html', context)
        else:
            # Handle any other status code (e.g., display an error)
            return render(request, 'rescuetime_app_error.html', {'error_message': 'Failed to fetch data'})
    except Exception as e:
        # Handle any exceptions (e.g., network issues, JSON parsing errors)
        return render(request, 'rescuetime_app_error.html', {'error_message': str(e)})
