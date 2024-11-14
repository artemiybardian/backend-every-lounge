from django.urls import path, include
from rest_framework import permissions
# from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Cosmomoll Developers Api",
        default_version='v0.1',
        description="Описание для разработчиков фронтенда",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# schema_view = get_swagger_view(title="API Documentation")


urlpatterns = [
    # path('api/swagger/', schema_view),
    path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('api/admin/', include('admin_panel.urls')),
    path('api/users/', include('users.urls')),
    path('api/locations/', include('locations.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/notifications/', include('notifications.urls')),
]
