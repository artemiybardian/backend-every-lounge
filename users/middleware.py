from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class TokenFromUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.GET.get('token')
        if token:
            # Устанавливаем токен в заголовки, чтобы стандартная аутентификация JWT могла его обработать
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        
        response = self.get_response(request)
        return response
