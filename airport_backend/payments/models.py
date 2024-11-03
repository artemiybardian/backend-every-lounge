from django.db import models
from bookings.models import Booking


class Transaction(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    booking = models.ForeignKey(
        Booking, related_name="transactions", on_delete=models.CASCADE)
    # ID платежа в платежной системе
    payment_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.payment_id} - {self.status}"
