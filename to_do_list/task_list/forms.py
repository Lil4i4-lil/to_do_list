from django import forms

from .models import Tag, Task


class TaskForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите теги через запятую'
        }),
        label='Теги'
    )

    class Meta:
        model = Task  # Укажите модель
        fields = ('title', 'content', 'tags')
        widgets = { # noqa: RUF012
            'content': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['tags'] = ', '.join(
                [tag.tag for tag in self.instance.tags.all()]
            )

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            title = title[:200]
        return title

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        tags_input = self.cleaned_data.get('tags', '')
        if tags_input:
            tag_names = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            tags = []
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(tag=tag_name)
                tags.append(tag)
            instance.tags.set(tags)
        else:
            instance.tags.clear()

        return instance
