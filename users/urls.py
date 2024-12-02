from django.urls import path, include
from .views import TelegramAuthView, UserProfileView

urlpatterns = [
    path('auth/', TelegramAuthView.as_view()),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
