from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    title = forms.CharField(max_length=200, required=True, label="Задача")
    content = forms.CharField(widget=forms.Textarea, required=False, label="Пояснения к задаче")

    class Meta:
        model = Task  # Укажите модель
        fields = ['title', 'content']