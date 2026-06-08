from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.permissions import IsMerchant
from apps.common.response import success, error
from apps.merchant.models import Inventory, Merchant, Product
from apps.merchant.serializers import (
    MerchantSerializer, MerchantLoginSerializer,
    ProductSerializer, ProductWriteSerializer, ProductUpdateSerializer,
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


class MerchantApplicationView(APIView):
    """入驻申请 — GET/POST /merchant/api/application"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        """获取当前入驻申请状态"""
        try:
            merchant = Merchant.objects.get(user=request.user)
        except Merchant.DoesNotExist:
            return error("尚未提交入驻申请", status.HTTP_200_OK)
        from apps.merchant.serializers import MerchantApplicationStatusSerializer
        return success(MerchantApplicationStatusSerializer(merchant).data)

    def post(self, request):
        """提交/重新提交入驻申请"""
        from apps.merchant.serializers import MerchantApplicationSerializer
        ser = MerchantApplicationSerializer(data=request.data)
        if not ser.is_valid():
            return error(ser.errors, status.HTTP_400_BAD_REQUEST)

        data = ser.validated_data
        Merchant.objects.update_or_create(
            user=request.user,
            defaults={
                "name": data["merchant_name"],
                "contact_name": data["contact_name"],
                "phone": data["phone"],
                "business_scope": data.get("business_scope", ""),
                "supply_desc": data.get("supply_description", ""),
                "status": Merchant.Status.PENDING,
            },
        )
        return success(None, "申请已提交，等待审核")


class ProductListView(APIView):
    """商品列表与新增 — GET/POST /merchant/api/products"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        """商品列表，支持 ?status=&keyword= 过滤"""
        merchant = get_object_or_404(Merchant, user=request.user)
        qs = Product.objects.filter(merchant=merchant)

        status_filter = request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)

        keyword = request.query_params.get("keyword")
        if keyword:
            qs = qs.filter(name__icontains=keyword)

        return success(ProductSerializer(qs, many=True).data)

    def post(self, request):
        """提交新商品"""
        merchant = get_object_or_404(Merchant, user=request.user)

        ser = ProductWriteSerializer(data=request.data)
        if not ser.is_valid():
            return error(ser.errors, status.HTTP_400_BAD_REQUEST)

        data = ser.validated_data
        product = Product.objects.create(
            merchant=merchant,
            name=data["name"],
            image=data.get("image", ""),
            description=data.get("description", ""),
            category=data["category"],
            rarity=data["rarity"],
            estimated_points=0,
            status=Product.Status.PENDING,
        )
        Inventory.objects.create(product=product, current_stock=data.get("stock", 0))
        return success(ProductSerializer(product).data, "提交成功，等待审核")


class ProductDetailView(APIView):
    """商品详情与编辑 — GET/PUT /merchant/api/products/<pk>"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def _get_product(self, pk, user):
        merchant = get_object_or_404(Merchant, user=user)
        return get_object_or_404(Product, pk=pk, merchant=merchant)

    def get(self, request, pk):
        product = self._get_product(pk, request.user)
        return success(ProductSerializer(product).data)

    def put(self, request, pk):
        product = self._get_product(pk, request.user)

        ser = ProductUpdateSerializer(data=request.data)
        if not ser.is_valid():
            return error(ser.errors, status.HTTP_400_BAD_REQUEST)

        data = ser.validated_data
        for field in ("name", "image", "description"):
            if field in data:
                setattr(product, field, data[field])

        if "stock" in data:
            inv, _ = Inventory.objects.get_or_create(product=product)
            inv.current_stock = data["stock"]
            inv.save()

        product.save()
        return success(None, "修改成功")
