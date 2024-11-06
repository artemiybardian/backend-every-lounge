from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUser


class TelegramAuthView(APIView):
    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        username = request.data.get("username")  # username в Telegram
        location = request.data.get("location")

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
            user.save()
            
            login(request, user)
            
            return Response({"status": "success", "details": "Location updated successfully"}, status=status.HTTP_200_OK)
        
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(
                telegram_id=telegram_id, username=username, location=location_json)
            
            return Response({"status": "success", "details": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"status": "error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        