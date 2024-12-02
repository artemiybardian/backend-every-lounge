from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from .models import Airport, Lounge
from .serializers import AirportSerializer, LoungeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.db.models import Q
from .utils import haversine
from rest_framework.decorators import action

# Эндпоинт для списка аэропортов
class AirportReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer



# Эндпоинт для списка залов в выбранном аэропорту
class LoungeReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lounge.objects.all()
    serializer_class = LoungeSerializer

    # Метод для получения списка залов по коду аэропорта
    @action(detail=False, methods=['get'], url_path='by_airport')
    def list_by_airport(self, request):
        airport_code = request.query_params.get('airport_code')
        if not airport_code:
            return Response({"error": "airport_code is required"}, status=status.HTTP_400_BAD_REQUEST)

        lounges = Lounge.objects.filter(airport_id__code=airport_code)
        serializer = self.get_serializer(lounges, many=True)
        return Response(serializer.data)

    # Метод для получения детальной информации о конкретном зале по его ID
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class NearestAirportsView(generics.ListAPIView):
    serializer_class = AirportSerializer

    def get_queryset(self):
        user = self.request.user

        # Проверка, что у пользователя установлены координаты
        if not user.location or 'latitude' not in user.location or 'longitude' not in user.location:
            return []

        user_lat = user.location['latitude']
        user_lon = user.location['longitude']

        # Получаем количество ближайших аэропортов по умолчанию из настроек
        nearest_count = getattr(settings, 'NEAREST_AIRPORTS_COUNT', 2)

        # Создаем список для хранения аэропортов с рассчитанным расстоянием
        airports_with_distance = []

        # Вычисляем расстояние до каждого аэропорта и добавляем в список
        for airport in Airport.objects.all():
            airport_location = airport.location
            airport_lat = airport_location.get('latitude')
            airport_lon = airport_location.get('longitude')

            if airport_lat is None or airport_lon is None:
                continue

            # Рассчитываем расстояние и добавляем аэропорты в список
            distance = haversine(user_lat, user_lon, airport_lat, airport_lon)

            # Извлекаем нужные поля из объекта Airport, чтобы они были сериализуемыми
            airports_with_distance.append({
                'id': airport.id,
                'name': airport.name,
                'code': airport.code,
                'city': airport.city,
                'country': airport.country,
                'distance': round(distance)
            })

        # Сортируем аэропорты по расстоянию
        airports_with_distance.sort(key=lambda x: x['distance'])

        # Ограничиваем список ближайшими аэропортами
        return airports_with_distance[:nearest_count]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset:
            return Response({"error": "User location not set or no airports found"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(queryset, status=status.HTTP_200_OK)


class AirportSearchView(APIView):
    """
    API для поиска аэропортов по названию, городу или коду аэропорта
    """

    def get(self, request):
        word = request.query_params.get('word', '').strip()
        if not word:
            return Response([], status=status.HTTP_200_OK)

        # Поиск совпадений по полям name, code, city
        airports = Airport.objects.filter(
            Q(name__icontains=word) |
            Q(code__icontains=word) |
            Q(city__icontains=word) |
            Q(country__icontains=word)
        )

        if not airports.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = AirportSerializer(airports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
