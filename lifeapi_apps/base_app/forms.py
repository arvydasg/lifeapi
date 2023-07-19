from django import forms
from .models import WebsiteFix

class WebsiteFixForm(forms.ModelForm):
    class Meta:
        model = WebsiteFix
        fields = ['title', 'description']
