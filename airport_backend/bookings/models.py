from django.db import models
from airport_backend.settings import AUTH_USER_MODEL
from locations.models import Lounge


class Booking(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('cancelled', 'Cancelled'),
        ('confirmed', 'Confirmed'),
    ]
    user = models.ForeignKey(AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    lounge = models.ForeignKey(Lounge, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='in_progress')
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.lounge.name} for {self.user.username}"
