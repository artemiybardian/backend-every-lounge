from django.urls import path, include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.schemas import get_schema_view
# from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Описание доступных API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # Только для чтения, можете настроить доступ
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # path('api/api_schema/', get_schema_view(
    #     title='API Schema',
    #     description='Guide for the REST API'
    # ), name='api_schema'),
    # path("api/swagger/", TemplateView.as_view(
    #             template_name="swagger-ui.html",
    #             extra_context={"schema_url": "/api/api_schema/"},
    #     ),
    #      name="swagger-ui",
    # ),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
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
