"""
URL configuration for lifeapi_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("lifeapi_apps.base_app.urls")),
    path("weather/", include("lifeapi_apps.weather_app.urls")),
    path("quiz/", include("lifeapi_apps.quiz_app.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("members/", include('django.contrib.auth.urls')),
    path("members/", include("lifeapi_apps.members_app.urls")),
    # path("website_fixes/", include("lifeapi_apps.website_fixes_app.urls")),
    path("rescuetime/", include("lifeapi_apps.rescuetime_app.urls")),
]
