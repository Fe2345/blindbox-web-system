from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.permissions import IsMerchant
from apps.common.response import success, error
from apps.merchant.models import Merchant
from apps.merchant.serializers import (
    MerchantSerializer, MerchantLoginSerializer,
)


class MerchantLoginView(APIView):
    """商家登录 — POST /merchant/api/login"""

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        ser = MerchantLoginSerializer(data=request.data)
        if not ser.is_valid():
            return error(ser.errors, status.HTTP_400_BAD_REQUEST)

        username = ser.validated_data["username"]
        password = ser.validated_data["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            return error("用户名或密码错误", status.HTTP_200_OK)
        if not user.is_active:
            return error("账号已被冻结", status.HTTP_200_OK)
        if user.role != "merchant":
            return error("非商家账号", status.HTTP_200_OK)

        refresh = RefreshToken.for_user(user)
        try:
            merchant = Merchant.objects.get(user=user)
        except Merchant.DoesNotExist:
            return error("商家档案不存在", status.HTTP_200_OK)

        return success({
            "token": str(refresh.access_token),
            "merchant": MerchantSerializer(merchant).data,
        })


class MerchantInfoView(APIView):
    """当前商家信息 — GET /merchant/api/info"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        try:
            merchant = Merchant.objects.get(user=request.user)
        except Merchant.DoesNotExist:
            return error("商家档案不存在", status.HTTP_404_NOT_FOUND)
        return success(MerchantSerializer(merchant).data)
