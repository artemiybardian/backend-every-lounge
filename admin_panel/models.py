from django.db import models
from airport_backend.settings import AUTH_USER_MODEL


class AdminActionLog(models.Model):
    admin_user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Администратор"
    )
    action = models.TextField(verbose_name="Описание действия")
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Время действия")

    def __str__(self):
        return f"Действие админа {self.admin_user.username} - {self.action}"

    class Meta:
        verbose_name = "Лог действий администратора"
        verbose_name_plural = "Логи действий администраторов"
