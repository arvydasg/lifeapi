from django.urls import path
from . import views

urlpatterns = [
    path("", views.members_app_home, name="members_app_home"),
]