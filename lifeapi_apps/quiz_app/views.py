from django.shortcuts import render, redirect
from .models import Question, Answer
from django.http import HttpResponse
from django.utils import timezone
from datetime import date
from django.contrib import messages
from .forms import QuestionForm


def quiz_app_home(request):
    return render(request, 'quiz_app_home.html')


def quiz_questions(request):
    '''View to display all the questions'''
    questions = Question.objects.all()
    context = {'questions': questions}
    return render(request, 'quiz_app_questions.html', context)


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

        # Save the answer to the database
        answer = Answer(question_id=question_id, answer=answer_text)
        answer.save()

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
    '''View to display all entries of answers table'''
    answers = Answer.objects.all()
    context = {'answers': answers}
    return render(request, 'quiz_app_summary.html', context)