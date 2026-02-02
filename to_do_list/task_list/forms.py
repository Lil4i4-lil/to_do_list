from django import forms


class TaskForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label="Задача")
    content = forms.CharField(widget=forms.Textarea, required=False, label="Пояснения к задаче")