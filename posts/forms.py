from django import forms
from .models import StatusPost

class StatusPostForm(forms.ModelForm):
    class Meta:
        model = StatusPost
        fields = ['title', 'content']