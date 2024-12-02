from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework import status
from users.models import CustomUser
from .serializers import CustomUserSerializer
from logging import getLogger
from rest_framework_simplejwt.tokens import RefreshToken
import logging


logging.basicConfig(level=logging.INFO)
log = getLogger(__name__)


class TelegramAuthView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        username = request.data.get("username")  # username в Telegram
        location = request.data.get("location")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        if not telegram_id or not location:
            return Response({"error": "telegram_id and location is required"}, status=status.HTTP_400_BAD_REQUEST)

        latitude = location.get("latitude")
        longitude = location.get("longitude")
        
        if latitude is None or longitude is None:
            return Response({"status": "error", "details": "Both latitude and longitude are required in location"}, status=status.HTTP_400_BAD_REQUEST)

        location_json = {"latitude": latitude, "longitude": longitude}
        
        try:
            user = CustomUser.objects.get(
                telegram_id=telegram_id)

            user.location = location_json
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            log.info(f"Get access token for {user.username} - {access_token}")

            return Response({
                "status": "success",
                "details": "Location updated successfully",
                "token": access_token  
            }, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(
                telegram_id=telegram_id, username=username, location=location_json, first_name=first_name, last_name=last_name)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            log.info(f"Get access token for {user.username} - {access_token}")

            return Response({
                "status": "success",
                "details": "Location updated successfully",
                "token": access_token
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=200)
