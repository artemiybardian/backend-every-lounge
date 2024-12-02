from django.urls import path, include
from rest_framework.routers import SimpleRouter
from locations import views


router = SimpleRouter()
router.register(r'airports', views.AirportReadOnlyViewSet)
router.register(r'lounges', views.LoungeReadOnlyViewSet, basename='lounge')

urlpatterns = [
    path('', include(router.urls)),
    path('nearest_airports/', views.NearestAirportsView.as_view()),
    path('airport/search/', views.AirportSearchView.as_view(), name='airport-search'),
]
