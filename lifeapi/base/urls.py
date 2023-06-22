from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("quiz/questions/", views.questions, name="questions"),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/<int:question_id>/', views.quiz_question, name='quiz_question'),
    path('quiz/summary/', views.quiz_summary, name='quiz_summary'),
    path('add-question/', views.add_question, name='add_question'),
]
