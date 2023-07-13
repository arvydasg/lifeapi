from django.shortcuts import render
from lifeapi_apps.weather_app.models import Weather
from lifeapi_apps.quiz_app.models import Question, Answer


def home(request):
    return render(request, 'home.html')


def data_table(request):
    questions = Question.objects.all()
    answers = Answer.objects.all()
    weather_entries = Weather.objects.all()

    # Separate the questions based on their types
    yn_questions = questions.filter(type='YN')
    scale_questions = questions.filter(type='Scale')
    text_questions = questions.filter(type='Text')

    context = {
        'yn_questions': yn_questions,
        'scale_questions': scale_questions,
        'text_questions': text_questions,

        "answers": answers,
        'weather_entries': weather_entries,
    }

    return render(request, 'data_table.html', context)