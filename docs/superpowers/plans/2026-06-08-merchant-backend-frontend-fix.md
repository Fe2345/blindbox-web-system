# 商家端后端补全 & 前端 Mock 缺陷修复 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 补齐商家端后端全部 API（16 个端点），修复前端去掉 Mock 后的 3 处客户端过滤缺陷及类型不匹配问题。

**Architecture:** 后端遵循现有 accounts 应用的 APIView 模式 + 蛇形/驼峰命名转换 + 统一 `{code, message, data}` 响应格式。前端遵循现有 Pinia store 模式，仅修复过滤参数传递和类型定义。

**Tech Stack:** Django 6.0 + DRF + SimpleJWT, Vue 3 + TypeScript + Pinia + Element Plus

---

## 文件结构

| 操作 | 文件 | 职责 |
|------|------|------|
| 修改 | `back-end/apps/common/permissions.py` | 新增 `IsMerchant` 权限类 |
| 创建 | `back-end/apps/merchant/serializers.py` | 全部序列化器（11 个） |
| 修改 | `back-end/apps/merchant/views.py` | 13 个 View 类（覆盖 16 个端点） |
| 修改 | `back-end/apps/merchant/urls_merchant.py` | 商家端路由（13 条 path） |
| 修改 | `front-end/src/types/merchant.ts` | 补充 missing 字段 |
| 修改 | `front-end/src/views/merchant/ProductManage.vue` | 传入过滤参数到 API |
| 修改 | `front-end/src/views/merchant/ShipmentTasks.vue` | 传入过滤参数到 API |
| 修改 | `front-end/src/views/merchant/RecordQuery.vue` | 传入过滤参数到 API |

> 注：`api/merchant/*.ts` 文件本身已正确定义了 params 参数，无需修改。问题在 Vue 页面未传递参数。

---

### Task 1: 新增 `IsMerchant` 权限类

**Files:**
- Modify: `back-end/apps/common/permissions.py`

- [ ] **Step 1: 新增 IsMerchant 权限**

在 `IsAdmin` 类下方添加：

```python
class IsMerchant(BasePermission):
    """仅商家用户可访问，返回 403。"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == "merchant"
```

注意：`IsAuthenticated` 已在 `custom_exception_handler` 中映射为 401，`IsMerchant` 继承自 `BasePermission` 由 DRF 默认返回 403，会被 handler 转为"没有权限执行此操作"。

- [ ] **Step 2: 提交**

```bash
git add back-end/apps/common/permissions.py
git commit -m "feat: add IsMerchant permission class"
```

---

### Task 2: 创建商家端序列化器

**Files:**
- Create: `back-end/apps/merchant/serializers.py`

- [ ] **Step 1: 写入完整序列化器文件**

