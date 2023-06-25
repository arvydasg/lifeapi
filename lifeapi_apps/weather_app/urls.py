from django.urls import path
from . import views

urlpatterns = [
    path("", views.weather_app_home, name="weather_app_home"),
    path("fetch/", views.weather_app_display_from_db, name="weather_app_display_from_db")
]