from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True, null=True, blank=True) # username в telegram
    telegram_id = models.BigIntegerField(unique=True, null=False)
    location = models.JSONField(
        null=False)  # Координаты (широта и долгота)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.username or str(self.telegram_id)
