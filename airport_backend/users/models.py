from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    telegram_id = models.BigIntegerField(unique=True, null=False)
    location = models.JSONField(
        null=False)  # Координаты (широта и долгота)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.username
