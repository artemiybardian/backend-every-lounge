from django.urls import path, include
from .views import TelegramAuthView

urlpatterns = [
    path('auth/', TelegramAuthView.as_view())
]
