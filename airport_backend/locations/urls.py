from django.urls import path, include
from rest_framework.routers import SimpleRouter
from locations import views


router = SimpleRouter()
router.register(r'airports', views.AirportReadOnlyViewSet)
router.register(r'lounges', views.LoungeReadOnlyViewSet)
router.register(r'lounges_details',
                views.LoungeDetailReadOnlyViewSet, basename='lounge-detail')
router.register(r'nearest_airports', views.NearestAirportsViewSet,
                basename='nearest_airports')

urlpatterns = [
    path('', include(router.urls))
]
