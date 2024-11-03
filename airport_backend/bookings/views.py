from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from locations.models import Lounge
from airport_backend.settings import MARKUP_PERCENTAGE
from .models import Booking, BookingLog
from .serializers import BookingSerializer


# Эндпоинт для создания бронирования
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        lounge_id = request.data.get('lounge_id')

        try:
            lounge = Lounge.objects.get(id=lounge_id)
        except Lounge.DoesNotExist:
            return Response({'status': 'error', 'details': 'Lounge not found'}, status=status.HTTP_404_NOT_FOUND)

        # Пример наценки
        markup_percentage = MARKUP_PERCENTAGE
        total_price = lounge.base_price * (1 + markup_percentage)

        booking = Booking.objects.create(
            user=user,
            lounge=lounge,
            total_price=total_price,
            status='in_progress'
        )
        
        # Логируем создание бронирования
        BookingLog.objects.create(booking_id=booking)

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