```python
import re
from rest_framework import serializers

from apps.merchant.models import (
    Merchant, Product, Inventory, InventoryRecord, ShipmentTask
)
from apps.common.utils import keys_to_camel, keys_to_snake


# ---------- merchant ----------

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = [
            "id", "name", "contact_name", "phone", "email",
            "license", "business_scope", "supply_desc", "status",
            "credit_score", "review_note", "created_at", "reviewed_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 兼容前端 Profile.vue 读取 businessScope / supplyDescription
        data["supply_count"] = instance.products.count()
        data["violation_count"] = 0  # 预留字段
        return keys_to_camel(data)


class MerchantLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class MerchantApplicationSerializer(serializers.Serializer):
    merchant_name = serializers.CharField(max_length=100)
    contact_name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=11)
    business_scope = serializers.CharField(required=False, allow_blank=True)
    supply_description = serializers.CharField(required=False, allow_blank=True)

    def to_internal_value(self, data):
        return super().to_internal_value(keys_to_snake(data))

    def validate_phone(self, value):
        if not re.match(r"^1[3-9]\d{9}$", value):
            raise serializers.ValidationError("手机号格式不正确")
        return value


class MerchantApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = [
            "id", "name", "contact_name", "phone", "business_scope",
            "supply_desc", "status", "review_note", "created_at", "reviewed_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 前端 Application.vue 期望的 key 命名
        data["merchant_name"] = data.pop("name")
        data["supply_description"] = data.pop("supply_desc", "")
        return keys_to_camel(data)


# ---------- product ----------

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id", "name", "image", "description", "category", "rarity",
            "estimated_points", "status", "review_note", "created_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            data["stock"] = instance.inventory.current_stock
        except Inventory.DoesNotExist:
            data["stock"] = 0
        return keys_to_camel(data)


class ProductWriteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    image = serializers.CharField(max_length=500, required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(max_length=50)
    rarity = serializers.ChoiceField(choices=["N", "R", "SR", "SSR"])
    stock = serializers.IntegerField(min_value=0)

    def to_internal_value(self, data):
        return super().to_internal_value(keys_to_snake(data))


class ProductUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    image = serializers.CharField(max_length=500, required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    stock = serializers.IntegerField(min_value=0, required=False)

    def to_internal_value(self, data):
        return super().to_internal_value(keys_to_snake(data))


# ---------- inventory ----------

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["id", "current_stock"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["product_id"] = instance.product_id
        data["product_name"] = instance.product.name
        data["product_image"] = instance.product.image
        stock = data.pop("current_stock")
        data["current_stock"] = stock
        if stock <= 0:
            data["stock_status"] = "empty"
        elif stock < 10:
            data["stock_status"] = "low"
        else:
            data["stock_status"] = "normal"
        return keys_to_camel(data)


class InventoryUpdateSerializer(serializers.Serializer):
    stock = serializers.IntegerField(min_value=0)

    def to_internal_value(self, data):
        return super().to_internal_value(keys_to_snake(data))


class InventoryRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryRecord
        fields = ["id", "type", "before_stock", "after_stock", "reason", "created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["product_id"] = instance.product_id
        data["product_name"] = instance.product.name
        return keys_to_camel(data)


# ---------- shipment ----------

class ShipmentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentTask
        fields = [
            "id", "task_no", "order_no", "receiver_name", "receiver_phone",
            "receiver_address", "status", "logistics_company", "tracking_no",
            "created_at", "shipped_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["product_name"] = instance.product.name
        data["product_image"] = instance.product.image
        return keys_to_camel(data)


class ShipmentConfirmSerializer(serializers.Serializer):
    logistics_company = serializers.CharField(max_length=100)
    tracking_no = serializers.CharField(max_length=100)

    def to_internal_value(self, data):
        return super().to_internal_value(keys_to_snake(data))
```

- [ ] **Step 2: 提交**

```bash
git add back-end/apps/merchant/serializers.py
git commit -m "feat: add merchant serializers"
```

---

### Task 3: 商家认证视图（Login / Info）

**Files:**
- Modify: `back-end/apps/merchant/views.py`

- [ ] **Step 1: 写入 MerchantLoginView 和 MerchantInfoView**

```python
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
```

- [ ] **Step 2: 提交**

```bash
git add back-end/apps/merchant/views.py
git commit -m "feat: add merchant login and info views"
```

---

### Task 4: 入驻申请视图

**Files:**
- Modify: `back-end/apps/merchant/views.py`（追加）

- [ ] **Step 1: 追加 MerchantApplicationView（合并 GET + POST）**

Django URL 匹配不区分 HTTP 方法，因此 `GET /application` 和 `POST /application` 必须合并到一个 View 中，通过 `get()` 和 `post()` 方法区分。

```python
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
```

- [ ] **Step 2: 提交**

```bash
git add back-end/apps/merchant/views.py
git commit -m "feat: add merchant application view (GET+POST)"
```

---

### Task 5: 商品管理视图

**Files:**
- Modify: `back-end/apps/merchant/views.py`（追加）

- [ ] **Step 1: 追加 ProductListView（GET列表 + POST新增合并）和 ProductDetailView（GET详情 + PUT编辑合并）**

Django URL 匹配不区分 HTTP 方法，`/products` 需要合并 GET+POST，`/products/<pk>` 需要合并 GET+PUT。

```python
from django.shortcuts import get_object_or_404
from apps.merchant.serializers import (
    ProductSerializer, ProductWriteSerializer, ProductUpdateSerializer,
)


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
```

- [ ] **Step 2: 提交**

```bash
git add back-end/apps/merchant/views.py
git commit -m "feat: add merchant product list/detail views"
```

