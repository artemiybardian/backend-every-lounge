from django.db import models
from airport_backend.settings import AUTH_USER_MODEL


class AdminActionLog(models.Model):
    admin_user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.TextField()  # Описание действия
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Action by {self.admin_user.username} - {self.action}"
