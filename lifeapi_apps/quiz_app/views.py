from django.shortcuts import render, redirect
from .models import Question, Answer
from django.http import HttpResponse
from django.utils import timezone
from datetime import date
from django.contrib import messages
from .forms import QuestionForm
from django.db import transaction


def quiz_app_home(request):
    return render(request, 'quiz_app_home.html')


def quiz_question_list(request):
    '''View to display all the questions'''
    questions = Question.objects.all()
    context = {'questions': questions}
    return render(request, 'quiz_app_question_list.html', context)


def quiz_add_question(request):
    '''View to add a posibility to add new questions'''
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz_questions')
    else:
        form = QuestionForm()
    
    context = {'form': form}
    return render(request, 'quiz_app_add_question.html', context)


def quiz_start(request):
    '''View to add a posibility to add new questions'''
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
                context = {'question': first_question}
                
                return render(request, 'quiz_app_question.html', context)

        # Check if the user clicked the "Delete Answers" button
        elif 'delete_answers' in request.POST:
            today = date.today()
            Answer.objects.filter(date_added__date=today).delete()
            messages.success(request, "Your answers for today have been deleted.")

    # Retrieve any flash messages and pass them to the template context
    messages_to_display = messages.get_messages(request)
    context = {'messages': messages_to_display}

    return render(request, 'quiz_app_ready.html', context)


def quiz_question(request, question_id):
    if request.method == 'POST':
        question_id = int(request.POST.get('question_id'))
        answer_text = request.POST.get('answer')

        # Save the answer to the session
        request.session['answer_' + str(question_id)] = answer_text

        # Redirect to the next question or finish the quiz if all questions are answered
        next_question_id = question_id + 1
        if next_question_id > Question.objects.count():
            return redirect('quiz_summary')  # Redirect to the quiz summary page
        else:
            question = Question.objects.get(id=next_question_id)
            context = {'question': question}
            return render(request, 'quiz_app_question.html', context)

    # Retrieve the question based on the question_id
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'quiz_app_question.html', context)


def quiz_summary(request):
    '''View to display all entries of answers stored in the session'''
    answers = {}
    for question_id, question in Question.objects.all().values_list('id', 'description'):
        answer_key = 'answer_' + str(question_id)
        if answer_key in request.session:
            answer_text = request.session[answer_key]
            answers[question] = answer_text
    
    print(answers)
    # {'Workout': 'YES', 'Meditated': 'YES', 'Cold shower': 'YES', 'Sleep quality': '2', 'Mood in the morning': '2', 'Streched': 'YES', 'Rained today': 'YES', 'Work from home': 'YES', 'Master': 'YES', 'Sx': 'YES', 'Was pikc': 'YES', 'Mintys': 'ffff'}

    context = {'answers': answers}

    if request.method == 'POST':
        if 'store_answers' in request.POST:
            # Store answers in the database
            with transaction.atomic():
                for question_text, answer_text in answers.items():
                    question = Question.objects.get(description=question_text)
                    answer = Answer(question=question, answer=answer_text)
                    answer.save()
            
            # Clear session data
            request.session.clear()
            return redirect('data_table')

    return render(request, 'quiz_app_summary.html', context)