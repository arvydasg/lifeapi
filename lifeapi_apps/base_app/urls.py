from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('website-fixes/', views.website_fixes, name='website_fixes'),
    path('website-fixes/<int:fix_id>/edit/', views.edit_website_fix, name='edit_website_fix'),
    path('website-fixes/<int:fix_id>/delete/', views.delete_website_fix, name='delete_website_fix'),
]