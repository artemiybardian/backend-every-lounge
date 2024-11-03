from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import BookingViewSet

router = SimpleRouter()
router.register(r'book', BookingViewSet)

urlpatterns = [
    path('', include(router.urls))
]
