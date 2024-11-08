from django.urls import path, include
from .views import BookingAnalyticsAPIView
from rest_framework.routers import DefaultRouter
from .views import AirportViewSet, LoungeViewSet, BookingViewSet, AdminLogViewSet, AdminUserCreateView

router = DefaultRouter()
router.register(r'airports', AirportViewSet)
router.register(r'lounges', LoungeViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'admin-logs', AdminLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('booking-analytics/', BookingAnalyticsAPIView.as_view(),
         name='booking-analytics'),
]
