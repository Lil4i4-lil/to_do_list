from django import forms
from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task  # Укажите модель
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(),
        }