from django.urls import path, include
from rest_framework import permissions
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка схемы Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Every Lounge Backend",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

from django.urls import path, include

urlpatterns = [
    path('admin/', include('admin_panel.urls')),
    path('api/users/', include('users.urls')),
    path('api/locations/', include('locations.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/notifications/', include('notifications.urls')),
]
