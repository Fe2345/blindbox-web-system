import logging

from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.common.permissions import IsAuthenticated
from apps.common.response import error, flatten_errors, success

from .models import Address, Division, User
from .serializers import (
    AddressSerializer,
    AddressWriteSerializer,
    DivisionSerializer,
    LoginSerializer,
    RegisterSerializer,
)

logger = logging.getLogger("blindbox")


class DivisionListView(APIView):
    """查询行政区划：?parent_code=440000 → 列出下辖市/区"""

    def get(self, request):
        parent_code = request.query_params.get("parent_code")
        qs = Division.objects.all()
        if parent_code:
            qs = qs.filter(parent__code=parent_code)
        else:
            qs = qs.filter(level=1)  # 默认返回所有省
        return success(data=DivisionSerializer(qs, many=True).data)


class AddressListView(APIView):
    """用户收货地址列表 / 新增"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Address.objects.filter(user=request.user)
        self._ensure_default(request.user)
        return success(data=AddressSerializer(qs, many=True).data)

    def post(self, request):
        user = request.user
        if Address.objects.filter(user=user).count() >= 10:
            return error(message="最多添加 10 个收货地址", code=400)

        serializer = AddressWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), code=400)

        data = serializer.validated_data
        addr = Address.objects.create(
            user=user,
            receiver_name=data["receiver_name"],
            receiver_phone=data["receiver_phone"],
            province_id=data["province_code"],
            city_id=data["city_code"],
            district_id=data["district_code"],
            street=data.get("street", ""),
            detail=data["detail"],
            is_default=data["is_default"],
        )
        return success(data=AddressSerializer(addr).data)

    @staticmethod
    def _ensure_default(user):
        qs = Address.objects.filter(user=user)
        if not qs.filter(is_default=True).exists() and qs.exists():
            first = qs.first()
            first.is_default = True
            first.save(update_fields=["is_default"])


class AddressDetailView(APIView):
    """单个收货地址：修改 / 删除"""

    permission_classes = [IsAuthenticated]

    def _get(self, user, pk):
        try:
            return Address.objects.get(pk=pk, user=user)
        except Address.DoesNotExist:
            return None

    def put(self, request, pk):
        addr = self._get(request.user, pk)
        if addr is None:
            return error(message="地址不存在", code=404)

        serializer = AddressWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), code=400)

        d = serializer.validated_data
        addr.receiver_name = d["receiver_name"]
        addr.receiver_phone = d["receiver_phone"]
        addr.province_id = d["province_code"]
        addr.city_id = d["city_code"]
        addr.district_id = d["district_code"]
        addr.street = d.get("street", "")
        addr.detail = d["detail"]
        addr.is_default = d["is_default"]
        addr.save()
        return success(data=AddressSerializer(addr).data)

    def delete(self, request, pk):
        addr = self._get(request.user, pk)
        if addr is None:
            return error(message="地址不存在", code=404)

        user = request.user
        was_default = addr.is_default
        addr.delete()

        if was_default:
            first = Address.objects.filter(user=user).first()
            if first:
                first.is_default = True
                first.save(update_fields=["is_default"])
        return success(message="已删除")


class LogoutView(APIView):
    """用户登出，清除 httpOnly cookie"""

    def post(self, request):
        jwt_config = settings.SIMPLE_JWT
        response = success(message="已退出登录")
        response.delete_cookie(jwt_config["AUTH_COOKIE"], path=jwt_config["AUTH_COOKIE_PATH"])
        response.delete_cookie(jwt_config["AUTH_COOKIE_REFRESH"], path=jwt_config["AUTH_COOKIE_PATH"])
        return response


class RegisterView(APIView):
    """用户注册"""

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), code=400)

        data = serializer.validated_data
        User.objects.create_user(
            username=data["username"],
            password=data["password"],
            phone=data.get("phone", ""),
        )
        return success(message="注册成功")


class LoginView(APIView):
    """用户登录，返回 JWT Token 并设置 httpOnly cookie"""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), code=400)

        data = serializer.validated_data
        user = authenticate(request, username=data["username"], password=data["password"])
        if user is None:
            return error(message="用户名或密码错误", code=400)

        if not user.is_active:
            return error(message="账号已被冻结", code=400)

        jwt_config = settings.SIMPLE_JWT
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        response = success(data={
            "token": access,
            "user": {
                "id": user.id,
                "username": user.username,
                "phone": user.phone,
                "avatar": user.avatar,
                "status": "active" if user.is_active else "frozen",
                "createdAt": user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
            },
        })

        # 设置 httpOnly cookie
        cookie_kwargs = {
            "httponly": jwt_config["AUTH_COOKIE_HTTP_ONLY"],
            "secure": jwt_config["AUTH_COOKIE_SECURE"],
            "samesite": jwt_config["AUTH_COOKIE_SAMESITE"],
            "path": jwt_config["AUTH_COOKIE_PATH"],
        }
        response.set_cookie(
            jwt_config["AUTH_COOKIE"], access,
            max_age=jwt_config["ACCESS_TOKEN_LIFETIME"].total_seconds(),
            **cookie_kwargs,
        )
        response.set_cookie(
            jwt_config["AUTH_COOKIE_REFRESH"], str(refresh),
            max_age=jwt_config["REFRESH_TOKEN_LIFETIME"].total_seconds(),
            **cookie_kwargs,
        )
        return response


class CookieTokenRefreshView(TokenRefreshView):
    """Token 刷新视图：优先从 httpOnly cookie 读取 refresh token，
    刷新成功后更新 cookie 中的新 token。"""

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, dict) and "refresh" not in request.data:
            cookie_name = settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"]
            refresh_token = request.COOKIES.get(cookie_name)
            if refresh_token:
                request._full_data = {**request.data, "refresh": refresh_token}

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            jwt_config = settings.SIMPLE_JWT
            cookie_kwargs = {
                "httponly": jwt_config["AUTH_COOKIE_HTTP_ONLY"],
                "secure": jwt_config["AUTH_COOKIE_SECURE"],
                "samesite": jwt_config["AUTH_COOKIE_SAMESITE"],
                "path": jwt_config["AUTH_COOKIE_PATH"],
            }
            if "access" in response.data:
                response.set_cookie(
                    jwt_config["AUTH_COOKIE"],
                    response.data["access"],
                    max_age=jwt_config["ACCESS_TOKEN_LIFETIME"].total_seconds(),
                    **cookie_kwargs,
                )
            if "refresh" in response.data:
                response.set_cookie(
                    jwt_config["AUTH_COOKIE_REFRESH"],
                    response.data["refresh"],
                    max_age=jwt_config["REFRESH_TOKEN_LIFETIME"].total_seconds(),
                    **cookie_kwargs,
                )
        return response
