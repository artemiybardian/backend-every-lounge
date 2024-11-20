from decimal import Decimal
from .models import Booking
from rest_framework import serializers
from airport_backend.settings import MARKUP_PERCENTAGE


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'lounge', 'first_name', 'last_name',
                  'guest_count', 'status', 'total_price', 'created_at']

    def create(self, validated_data):
        # Рассчитываем `total_price` с учётом гостей и наценки
        lounge = validated_data['lounge']
        guest_count = validated_data['guest_count']
        validated_data['total_price'] = (
            lounge.base_price * Decimal(1 + MARKUP_PERCENTAGE)) * guest_count

        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        base_price = instance.lounge.base_price
        guest_count = instance.guest_count
        representation['total_price'] = (
            base_price * Decimal(1 + MARKUP_PERCENTAGE)) * guest_count
        return representation
