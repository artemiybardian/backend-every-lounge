from django.db import models
from airport_backend.settings import AUTH_USER_MODEL
from locations.models import Lounge


from django.db import models
from airport_backend.settings import AUTH_USER_MODEL
from locations.models import Lounge


class Booking(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'В процессе'),
        ('cancelled', 'Отменено'),
        ('confirmed', 'Подтверждено'),
    ]
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    lounge = models.ForeignKey(
        Lounge, on_delete=models.CASCADE, verbose_name="Бизнес-зал")
    first_name = models.CharField(
        max_length=64, null=False, default="Unknown", verbose_name="Имя")
    last_name = models.CharField(
        max_length=64, null=False, default="Unknown", verbose_name="Фамилия")
    guest_count = models.IntegerField(
        default=1, verbose_name="Количество гостей")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='in_progress', verbose_name="Статус"
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Общая цена")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания")

    def __str__(self):
        return f"Бронирование #{self.id} - {self.lounge.name}"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
    
    
class BookingLog(models.Model):
    booking_id = models.ForeignKey(
        Booking, on_delete=models.PROTECT, verbose_name="Бронирование"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Время события")

    def __str__(self):
        return f"Бронирование #{self.booking_id.id} - {self.booking_id.status}"

    class Meta:
        verbose_name = "Лог бронирования"
        verbose_name_plural = "Логи бронирования"
