from django.urls import path, include
from rest_framework.routers import SimpleRouter
from locations import views

router = SimpleRouter()
router.register(r'airports', views.AirportReadOnlyViewSet)
router.register(r'lounges', views.LoungeReadOnlyViewSet)
router.register(r'lounges_details',
                views.LoungeDetailReadOnlyViewSet, basename='lounge-detail')

urlpatterns = [
    path('', include(router.urls))
]
