from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Airport, Lounge
from .serializers import AirportSerializer, LoungeSerializer, LoungeDetailSerializer



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
