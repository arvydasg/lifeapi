from django.shortcuts import render
from lifeapi_apps.weather_app.models import Weather
from lifeapi_apps.quiz_app.models import Question, Answer


def home(request):
    return render(request, 'home.html')


def data_table(request):
    questions = Question.objects.all()
    answers = Answer.objects.all()
    weather_entries = Weather.objects.all()

    context = {
        'questions': questions,
        "answers": answers,
        'weather_entries': weather_entries,
    }

    return render(request, 'data_table.html', context)