from django.shortcuts import render, redirect
from .models import Question, Answer
from lifeapi_apps.weather_app.models import Weather
from django.http import HttpResponse
from django.utils import timezone
from datetime import date
from django.contrib import messages
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required


def quiz_app_home(request):
    return render(request, 'quiz_app_home.html')


@login_required
def quiz_start(request):
    if request.method == 'POST':
        # Check if the user clicked the "Start Quiz" button
        if 'start_quiz' in request.POST:
            # Check if entries for today already exist
            today = date.today()
            if Answer.objects.filter(date_added__date=today).exists():
                messages.warning(request, "You have already answered the quiz for today.")
            else:
                # Retrieve the first question from the database
                first_question = Question.objects.first()

                context = {
                    'question': first_question
                }
                
                return render(request, 'quiz_app_question.html', context)

        # Check if the user clicked the "Delete Answers" button
        elif 'delete_answers' in request.POST:
            today = date.today()
            Answer.objects.filter(date_added__date=today).delete()
            messages.success(request, "Your answers for today have been deleted.")

    # Retrieve any flash messages and pass them to the template context
    messages_to_display = messages.get_messages(request)

    context = {
        'messages': messages_to_display
        }

    # this is the default view we get when there are no post requests are passed to this view
    return render(request, 'quiz_app_ready.html', context)


@login_required
def quiz_question(request, question_id):
    if request.method == 'POST':
        question_id = int(request.POST.get('question_id'))
        answer_text = request.POST.get('answer')

        # Get the currently logged-in user
        user = request.user

        # Save the answer to the database
        answer = Answer(question_id=question_id, answer=answer_text, created_by=user)
        answer.save()

        # use queryset filtering to find the next question with an id greater than the current question_id. 
        # We then use order_by('id').first() to retrieve the first question that matches the filter. 
        # If a next question is found, it is rendered on the template.
        try:
            next_question = Question.objects.filter(id__gt=question_id).order_by('id').first()
            if next_question:
                return render(request, 'quiz_app_question.html', {'question': next_question})
            else:
                return redirect('quiz_summary')  # Redirect to the quiz summary page
        except Question.DoesNotExist:
            return redirect('quiz_summary')  # Redirect to the quiz summary page

    # Retrieve the question based on the question_id
    question = Question.objects.get(id=question_id)

    context = {
        'question': question
        }

    return render(request, 'quiz_app_question.html', context)


@login_required
def quiz_summary(request):
    '''View to display all entries of answers table'''
    answers = Answer.objects.all()
    context = {'answers': answers}
    return render(request, 'quiz_app_summary.html', context)


@login_required
def data_table(request):
    answers = Answer.objects.all()
    questions = Question.objects.all()
    weather_entries = Weather.objects.all()

    # Separate the questions based on their types
    yn_questions = questions.filter(type='YN').prefetch_related('answer_set')
    scale_questions = questions.filter(type='Scale').prefetch_related('answer_set')
    text_questions = questions.filter(type='Text').prefetch_related('answer_set')

    context = {
        'yn_questions': yn_questions,
        'scale_questions': scale_questions,
        'text_questions': text_questions,
        'weather_entries': weather_entries,
        'answers': answers,
    }

    return render(request, 'data_table.html', context)


@login_required
def journal(request):
    journal_question = Question.objects.get(description="Journal")
    answers = journal_question.answer_set.all()

    context = {
        'question': journal_question,
        'answers': answers,
    }

    return render(request, 'journal.html', context)


@login_required
def learn(request):
    learn = Question.objects.get(description="Learn")
    answers = learn.answer_set.all()

    context = {
        'learn': learn,
        'answers': answers,
    }

    return render(request, 'learn.html', context)