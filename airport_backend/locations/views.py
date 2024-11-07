from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Airport, Lounge
from .serializers import AirportSerializer, LoungeSerializer, LoungeDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
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


class NearestAirportsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user

        # Проверка, что у пользователя установлены координаты
        if not user.location or 'latitude' not in user.location or 'longitude' not in user.location:
            return Response({"error": "User location not set"}, status=status.HTTP_400_BAD_REQUEST)

        user_lat = user.location['latitude']
        user_lon = user.location['longitude']

        # Получаем количество ближайших аэропортов по умолчанию из настроек
        nearest_count = getattr(settings, 'NEAREST_AIRPORTS_COUNT', 2)

        # Создаем список для хранения аэропортов с рассчитанным расстоянием
        airports_with_distance = []

        # Вычисляем расстояние до каждого аэропорта и добавляем в список
        for airport in Airport.objects.all():
            airport_location = airport.location
            airport_lat = airport_location['latitude']
            airport_lon = airport_location['longitude']

            # Преобразуем строку WKT "POINT(longitude latitude)" в координаты
            # match = re.match(r'POINT\(([-\d.]+)\s([-\d.]+)\)', airport_location)
            # if not match:
            #     # Пропускаем аэропорт с некорректным форматом
            #     continue

            # airport_lon = float(match.group(1))
            # airport_lat = float(match.group(2))

            if not airport_lat or not airport_lon:
                continue

            # Рассчитываем расстояние и добавляем аэропорты в список
            distance = haversine(user_lat, user_lon, airport_lat, airport_lon)

            # Извлекаем нужные поля из объекта Airport, чтобы они были сериализуемыми
            airports_with_distance.append({
                'id': airport.id,
                'name': airport.name,  # Предполагается, что у модели Airport есть поле `name`
                'latitude': airport_lat,
                'longitude': airport_lon,
                'distance': distance
            })

        # Сортируем аэропорты по расстоянию
        airports_with_distance.sort(key=lambda x: x['distance'])

        # Ограничиваем список ближайшими аэропортами
        nearest_airports = airports_with_distance[:nearest_count]

        # Возвращаем ответ
        return Response(nearest_airports, status=status.HTTP_200_OK)