---

### Task 6: 库存管理视图

**Files:**
- Modify: `back-end/apps/merchant/views.py`（追加）

- [ ] **Step 1: 追加 3 个库存视图**

```python
from apps.merchant.serializers import (
    InventorySerializer, InventoryUpdateSerializer, InventoryRecordSerializer,
)


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
```

- [ ] **Step 2: 提交**

```bash
git add back-end/apps/merchant/views.py
git commit -m "feat: add merchant inventory views"
```

---

### Task 7: 发货管理视图

**Files:**
- Modify: `back-end/apps/merchant/views.py`（追加）

- [ ] **Step 1: 追加 3 个发货视图**

```python
from apps.merchant.serializers import (
    ShipmentTaskSerializer, ShipmentConfirmSerializer,
)


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
```

- [ ] **Step 2: 提交**

```bash
git add back-end/apps/merchant/views.py
git commit -m "feat: add merchant shipment views"
```

---

### Task 8: 工作台与记录查询视图

**Files:**
- Modify: `back-end/apps/merchant/views.py`（追加）

- [ ] **Step 1: 追加 Dashboard 和 Record 视图**

```python
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
```

- [ ] **Step 2: 提交**

```bash
git add back-end/apps/merchant/views.py
git commit -m "feat: add merchant dashboard and record views"
```

---

### Task 9: 商家端 URL 路由

**Files:**
- Modify: `back-end/apps/merchant/urls_merchant.py`

- [ ] **Step 1: 写入完整路由（合并视图使用单一 path）**

```python
from django.urls import path

from apps.merchant.views import (
    MerchantLoginView, MerchantInfoView,
    MerchantApplicationView,
    MerchantDashboardView,
    ProductListView, ProductDetailView,
    InventoryListView, InventoryUpdateView, InventoryRecordListView,
    ShipmentTaskListView, ShipmentTaskDetailView, ShipmentConfirmView,
    RecordListView,
)

urlpatterns = [
    # 认证
    path("login", MerchantLoginView.as_view(), name="merchant-login"),
    path("info", MerchantInfoView.as_view(), name="merchant-info"),
    # 入驻申请（GET 查状态 / POST 提交）
    path("application", MerchantApplicationView.as_view(), name="merchant-application"),
    # 工作台
    path("dashboard", MerchantDashboardView.as_view(), name="merchant-dashboard"),
    # 商品（GET 列表 / POST 新增）
    path("products", ProductListView.as_view(), name="merchant-product-list"),
    # 商品（GET 详情 / PUT 编辑）
    path("products/<int:pk>", ProductDetailView.as_view(), name="merchant-product-detail"),
    # 库存
    path("inventory", InventoryListView.as_view(), name="merchant-inventory-list"),
    path("inventory/records", InventoryRecordListView.as_view(), name="merchant-inventory-records"),
    path("inventory/<int:product_id>", InventoryUpdateView.as_view(), name="merchant-inventory-update"),
    # 发货
    path("shipments", ShipmentTaskListView.as_view(), name="merchant-shipment-list"),
    path("shipments/<int:pk>", ShipmentTaskDetailView.as_view(), name="merchant-shipment-detail"),
    path("shipments/<int:pk>/ship", ShipmentConfirmView.as_view(), name="merchant-shipment-confirm"),
    # 记录
    path("records", RecordListView.as_view(), name="merchant-records"),
]
```

每个 URL pattern 只出现一次，不会冲突。Django 的 `View.as_view()` 内部 `dispatch()` 根据 HTTP 方法自动路由到 `get()`/`post()`/`put()`。

- [ ] **Step 2: 验证路由无冲突**

```bash
cd back-end && python manage.py check
```

- [ ] **Step 3: 提交**

```bash
git add back-end/apps/merchant/urls_merchant.py
git commit -m "feat: add merchant URL routes"
```

---

### Task 10: 修复前端 ProductManage 过滤参数传递

**Files:**
- Modify: `front-end/src/views/merchant/ProductManage.vue`

- [ ] **Step 1: 修改 fetchList 调用，传入 status 和 keyword**

找到 `ProductManage.vue` 中调用 `productStore.fetchList()` 的位置（约第 119 行和筛选按钮处），改为传入参数：

