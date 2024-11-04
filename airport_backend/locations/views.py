from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Airport, Lounge
from .serializers import AirportSerializer, LoungeSerializer, LoungeDetailSerializer, NearestAirportSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from .models import Airport
from .utils import haversine



# Эндпоинт для списка аэропортов
class AirportReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer



# Эндпоинт для списка залов в выбранном аэропорту
class LoungeReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lounge.objects.all()
    serializer_class = LoungeSerializer

    def list(self, request, *args, **kwargs):
        airport_id = request.query_params.get('airport_id')
        if not airport_id:
            return Response({"error": "airport_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        lounges = Lounge.objects.filter(airport_id=airport_id)
        serializer = self.get_serializer(lounges, many=True)
        return Response(serializer.data)



# Эндпоинт для детальной информации о зале
class LoungeDetailReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lounge.objects.all()
    serializer_class = LoungeDetailSerializer


# Эндпоинт для ближайших аэропортов
class NearestAirportsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user

        # Проверка, что у пользователя установлены координаты
        if not user.location or 'latitude' not in user.location or 'longitude' not in user.location:
            return Response({"error": "User location not set"}, status=status.HTTP_400_BAD_REQUEST)

        user_lat = user.location['latitude']
        user_lon = user.location['longitude']

        # Получаем количество ближайших аэропортов по умолчанию из настроек
        # Используем 2 как значение по умолчанию
        nearest_count = getattr(settings, 'NEAREST_AIRPORTS_COUNT', 2)

        # Создаем список для хранения аэропортов с рассчитанным расстоянием
        airports_with_distance = []

        # Вычисляем расстояние до каждого аэропорта и добавляем в список
        for airport in Airport.objects.all():
            airport_lat = airport.location.get('latitude')
            airport_lon = airport.location.get('longitude')

            if airport_lat is not None and airport_lon is not None:
                distance = haversine(user_lat, user_lon,
                                     airport_lat, airport_lon)
                airports_with_distance.append({
                    "airport": airport,
                    "distance": distance
                })
            else:
                return Response({'status': 'error', 'details': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Сортируем аэропорты по расстоянию и берем количество ближайших из настройки
        sorted_airports = sorted(airports_with_distance, key=lambda x: x["distance"])[:nearest_count]

        # Сериализуем данные для ответа, включая расстояние
        serializer = NearestAirportSerializer(
            [item["airport"] for item in sorted_airports], many=True)
        for idx, airport_data in enumerate(serializer.data):
            airport_data["distance"] = sorted_airports[idx]["distance"]

        return Response(serializer.data)
