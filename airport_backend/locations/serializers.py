from rest_framework import serializers
from .models import Airport, Lounge


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'name', 'code', 'city', 'country']


class LoungeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lounge
        fields = ['id', 'name', 'description', 'terminal',
                  'base_price', 'features', 'gallery']


class LoungeDetailSerializer(serializers.ModelSerializer):
    schedule = serializers.StringRelatedField(many=True)
    entry_conditions = serializers.StringRelatedField(many=True)
    features = serializers.StringRelatedField(many=True)
    gallery = serializers.StringRelatedField(many=True)

    class Meta:
        model = Lounge
        fields = ['id', 'name', 'description', 'terminal', 'base_price',
                  'schedule', 'entry_conditions', 'features', 'gallery']


class NearestAirportSerializer(serializers.ModelSerializer):
    distance = serializers.FloatField(read_only=True)

    class Meta:
        model = Airport
        fields = ['id', 'name', 'code', 'city',
                  'country', 'location', 'distance']
