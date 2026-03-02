from django.conf import settings
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Задача")
    content = models.TextField(null=True, blank=True, verbose_name="Пояснение к задаче")
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    completed = models.BooleanField(default=False, null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, default=3,
                               related_name='tasks')
    tags = models.ManyToManyField('Tag', verbose_name="Теги", blank=True,
                                  help_text='Удерживайте Ctrl для выбора нескольких вариантов')

    def __str__(self):
        return self.title


class Tag(models.Model):
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.tag