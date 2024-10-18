from django import forms
from .models import Story, Category

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'description', 'image', 'category']