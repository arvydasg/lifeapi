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
            if Answer.objects.filter(date_added__date=today, created_by=request.user).exists():
                messages.warning(request, "You have already answered the quiz for today.")
            else:
                # Retrieve the first question from the database
                first_question = Question.objects.filter(created_by=request.user).first()

                context = {
                    'question': first_question
                }
                
                return render(request, 'quiz_app_question.html', context)

        # Check if the user clicked the "Delete Answers" button
        elif 'delete_answers' in request.POST:
            today = date.today()
            Answer.objects.filter(date_added__date=today, created_by=request.user).delete()
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
            next_question = Question.objects.filter(id__gt=question_id, created_by=request.user).order_by('id').first()
            if next_question:
                return render(request, 'quiz_app_question.html', {'question': next_question})
            else:
                return redirect('data_table')
        except Question.DoesNotExist:
            return redirect('data_table')

    # Retrieve the question based on the question_id
    question = Question.objects.get(id=question_id)

    context = {
        'question': question
        }

    return render(request, 'quiz_app_question.html', context)


@login_required
def data_table(request):
    answers = Answer.objects.filter(created_by=request.user)
    questions = Question.objects.filter(created_by=request.user)
    weather_entries = Weather.objects.all()

    data_to_display = []

    for weather_entry in weather_entries:
        matching_answers = []

        for question in questions:
            corresponding_answer = question.answer_set.filter(date_added__date=weather_entry.date).first()
            if corresponding_answer:
                matching_answers.append({
                    'description': question.description,
                    'answer': corresponding_answer.answer,
                })

        if matching_answers:
            data_to_display.append({
                'date': weather_entry.date,
                'temperature': weather_entry.temperature,
                'answers': matching_answers,
            })

    context = {
        'user': request.user,
        'answers': Answer.objects.filter(created_by=request.user),
        'data_to_display': data_to_display,
        'questions': questions,
    }

    print(data_to_display)


    return render(request, 'data_table.html', context)


# in base.html the link to this view is visible only for the members of the data_table_test group
# it would be nice to make it not ACCESSIBLE to those that are not members of data_table_test
# but could not make it work
@login_required
def data_table_test(request):
    answers = Answer.objects.filter(created_by=request.user)
    questions = Question.objects.filter(created_by=request.user)
    weather_entries = Weather.objects.all()

    data_to_display = []

    for weather_entry in weather_entries:
        matching_answers = []

        for question in questions:
            corresponding_answer = question.answer_set.filter(date_added__date=weather_entry.date).first()
            if corresponding_answer:
                matching_answers.append({
                    'description': question.description,
                    'answer': corresponding_answer.answer,
                })
            else:
            # If there's no corresponding answer, add an empty answer
                matching_answers.append({
                'description': question.description,
                'answer': '',
            })

        if matching_answers:
            data_to_display.append({
                'date': weather_entry.date,
                'temperature': weather_entry.temperature,
                'answers': matching_answers,
            })

    context = {
        'user': request.user,
        'answers': Answer.objects.filter(created_by=request.user),
        'data_to_display': data_to_display,
        'questions': questions,
    }

    print(data_to_display)

    return render(request, 'data_table_test.html', context)


@login_required
def user_questions(request):
    # Retrieve all questions created by the currently logged-in user
    user_questions = Question.objects.filter(created_by=request.user)

    context = {
        'user_questions': user_questions,
    }

    return render(request, 'user_questions.html', context)


@login_required
def add_question(request):
    if request.method == 'POST':
        # Retrieve question details from the form submission
        description = request.POST.get('description')

        # Create a new question
        new_question = Question(description=description, created_by=request.user)
        new_question.save()

        return redirect('user_questions')  # Redirect to the home page after adding the question

    return render(request, 'add_question.html')


@login_required
def edit_question(request, question_id):
    try:
        # Retrieve the question based on the provided question_id
        question = Question.objects.get(id=question_id)

        # Check if the logged-in user is the creator of the question
        if question.created_by == request.user:
            if request.method == 'POST':
                # Update the question details based on the form submission
                question.description = request.POST.get('description')
                question.save()

                return redirect('user_questions')  # Redirect to the list of user questions

            context = {
                'question': question,
            }

            return render(request, 'edit_question.html', context)

    except Question.DoesNotExist:
        pass  # Handle the case where the question doesn't exist or is not owned by the user

    # Redirect to the list of user questions if the user doesn't have permission to edit
    return redirect('list_user_questions')


@login_required
def delete_question(request, question_id):
    try:
        # Retrieve the question based on the provided question_id
        question = Question.objects.get(id=question_id)

        # Check if the logged-in user is the creator of the question
        if question.created_by == request.user:
            # Delete the question
            question.delete()

    except Question.DoesNotExist:
        pass  # Handle the case where the question doesn't exist or is not owned by the user

    # Redirect to the list of user questions after deleting or in case of any issues
    return redirect('user_questions')