from django.urls import path
from . import views

urlpatterns = [
    path("", views.quiz_app_home, name="quiz_app_home"),
    path('start_quiz/', views.quiz_start, name='quiz_start'),
    path('quiz/<int:question_id>/', views.quiz_question, name='quiz_question'),
    path("data_table/", views.data_table, name="data_table"),
    path("journal/", views.journal, name="journal"),
    path("learn/", views.learn, name="learn"),
    path('add_question/', views.add_question, name='add_question'),
]