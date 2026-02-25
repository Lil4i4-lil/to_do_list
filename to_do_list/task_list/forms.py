from django import forms
from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task  # Укажите модель
        fields = ['title', 'content', 'tags']
        widgets = {
            'content': forms.Textarea(),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            title = title[:200]
        return title