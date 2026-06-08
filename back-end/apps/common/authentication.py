from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class CookieOrHeaderJWTAuthentication(JWTAuthentication):
    """从 httpOnly cookie 或 Authorization header 获取 JWT token 进行认证。"""

    def authenticate(self, request):
        cookie_name = settings.SIMPLE_JWT.get("AUTH_COOKIE", "access_token")
        raw_token = request.COOKIES.get(cookie_name)

        if raw_token:
            try:
                validated_token = self.get_validated_token(raw_token)
                return self.get_user(validated_token), validated_token
            except InvalidToken:
                pass

        return super().authenticate(request)
