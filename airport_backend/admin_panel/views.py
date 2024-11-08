from django.db.models import Count, Q
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .utils import send_telegram_notification
from .models import AdminActionLog
from .serializers import AdminActionLogSerializer, BookingAnalyticsSerializer
from locations.models import Airport, Lounge 
from bookings.serializers import Booking
from locations.serializers import AirportSerializer, LoungeSerializer
from bookings.serializers import BookingSerializer

from datetime import datetime


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminUser]  # Только админы могут управлять данными


class LoungeViewSet(viewsets.ModelViewSet):
    queryset = Lounge.objects.all()
    serializer_class = LoungeSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'], url_path='by_airport')
    def list_by_airport(self, request):
        airport_code = request.query_params.get('airport_code')
        if not airport_code:
            return Response({"error": "airport_code is required"}, status=status.HTTP_400_BAD_REQUEST)

        lounges = Lounge.objects.filter(airport_id__code=airport_code)
        serializer = self.get_serializer(lounges, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=True, methods=['get'], permission_classes=[IsAdminUser], url_path='confirm')
    def confirm(self, request, pk=None):
        # Получаем объект бронирования по pk
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        booking.status = 'confirmed'
        booking.save()

        send_telegram_notification(
            booking.user.telegram_id,
            f"Ваше бронирование {booking.lounge.name} для аэропорта {booking.lounge.airport_id.name} одобрено!")

        AdminActionLog.objects.create(
            admin_user=request.user,
            action=f"Бронирование #{booking.id} одобрено!"
        )
        
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['get'], permission_classes=[IsAdminUser], url_path='cancel')
    def cancel(self, request, pk=None):
        # Получаем объект бронирования по pk
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        booking.status = 'cancelled'
        booking.save()

        send_telegram_notification(
            booking.user.telegram_id,
            f"Ваше бронирование {booking.lounge.name} для аэропорта {booking.lounge.airport_id.name} отклонено!")

        AdminActionLog.objects.create(
            admin_user=request.user,
            action=f"Бронирование #{booking.id} отменено!"
        )

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
    
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser], url_path='in_progress')
    def in_progress_bookings(self, request):
        """
        Get all bookings with 'in_progress' status.
        Only accessible by superusers.
        """
        in_progress_bookings = Booking.objects.filter(status='in_progress')
        serializer = self.get_serializer(in_progress_bookings, many=True)
        return Response(serializer.data)


class AdminLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdminActionLog.objects.all()
    serializer_class = AdminActionLogSerializer
    permission_classes = [IsAdminUser]  


class BookingAnalyticsAPIView(generics.ListAPIView):
    serializer_class = BookingAnalyticsSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Получаем параметры start_date и end_date
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({'error': 'Both start_date and end_date are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({'error': 'Invalid date format, use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        # Фильтруем по датам
        bookings = Booking.objects.filter(
            created_at__range=[start_date, end_date]
        )

        # Выполняем агрегацию
        analytics = bookings.aggregate(
            total_bookings=Count('id'),
            confirmed_bookings=Count('id', filter=Q(status='confirmed')),
            cancelled_bookings=Count('id', filter=Q(status='cancelled')),
            in_progress_bookings=Count('id', filter=Q(status='in_progress'))
        )

        # Добавляем даты в результат
        result = {
            'start_date': start_date,
            'end_date': end_date,
            'total_bookings': analytics['total_bookings'],
            'confirmed_bookings': analytics['confirmed_bookings'],
            'cancelled_bookings': analytics['cancelled_bookings'],
            'in_progress_bookings': analytics['in_progress_bookings']
        }

        return Response(result, status=status.HTTP_200_OK)
