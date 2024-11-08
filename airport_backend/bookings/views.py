from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from decimal import Decimal
from locations.models import Lounge
from airport_backend.settings import MARKUP_PERCENTAGE
from admin_panel.utils import send_telegram_notification
from .models import Booking, BookingLog
from .serializers import BookingSerializer


# Эндпоинт для создания бронирования
class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        lounge_id = request.data.get('lounge_id')

        try:
            lounge = Lounge.objects.get(id=lounge_id)
        except Lounge.DoesNotExist:
            return Response({'status': 'error', 'details': 'Lounge not found'}, status=status.HTTP_404_NOT_FOUND)

        # Расчет общей цены с наценкой
        total_price = lounge.base_price * Decimal(1 + MARKUP_PERCENTAGE)

        # Создание бронирования
        booking = Booking.objects.create(
            user=user,
            lounge=lounge,
            total_price=total_price,
            status='in_progress'
        )

        # Логирование бронирования
        BookingLog.objects.create(booking_id=booking)
        
        # Отправка уведомления в Telegram (если нужно)
        send_telegram_notification(user.telegram_id, f"Ваше бронирование {booking.lounge.name} для аэропорта {booking.lounge.airport_id.name} создано.")

        # Сериализация данных и отправка ответа
        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
