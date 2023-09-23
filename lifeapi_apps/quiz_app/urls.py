from django.urls import path
from . import views

urlpatterns = [
    path("", views.quiz_app_home, name="quiz_app_home"),
    path('start_quiz/', views.quiz_start, name='quiz_start'),
    path('quiz/<int:question_id>/', views.quiz_question, name='quiz_question'),
    path("data_table/", views.data_table, name="data_table"),
    path("data_table_test/", views.data_table_test, name="data_table_test"),
    path('add_question/', views.add_question, name='add_question'),
    path('user_questions/', views.user_questions, name='user_questions'),
    path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
]