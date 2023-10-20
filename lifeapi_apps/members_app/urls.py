from django.urls import path
from . import views

urlpatterns = [
    path("login_user", views.members_login_user, name="members_login_user"),
    path("logout_user", views.members_logout_user, name="members_logout_user"),
    path("register_user", views.members_register_user, name="members_register_user"),
    path("dashboard", views.members_dashboard, name="members_dashboard"), 
]