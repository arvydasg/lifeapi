from django import forms
from .models import WebsiteFix

class WebsiteFixForm(forms.ModelForm):
    class Meta:
        model = WebsiteFix
        fields = ['title', 'description', 'tags', 'status']


class ViewFixesForm(forms.Form):
    CHOICES = (
        ('all', 'All Fixes'),
        ('user', 'My Fixes'),
    )
    view_option = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)