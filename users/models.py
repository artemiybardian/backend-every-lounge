from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True, null=True, blank=True, verbose_name="Username в Telegram"
    )
    telegram_id = models.BigIntegerField(
        unique=True, null=False, verbose_name="ID пользователя в Telegram")
    location = models.JSONField(
        null=False, verbose_name="Координаты (широта и долгота)")
    first_name = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="Фамилия")

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
