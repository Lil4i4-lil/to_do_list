from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    completed = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return self.title