```typescript
// 原代码（约第 119 行）:
productStore.fetchList()

// 改为:
productStore.fetchList({ status: statusFilter.value || undefined, keyword: searchKeyword.value || undefined })
```

同时删除客户端过滤的 computed（约第 85-90 行），因为过滤已在服务端完成。`filteredProducts` 直接返回 `productStore.list`：

```typescript
// 原代码（客户端过滤）:
const filteredProducts = computed(() => {
  return productStore.list.filter(...)
})

// 改为:
const filteredProducts = computed(() => productStore.list)
```

**注意**：具体行号和代码依赖实际文件内容，执行时以 Read 工具读取的实际文件为准进行调整。

- [ ] **Step 2: 在查询按钮点击时重新 fetch**

确保搜索按钮和状态筛选变更时触发 `fetchList` 并传入当前过滤参数。

- [ ] **Step 3: 提交**

```bash
git add front-end/src/views/merchant/ProductManage.vue
git commit -m "fix: pass filter params to API in ProductManage"
```

---

### Task 11: 修复前端 ShipmentTasks 过滤参数传递

**Files:**
- Modify: `front-end/src/views/merchant/ShipmentTasks.vue`

- [ ] **Step 1: 修改 fetchList 调用，传入 status 参数**

```typescript
// 原代码（约第 159 行）:
shipmentStore.fetchList()

// 改为:
shipmentStore.fetchList({ status: statusFilter.value || undefined })
```

删除客户端过滤的 computed（约第 122-125 行），`filteredTasks` 直接返回 `shipmentStore.list`。

- [ ] **Step 2: 状态筛选变更时重新 fetch**

确保状态筛选下拉变更时调用 `fetchList` 并传入当前 status 参数。

- [ ] **Step 3: 提交**

```bash
git add front-end/src/views/merchant/ShipmentTasks.vue
git commit -m "fix: pass filter params to API in ShipmentTasks"
```

---

### Task 12: 修复前端 RecordQuery 过滤参数传递

**Files:**
- Modify: `front-end/src/views/merchant/RecordQuery.vue`

- [ ] **Step 1: 修改 fetchList 调用，传入全部过滤参数**

```typescript
// 原代码（约第 77 行）:
recordStore.fetchList()

// 改为:
recordStore.fetchList({
  type: typeFilter.value || undefined,
  keyword: searchKeyword.value || undefined,
  startDate: dateRange.value?.[0] || undefined,
  endDate: dateRange.value?.[1] || undefined,
})
```

删除客户端过滤的 computed（约第 52-63 行），`filteredRecords` 直接返回 `recordStore.list`。

- [ ] **Step 2: 查询按钮重新 fetch**

确保点击查询按钮时调用带参数的 `fetchList`。

- [ ] **Step 3: 提交**

```bash
git add front-end/src/views/merchant/RecordQuery.vue
git commit -m "fix: pass filter params to API in RecordQuery"
```

---

### Task 13: 修复 Merchant 类型定义缺失字段

**Files:**
- Modify: `front-end/src/types/merchant.ts`

- [ ] **Step 1: 补充 businessScope 和 supplyDescription 字段**

```typescript
export interface Merchant {
  id: string
  name: string
  contactName: string
  phone: string
  email: string
  license: string
  businessScope: string       // 新增
  supplyDescription: string   // 新增
  status: 'pending' | 'approved' | 'rejected' | 'frozen'
  creditScore: number
  supplyCount: number
  violationCount: number
  reviewNote: string
  createdAt: string
  reviewedAt: string | null
}
```

- [ ] **Step 2: 提交**

```bash
git add front-end/src/types/merchant.ts
git commit -m "fix: add missing fields to Merchant type"
```

---

### 可选后续任务（不在本次计划范围内）

- 商家端 `merchant-request.ts` 无 401 自动刷新/重定向（对标用户端 `request.ts` 的 401 拦截器）
- 商家端退出时调用后端 logout 接口
- 商家端修改密码页面（前端 Profile 页目前只读）
- 管理端用户管理 API（`accounts/urls_admin.py` 仍为空）
- 管理端商家审核 API（`merchant/urls_admin.py` 仍为空）

---
