from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path('api/api_schema/', get_schema_view(
        title='API Schema',
        description='Guide for the REST API'
    ), name='api_schema'),
    path("api/swagger/", TemplateView.as_view(
                template_name="swagger-ui.html",
                extra_context={"schema_url": "/api/api_schema/"},
        ),
         name="swagger-ui",
    ),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/locations/', include('locations.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
