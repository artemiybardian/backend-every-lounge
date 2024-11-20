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
        # Получение и валидация данных выполняется сериализатором
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save(user=request.user)

        # Логирование бронирования
        BookingLog.objects.create(booking_id=booking)

        # Отправка уведомления в Telegram
        send_telegram_notification(
            booking.user.telegram_id,
            f"Ваше бронирование {booking.lounge.name} для аэропорта {
                booking.lounge.airport_id.name} создано."
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
