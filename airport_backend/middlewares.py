from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.middleware import get_user


class DisableJWTForAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and 'Authorization' in request.headers:
            try:
                # Попытка извлечь пользователя через JWT
                jwt_auth = JWTAuthentication()
                jwt_auth.authenticate(request)
                request.user = get_user(request)
            except Exception:
                request.user = None
        return self.get_response(request)
