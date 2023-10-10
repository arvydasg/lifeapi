from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("apps/", views.apps, name="apps"),

]