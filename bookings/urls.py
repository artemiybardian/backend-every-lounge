from django.urls import path
from bookings.views import BookingCreateAPIView


urlpatterns = [
    path('create/', BookingCreateAPIView.as_view())
]
