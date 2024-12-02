from django import forms
from django.db.models import Q, Count
from datetime import datetime
from bookings.models import Booking


class BookingAnalyticsForm(forms.Form):
    start_date = forms.DateField(
        label='Дата начала', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(
        label='Дата окончания', widget=forms.DateInput(attrs={'type': 'date'}))

    def get_analytics(self):
        # Получаем данные из формы
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']

        # Фильтруем записи
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

        return {
            'start_date': start_date,
            'end_date': end_date,
            'total_bookings': analytics['total_bookings'],
            'confirmed_bookings': analytics['confirmed_bookings'],
            'cancelled_bookings': analytics['cancelled_bookings'],
            'in_progress_bookings': analytics['in_progress_bookings']
        }
