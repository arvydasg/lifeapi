from django.urls import path
from . import views

urlpatterns = [
    path("", views.rescuetime_app_home, name="rescuetime_app_home"),
    path("dsf", views.rescuetime_app_dsf, name="rescuetime_app_dsf"),
]