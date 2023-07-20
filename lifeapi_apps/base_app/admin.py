from django.contrib import admin
from .models import WebsiteFix, WebsiteFixTag

# Register your models here.

admin.site.register(WebsiteFix)
admin.site.register(WebsiteFixTag)