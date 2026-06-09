import logging
import os
import uuid

from django.conf import settings
from django.contrib.auth import authenticate
from django.db import models
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.common.permissions import IsAdmin, IsAuthenticated
from apps.common.response import error, flatten_errors, success

from .models import Address, Division, User
from .serializers import (
    AddressSerializer,
    AddressWriteSerializer,
    AdminUserSerializer,
    AdminUserStatusSerializer,
    DivisionSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserInfoSerializer,
)

logger = logging.getLogger("blindbox")


@method_decorator(csrf_exempt, name="dispatch")
class CSRFExemptView(APIView):
    pass


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
            return error(message="最多添加 10 个收货地址", http_status=400)

        serializer = AddressWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

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
            return error(message="地址不存在", http_status=404)

        serializer = AddressWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

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
            return error(message="地址不存在", http_status=404)

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
            return error(message=flatten_errors(serializer.errors), http_status=400)

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
            return error(message=flatten_errors(serializer.errors), http_status=400)

        data = serializer.validated_data
        user = authenticate(request, username=data["username"], password=data["password"])
        if user is None:
            return error(message="用户名或密码错误", http_status=400)

        if not user.is_active:
            return error(message="账号已被冻结", http_status=400)

        jwt_config = settings.SIMPLE_JWT
        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        access = str(refresh.access_token)

        from apps.points.models import PointsAccount
        points_account = PointsAccount.objects.filter(user=user).first()

        response = success(data={
            "token": access,
            "user": {
                "id": user.id,
                "username": user.username,
                "phone": user.phone,
                "avatar": user.avatar,
                "role": user.role,
                "points": points_account.balance if points_account else 0,
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


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    """刷新时从旧 refresh token 中保留 role claim 到新 access token。"""

    def validate(self, attrs):
        # 在父类刷新（可能轮换 token）之前，从旧 token 读取 role
        refresh = RefreshToken(attrs["refresh"])
        role = refresh.get("role")

        data = super().validate(attrs)

        if role and "access" in data:
            # super().validate 内部的 refresh.access_token 是一个可变对象，
            # 直接修改它会影响 data["access"] 的序列化结果
            new_refresh = RefreshToken(data["refresh"])
            new_refresh.access_token["role"] = role
            data["access"] = str(new_refresh.access_token)
        return data


class CookieTokenRefreshView(TokenRefreshView):
    """Token 刷新视图：优先从 httpOnly cookie 读取 refresh token，
    刷新成功后更新 cookie 中的新 token。"""

    serializer_class = CookieTokenRefreshSerializer

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


class UserInfoView(APIView):
    """获取 / 修改当前用户基本资料"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return success(data=self._user_data(user))

    def put(self, request):
        serializer = UserInfoSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        data = serializer.validated_data
        user = request.user
        updatable = ["username", "phone", "avatar"]
        for field in updatable:
            if field in data:
                setattr(user, field, data[field])
        if any(f in data for f in updatable):
            user.save(update_fields=[f for f in updatable if f in data])

        return success(data=self._user_data(user))

    @staticmethod
    def _user_data(user):
        from apps.points.models import PointsAccount
        points_account = PointsAccount.objects.filter(user=user).first()
        return {
            "id": user.id,
            "username": user.username,
            "phone": user.phone,
            "avatar": user.avatar,
            "points": points_account.balance if points_account else 0,
            "status": "active" if user.is_active else "frozen",
            "createdAt": user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
        }


class AvatarUploadView(APIView):
    """上传用户头像"""

    permission_classes = [IsAuthenticated]

    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    MAX_SIZE = 2 * 1024 * 1024  # 2MB

    def post(self, request):
        file = request.FILES.get("avatar")
        if not file:
            return error(message="请选择文件", http_status=400)

        ext = os.path.splitext(file.name)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            return error(message="仅支持 JPG、PNG、GIF、WebP 格式", http_status=400)

        if file.size > self.MAX_SIZE:
            return error(message="文件大小不能超过 2MB", http_status=400)

        filename = f"{uuid.uuid4().hex}{ext}"
        avatar_dir = os.path.join(settings.MEDIA_ROOT, "avatar")
        os.makedirs(avatar_dir, exist_ok=True)

        filepath = os.path.join(avatar_dir, filename)
        with open(filepath, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        avatar_url = f"{settings.MEDIA_URL}avatar/{filename}"
        request.user.avatar = avatar_url
        request.user.save(update_fields=["avatar"])

        return success(data={"avatar": avatar_url})


class ChangePasswordView(APIView):
    """修改密码"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get("oldPassword")
        new_password = request.data.get("newPassword")

        if not old_password or not new_password:
            return error(message="请提供原密码和新密码")

        if len(new_password) < 6:
            return error(message="新密码至少6位")

        user = request.user
        if not user.check_password(old_password):
            return error(message="原密码错误")

        user.set_password(new_password)
        user.save()
        return success(message="密码修改成功")


# ==================== 管理端 ====================


class AdminUserListView(CSRFExemptView):
    """用户列表（管理端）"""

    permission_classes = [IsAdmin]

    def get(self, request):
        qs = User.objects.filter(role="user").order_by("-date_joined")
        keyword = request.query_params.get("keyword")
        if keyword:
            qs = qs.filter(
                models.Q(username__icontains=keyword) | models.Q(phone__icontains=keyword)
            )
        status = request.query_params.get("status")
        if status == "active":
            qs = qs.filter(is_active=True)
        elif status == "frozen":
            qs = qs.filter(is_active=False)
        return success(data=AdminUserSerializer(qs[:100], many=True).data)


class AdminUserStatusView(CSRFExemptView):
    """用户状态切换（管理端）"""

    permission_classes = [IsAdmin]

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk, role="user")
        except User.DoesNotExist:
            return error(message="用户不存在", http_status=404)

        serializer = AdminUserStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        user.is_active = serializer.validated_data["is_active"]
        user.save(update_fields=["is_active"])
        return success(data=AdminUserSerializer(user).data)


class AdminLoginView(CSRFExemptView):
    """管理员登录，返回 JWT Token 并设置 httpOnly cookie"""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        data = serializer.validated_data
        user = authenticate(request, username=data["username"], password=data["password"])
        if user is None:
            return error(message="用户名或密码错误", http_status=400)

        if user.role != "admin":
            return error(message="无管理员权限", http_status=403)

        if not user.is_active:
            return error(message="账号已被冻结", http_status=400)

        jwt_config = settings.SIMPLE_JWT
        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        access = str(refresh.access_token)

        response = success(data={
            "token": access,
            "user": {
                "id": user.id,
                "username": user.username,
                "phone": user.phone,
                "avatar": user.avatar,
                "role": user.role,
            },
        })

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
