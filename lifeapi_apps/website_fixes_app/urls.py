from django.urls import path
from . import views

urlpatterns = [
    path("", views.website_fixes_app_home, name="website_fixes_app_home"),
    path('all-fixes/', views.website_fixes, name='website_fixes'),
    path('website-fixes/add', views.add_website_fix, name='add_website_fix'),
    path('website-fixes/<int:fix_id>/edit/', views.edit_website_fix, name='edit_website_fix'),
    path('website-fixes/<int:fix_id>/delete/', views.delete_website_fix, name='delete_website_fix'),
    path('website-fixes/<int:fix_id>/preview/', views.preview_website_fix, name='preview_website_fix'),
]