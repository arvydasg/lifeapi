from django.urls import path
from . import views

urlpatterns = [
    path("", views.quiz_app_home, name="quiz_app_home"),
]