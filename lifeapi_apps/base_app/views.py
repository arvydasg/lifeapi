from django.shortcuts import render
from lifeapi_apps.weather_app.models import Weather
from lifeapi_apps.quiz_app.models import Question, Answer


def home(request):
    return render(request, 'home.html')


def data_table(request):
    # Retrieve all questions
    questions = Question.objects.all()

    # Retrieve all answers
    answers = Answer.objects.all()

    # Retrieve all weather entries
    weather_entries = Weather.objects.all()

    # Pass the data to the template
    context = {
        'questions': questions,
        "answers": answers,
        'weather_entries': weather_entries,
    }

    return render(request, 'data_table.html', context)