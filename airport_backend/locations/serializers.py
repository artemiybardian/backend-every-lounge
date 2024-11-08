from rest_framework import serializers
from .models import Lounge, LoungeSchedule, EntryCondition, Feature, GalleryImage, Airport


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'name', 'code', 'city', 'country']

class LoungeScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoungeSchedule
        fields = ['valid_from_time', 'valid_till_time', 'valid_days']


class EntryConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryCondition
        fields = ['type', 'cost', 'max_stay_duration']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['name']


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['image_url']


class LoungeSerializer(serializers.ModelSerializer):
    airport = AirportSerializer(source='airport_id', read_only=True)
    schedule = LoungeScheduleSerializer(many=True, read_only=True)
    entry_conditions = EntryConditionSerializer(many=True, read_only=True)
    features = FeatureSerializer(many=True, read_only=True)
    gallery = GalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = Lounge
        fields = ['id', 'name', 'description', 'terminal', 'base_price',
                  'schedule', 'entry_conditions', 'features', 'gallery']
