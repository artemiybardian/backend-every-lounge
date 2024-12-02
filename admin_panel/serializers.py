from rest_framework import serializers
from .models import AdminActionLog


class AdminActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminActionLog
        fields = ['id', 'admin_user', 'action', 'timestamp']
        

class BookingAnalyticsSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    total_bookings = serializers.IntegerField()
    confirmed_bookings = serializers.IntegerField()
    cancelled_bookings = serializers.IntegerField()
    in_progress_bookings = serializers.IntegerField()
