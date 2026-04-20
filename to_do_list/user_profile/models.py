from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    phone_number = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        verbose_name='Номер телефона'
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name='День рождения'
    )
    tg = models.CharField(
        null=True,
        blank=True,
        verbose_name='Имя пользователя в Telegram'
    )
    tg_notifications = models.BooleanField(
        null=False,
        default=False
    )
