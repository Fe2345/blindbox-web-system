import os
import uuid

from django.conf import settings
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.permissions import IsAdmin, IsMerchant
from apps.common.response import success, error, flatten_errors
from apps.accounts.models import User
from apps.merchant.models import Inventory, InventoryRecord, Merchant, Product, ShipmentTask
from apps.merchant.serializers import (
    MerchantSerializer, MerchantLoginSerializer, MerchantRegisterSerializer,
    ProductSerializer, ProductWriteSerializer, ProductUpdateSerializer,
    InventorySerializer, InventoryUpdateSerializer, InventoryRecordSerializer,
    ShipmentTaskSerializer, ShipmentConfirmSerializer,
    AdminMerchantSerializer, AdminMerchantReviewSerializer,
    AdminMerchantStatusSerializer, AdminProductSerializer,
    AdminProductReviewSerializer,
)


class CSRFExemptView(APIView):
    pass


class MerchantRegisterView(APIView):
    """商家注册 — POST /merchant/api/register"""

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        ser = MerchantRegisterSerializer(data=request.data)
        if not ser.is_valid():
            return error(ser.errors, status.HTTP_400_BAD_REQUEST)

        data = ser.validated_data
        user = User.objects.create_user(
            username=data["username"],
            password=data["password"],
            phone=data.get("phone", ""),
        )
        user.role = User.Role.MERCHANT
        user.save(update_fields=["role"])

        Merchant.objects.create(
            user=user,
            phone=data.get("phone", ""),
            status=Merchant.Status.PENDING,
        )
        return success(None, "注册成功")


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
        refresh["role"] = user.role
        try:
            merchant = Merchant.objects.get(user=user)
        except Merchant.DoesNotExist:
            return error("商家档案不存在", status.HTTP_200_OK)

        jwt_config = settings.SIMPLE_JWT
        access = str(refresh.access_token)
        response = success({
            "token": access,
            "merchant": MerchantSerializer(merchant).data,
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


class MerchantLogoutView(APIView):
    """商家登出 — POST /merchant/api/logout"""

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        jwt_config = settings.SIMPLE_JWT
        response = success(message="已退出登录")
        response.delete_cookie(jwt_config["AUTH_COOKIE"], path=jwt_config["AUTH_COOKIE_PATH"])
        response.delete_cookie(jwt_config["AUTH_COOKIE_REFRESH"], path=jwt_config["AUTH_COOKIE_PATH"])
        return response


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
        if not merchant.name:
            return success(None)
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


class ProductImageUploadView(APIView):
    """上传商品图片 — POST /merchant/api/products/upload-image"""

    permission_classes = [IsAuthenticated, IsMerchant]

    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    MAX_SIZE = 2 * 1024 * 1024  # 2MB

    def post(self, request):
        file = request.FILES.get("image")
        if not file:
            return error("请选择文件", status.HTTP_400_BAD_REQUEST)

        ext = os.path.splitext(file.name)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            return error("仅支持 JPG、PNG、GIF、WebP 格式", status.HTTP_400_BAD_REQUEST)

        if file.size > self.MAX_SIZE:
            return error("文件大小不能超过 2MB", status.HTTP_400_BAD_REQUEST)

        filename = f"{uuid.uuid4().hex}{ext}"
        product_dir = os.path.join(settings.MEDIA_ROOT, "product")
        os.makedirs(product_dir, exist_ok=True)

        filepath = os.path.join(product_dir, filename)
        with open(filepath, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        image_url = f"{settings.MEDIA_URL}product/{filename}"
        return success(data={"image": image_url})


class InventoryListView(APIView):
    """库存列表 — GET /merchant/api/inventory"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        merchant = get_object_or_404(Merchant, user=request.user)
        inventories = Inventory.objects.filter(product__merchant=merchant).select_related("product")
        return success(InventorySerializer(inventories, many=True).data)


class InventoryUpdateView(APIView):
    """更新库存 — PUT /merchant/api/inventory/<product_id>"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def put(self, request, product_id):
        merchant = get_object_or_404(Merchant, user=request.user)
        product = get_object_or_404(Product, pk=product_id, merchant=merchant)
        inv, _ = Inventory.objects.get_or_create(product=product)

        ser = InventoryUpdateSerializer(data=request.data)
        if not ser.is_valid():
            return error(ser.errors, status.HTTP_400_BAD_REQUEST)

        new_stock = ser.validated_data["stock"]
        InventoryRecord.objects.create(
            product=product,
            type=InventoryRecord.ChangeType.MODIFY,
            before_stock=inv.current_stock,
            after_stock=new_stock,
            reason="商家手动调整",
        )
        inv.current_stock = new_stock
        inv.save()
        return success(None, "库存已更新")


class InventoryRecordListView(APIView):
    """库存变更记录 — GET /merchant/api/inventory/records?productId="""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        merchant = get_object_or_404(Merchant, user=request.user)
        qs = InventoryRecord.objects.filter(product__merchant=merchant).select_related("product")

        product_id = request.query_params.get("productId")
        if product_id:
            qs = qs.filter(product_id=product_id)

        return success(InventoryRecordSerializer(qs, many=True).data)


class ShipmentTaskListView(APIView):
    """发货任务列表 — GET /merchant/api/shipments?status="""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        merchant = get_object_or_404(Merchant, user=request.user)
        qs = ShipmentTask.objects.filter(product__merchant=merchant).select_related("product")

        status_filter = request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)

        return success(ShipmentTaskSerializer(qs, many=True).data)


class ShipmentTaskDetailView(APIView):
    """发货任务详情 — GET /merchant/api/shipments/<id>"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request, pk):
        merchant = get_object_or_404(Merchant, user=request.user)
        task = get_object_or_404(ShipmentTask, pk=pk, product__merchant=merchant)
        return success(ShipmentTaskSerializer(task).data)


class ShipmentConfirmView(APIView):
    """确认发货 — POST /merchant/api/shipments/<id>/ship"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def post(self, request, pk):
        merchant = get_object_or_404(Merchant, user=request.user)
        task = get_object_or_404(ShipmentTask, pk=pk, product__merchant=merchant)

        if task.status != ShipmentTask.Status.PENDING:
            return error("当前状态不可发货", status.HTTP_200_OK)

        ser = ShipmentConfirmSerializer(data=request.data)
        if not ser.is_valid():
            return error(ser.errors, status.HTTP_400_BAD_REQUEST)

        data = ser.validated_data
        task.status = ShipmentTask.Status.SHIPPED
        task.logistics_company = data["logistics_company"]
        task.tracking_no = data["tracking_no"]
        task.shipped_at = timezone.now()
        task.save()
        return success(None, "发货成功")


class MerchantDashboardView(APIView):
    """商家工作台 — GET /merchant/api/dashboard"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        merchant = get_object_or_404(Merchant, user=request.user)
        products = Product.objects.filter(merchant=merchant)
        total = products.count()
        pending = products.filter(status=Product.Status.PENDING).count()
        low_stock = Inventory.objects.filter(
            product__merchant=merchant, current_stock__lt=10
        ).count()
        pending_ship = ShipmentTask.objects.filter(
            product__merchant=merchant, status=ShipmentTask.Status.PENDING
        ).count()

        todos = []
        if pending:
            todos.append({"id": 1, "title": f"{pending} 个商品待审核", "type": "product", "link": "/products"})
        if pending_ship:
            todos.append({"id": 2, "title": f"{pending_ship} 个待发货任务", "type": "shipment", "link": "/shipments"})
        if low_stock:
            todos.append({"id": 3, "title": f"{low_stock} 个商品库存不足", "type": "stock", "link": "/inventory"})

        return success({
            "totalProducts": total,
            "pendingProducts": pending,
            "lowStockProducts": low_stock,
            "pendingShipments": pending_ship,
            "reviewStatus": merchant.status,
            "todos": todos,
        })


class RecordListView(APIView):
    """活动记录 — GET /merchant/api/records?type=&keyword=&startDate=&endDate="""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        merchant = get_object_or_404(Merchant, user=request.user)
        records = []

        type_filter = request.query_params.get("type")
        keyword = request.query_params.get("keyword")
        start_date = request.query_params.get("startDate")
        end_date = request.query_params.get("endDate")

        # 库存变更记录
        if not type_filter or type_filter == "inventory":
            inv_qs = InventoryRecord.objects.filter(
                product__merchant=merchant
            ).select_related("product")
            if keyword:
                inv_qs = inv_qs.filter(product__name__icontains=keyword)
            if start_date:
                inv_qs = inv_qs.filter(created_at__gte=start_date)
            if end_date:
                inv_qs = inv_qs.filter(created_at__lte=end_date)
            for r in inv_qs:
                records.append({
                    "id": f"inv-{r.id}",
                    "type": "inventory",
                    "productName": r.product.name,
                    "description": {
                        "increase": "入库", "decrease": "出库", "modify": "调整"
                    }.get(r.type, r.type),
                    "detail": f"{r.before_stock} → {r.after_stock}",
                    "createdAt": r.created_at.isoformat(),
                })

        # 发货记录
        if not type_filter or type_filter == "shipment":
            ship_qs = ShipmentTask.objects.filter(
                product__merchant=merchant, status=ShipmentTask.Status.SHIPPED
            ).select_related("product")
            if keyword:
                ship_qs = ship_qs.filter(product__name__icontains=keyword)
            if start_date:
                ship_qs = ship_qs.filter(shipped_at__gte=start_date)
            if end_date:
                ship_qs = ship_qs.filter(shipped_at__lte=end_date)
            for t in ship_qs:
                records.append({
                    "id": f"ship-{t.id}",
                    "type": "shipment",
                    "productName": t.product.name,
                    "description": "发货",
                    "detail": f"物流: {t.logistics_company} {t.tracking_no}",
                    "createdAt": (t.shipped_at or t.created_at).isoformat(),
                })

        # 按时间倒序
        records.sort(key=lambda x: x["createdAt"], reverse=True)
        return success(records)


# ==================== 管理端 ====================


class AdminMerchantListView(CSRFExemptView):
    """商家列表（管理端）"""

    permission_classes = [IsAdmin]

    def get(self, request):
        qs = Merchant.objects.all().order_by("-created_at")
        status = request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        keyword = request.query_params.get("keyword")
        if keyword:
            qs = qs.filter(name__icontains=keyword)
        return success(data=AdminMerchantSerializer(qs[:100], many=True).data)


class AdminMerchantReviewView(CSRFExemptView):
    """商家审核（管理端）"""

    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            merchant = Merchant.objects.get(pk=pk, status="pending")
        except Merchant.DoesNotExist:
            return error(message="商家不存在或不在待审核状态", http_status=404)

        serializer = AdminMerchantReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        d = serializer.validated_data
        if d["action"] == "approve":
            merchant.status = "approved"
        else:
            merchant.status = "rejected"
        merchant.review_note = d.get("note", "")
        merchant.reviewed_at = timezone.now()
        merchant.save(update_fields=["status", "review_note", "reviewed_at"])
        return success(data=AdminMerchantSerializer(merchant).data)


class AdminMerchantStatusView(CSRFExemptView):
    """商家状态切换（管理端）"""

    permission_classes = [IsAdmin]

    def put(self, request, pk):
        try:
            merchant = Merchant.objects.get(pk=pk)
        except Merchant.DoesNotExist:
            return error(message="商家不存在", http_status=404)

        serializer = AdminMerchantStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        merchant.status = serializer.validated_data["status"]
        merchant.save(update_fields=["status"])
        return success(data=AdminMerchantSerializer(merchant).data)


class AdminProductListView(CSRFExemptView):
    """商品列表（管理端）"""

    permission_classes = [IsAdmin]

    def get(self, request):
        qs = Product.objects.select_related("merchant").all().order_by("-created_at")
        status = request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return success(data=AdminProductSerializer(qs[:100], many=True).data)


class AdminProductReviewView(CSRFExemptView):
    """商品审核（管理端）"""

    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, status="pending")
        except Product.DoesNotExist:
            return error(message="商品不存在或不在待审核状态", http_status=404)

        serializer = AdminProductReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        d = serializer.validated_data
        if d["action"] == "approve":
            product.status = "approved"
        else:
            product.status = "rejected"
        product.review_note = d.get("note", "")
        product.save(update_fields=["status", "review_note"])
        return success(data=AdminProductSerializer(product).data)
