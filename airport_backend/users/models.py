from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True, null=True, blank=True)  # username в Telegram
    telegram_id = models.BigIntegerField(unique=True, null=False)
    location = models.JSONField(null=False)  # Координаты (широта и долгота)
    first_name = models.CharField(max_length=30, null=True, blank=True)  # Имя
    last_name = models.CharField(
        max_length=30, null=True, blank=True)    # Фамилия

    def __str__(self):
        # Проверка на наличие имени и фамилии
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
