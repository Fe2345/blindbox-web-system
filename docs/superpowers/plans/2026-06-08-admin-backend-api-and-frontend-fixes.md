# Admin Backend API + Frontend Save Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the admin management backend APIs and fix two frontend save button bugs, so the admin panel is fully functional end-to-end.

**Architecture:** Follow the existing blindbox admin pattern: `CSRFExemptView` + `IsAdmin` permission + `success()`/`error()` response helpers + `keys_to_camel`/`keys_to_snake` serializer transforms. Frontend fixes wire existing API functions through store actions to Vue dialog save buttons.

**Tech Stack:** Django REST Framework (backend), Vue 3 + Pinia + Element Plus (frontend)

---

## File Structure

### Frontend files to modify:
- `front-end/src/stores/admin/product.ts` -- add `save` and `update` actions
- `front-end/src/stores/admin/blindbox.ts` -- add `save` and `update` actions
- `front-end/src/views/admin/ProductTemplate.vue` -- wire save button to store
- `front-end/src/views/admin/BlindBoxConfig.vue` -- wire save button to store

### Backend files to create/modify:
- `back-end/apps/accounts/serializers.py` -- add admin serializers
- `back-end/apps/accounts/views.py` -- add admin views
- `back-end/apps/accounts/urls_admin.py` -- add admin routes
- `back-end/apps/merchant/serializers.py` -- add admin serializers
- `back-end/apps/merchant/views.py` -- add admin views
- `back-end/apps/merchant/urls_admin.py` -- add admin routes
- `back-end/apps/orders/serializers.py` -- add admin serializer
- `back-end/apps/orders/views.py` -- add admin views
- `back-end/apps/orders/urls_admin.py` -- add admin routes
- `back-end/apps/operations/serializers.py` -- create with all serializers
- `back-end/apps/operations/views.py` -- create with all views
- `back-end/apps/operations/urls.py` -- add admin routes

---

## Task 1: Fix ProductTemplate Save Button

**Files:**
- Modify: `front-end/src/stores/admin/product.ts`
- Modify: `front-end/src/views/admin/ProductTemplate.vue`

### Step 1: Add save/update actions to product store

In `front-end/src/stores/admin/product.ts`, add two new functions and export them:

```ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Product } from '@/types/product'
import * as api from '@/api/admin/product'

export const useProductStore = defineStore('product', () => {
  const list = ref<Product[]>([])

  async function fetchList() {
    const res: any = await api.getProductList()
    if (res.code === 200) list.value = res.data
    return res
  }

  async function review(id: string, action: string, note: string) {
    const res: any = await api.reviewProduct(id, { action, note })
    if (res.code === 200) await fetchList()
    return res
  }

  async function save(data: any) {
    const res: any = await api.saveProduct(data)
    if (res.code === 200) await fetchList()
    return res
  }

  async function update(id: string, data: any) {
    const res: any = await api.updateProduct(id, data)
    if (res.code === 200) await fetchList()
    return res
  }

  async function offline(id: string) {
    const res: any = await api.offlineProduct(id)
    if (res.code === 200) await fetchList()
    return res
  }

  return { list, fetchList, review, save, update, offline }
})
```

### Step 2: Wire save button in ProductTemplate.vue

In `front-end/src/views/admin/ProductTemplate.vue`, replace the script section to add a `handleSave` function and wire the button:

Change line 51 from:
```html
<el-button type="primary" @click="dialogVisible = false">保存</el-button>
```
to:
```html
<el-button type="primary" @click="handleSave">保存</el-button>
```

Add `handleSave` function after `showEdit` (after line 75):

```ts
async function handleSave() {
  if (!form.value.name || !form.value.category) {
    ElMessage.warning('请填写商品名称和分类')
    return
  }
  let res
  if (isEdit.value) {
    res = await productStore.update(form.value.id, form.value)
  } else {
    res = await productStore.save(form.value)
  }
  if (res.code === 200) {
    ElMessage.success(isEdit.value ? '修改成功' : '添加成功')
    dialogVisible.value = false
  }
}
```

Also add `id` to the form ref type (line 67) to support edit mode:
```ts
const form = ref({ id: '', name: '', category: '', rarity: 'N', description: '', stock: 0, estimatedPoints: 0 })
```

And update `showAdd` to include `id: ''`:
```ts
function showAdd() { isEdit.value = false; form.value = { id: '', name: '', category: '', rarity: 'N', description: '', stock: 0, estimatedPoints: 0 }; dialogVisible.value = true }
```

### Step 3: Verify the fix

Run the frontend dev server and test:
- Click "新增商品" -> fill form -> click "保存" -> dialog closes, list refreshes
- Click "编辑" on a row -> modify fields -> click "保存" -> dialog closes, list refreshes

---

## Task 2: Fix BlindBoxConfig Save Button

**Files:**
- Modify: `front-end/src/stores/admin/blindbox.ts`
- Modify: `front-end/src/views/admin/BlindBoxConfig.vue`

### Step 1: Add save/update actions to blindbox store

In `front-end/src/stores/admin/blindbox.ts`, add two new functions:

```ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AdminBlindBox } from '@/types/blindbox'
import * as api from '@/api/admin/blindbox'

export const useBlindBoxStore = defineStore('blindbox', () => {
  const list = ref<AdminBlindBox[]>([])

  async function fetchList() {
    const res: any = await api.getBlindBoxList()
    if (res.code === 200) list.value = res.data
    return res
  }

  async function save(data: any) {
    const res: any = await api.saveBlindBox(data)
    if (res.code === 200) await fetchList()
    return res
  }

  async function update(id: string, data: any) {
    const res: any = await api.updateBlindBox(id, data)
    if (res.code === 200) await fetchList()
    return res
  }

  async function updateStatus(id: string, status: string) {
    const res: any = await api.updateBlindBoxStatus(id, status)
    if (res.code === 200) await fetchList()
    return res
  }

  async function savePrizePool(blindboxId: string, prizes: any[]) {
    const res: any = await api.savePrizePool(blindboxId, prizes)
    if (res.code === 200) await fetchList()
    return res
  }

  return { list, fetchList, save, update, updateStatus, savePrizePool }
})
```

### Step 2: Wire save button in BlindBoxConfig.vue

Change line 43 from:
```html
<el-button type="primary" @click="dialogVisible = false">保存</el-button>
```
to:
```html
<el-button type="primary" @click="handleSave">保存</el-button>
```

Add `handleSave` function after `showEdit` (after line 60):

```ts
async function handleSave() {
  if (!form.value.name || !form.value.category) {
    ElMessage.warning('请填写盲盒名称和分类')
    return
  }
  const payload = {
    ...form.value,
    startTime: form.value.dateRange?.[0] || null,
    endTime: form.value.dateRange?.[1] || null,
  }
  delete payload.dateRange
  let res
  if (isEdit.value) {
    res = await blindBoxStore.update(form.value.id, payload)
  } else {
    res = await blindBoxStore.save(payload)
  }
  if (res.code === 200) {
    ElMessage.success(isEdit.value ? '修改成功' : '添加成功')
    dialogVisible.value = false
  }
}
```

Add `id` to the form ref (line 57):
```ts
const form = ref({ id: '', name: '', category: '', description: '', costPoints: 100, maxDrawCount: 10, dateRange: null })
```

Update `showAdd` (line 59):
```ts
function showAdd() { isEdit.value = false; form.value = { id: '', name: '', category: '', description: '', costPoints: 100, maxDrawCount: 10, dateRange: null }; dialogVisible.value = true }
```

### Step 3: Verify

Same verification pattern as Task 1.

---

## Task 3: Backend -- User Management Admin APIs

**Files:**
- Modify: `back-end/apps/accounts/serializers.py` (append admin serializers)
- Modify: `back-end/apps/accounts/views.py` (append admin views)
- Modify: `back-end/apps/accounts/urls_admin.py` (add routes)

### Step 1: Add admin serializers to accounts/serializers.py

Append at the end of the file:

```python
# ==================== 管理端 ====================


class AdminUserSerializer(serializers.ModelSerializer):
    """用户列表序列化器（管理端）"""

    class Meta:
        model = User
        fields = ["id", "username", "phone", "role", "is_active", "date_joined", "last_login"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = keys_to_camel(data)
        # 附加统计字段
        data["avatar"] = instance.avatar
        return data


class AdminUserStatusSerializer(serializers.Serializer):
    """用户状态切换序列化器"""

    is_active = serializers.BooleanField()
```

Make sure `User` is imported at the top of the file (it already is via `from .models import User, Division, Address`).

### Step 2: Add admin views to accounts/views.py

Append at the end of the file:

```python
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
```

Make sure these imports exist at the top of `accounts/views.py`:
- `from django.db import models` (for `models.Q`)
- `from apps.common.permissions import IsAdmin` (check if already imported)
- `from apps.common.views import CSRFExemptView` (check if already imported)

### Step 3: Add routes to accounts/urls_admin.py

Replace the entire file content:

```python
from django.urls import path

from . import views

urlpatterns = [
    path("users", views.AdminUserListView.as_view(), name="admin-user-list"),
    path("users/<int:pk>/status", views.AdminUserStatusView.as_view(), name="admin-user-status"),
]
```

### Step 4: Verify

Run: `cd back-end && python manage.py check`
Expected: No errors

---

## Task 4: Backend -- Merchant Management Admin APIs

**Files:**
- Modify: `back-end/apps/merchant/serializers.py` (append admin serializers)
- Modify: `back-end/apps/merchant/views.py` (append admin views)
- Modify: `back-end/apps/merchant/urls_admin.py` (add routes)

### Step 1: Add admin serializers to merchant/serializers.py

Append at the end of the file:

```python
# ==================== 管理端 ====================


class AdminMerchantSerializer(serializers.ModelSerializer):
    """商家列表序列化器（管理端）"""

    class Meta:
        model = Merchant
        fields = [
            "id", "name", "contact_name", "phone", "email", "license",
            "status", "credit_score", "review_note", "reviewed_at",
            "created_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = keys_to_camel(data)
        # 附加统计
        data["supplyCount"] = instance.products.count()
        data["violationCount"] = 0  # TODO: 后续接入违规记录
        return data


class AdminMerchantReviewSerializer(serializers.Serializer):
    """商家审核序列化器"""

    action = serializers.ChoiceField(choices=["approve", "reject"])
    note = serializers.CharField(required=False, allow_blank=True, default="")


class AdminMerchantStatusSerializer(serializers.Serializer):
    """商家状态切换序列化器"""

    status = serializers.ChoiceField(choices=Merchant.Status.choices)


class AdminProductSerializer(serializers.ModelSerializer):
    """商品列表序列化器（管理端）"""

    merchantName = serializers.CharField(source="merchant.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "image", "category", "rarity", "description",
            "estimated_points", "status", "review_note",
            "merchantName", "created_at",
        ]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))


class AdminProductReviewSerializer(serializers.Serializer):
    """商品审核序列化器"""

    action = serializers.ChoiceField(choices=["approve", "reject"])
    note = serializers.CharField(required=False, allow_blank=True, default="")
```

### Step 2: Add admin views to merchant/views.py

Append at the end of the file:

```python
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
        merchant.save()
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
        product.save()
        return success(data=AdminProductSerializer(product).data)
```

Make sure these imports exist at the top of `merchant/views.py`:
- `from django.utils import timezone`
- `from apps.common.permissions import IsAdmin`
- `from apps.common.views import CSRFExemptView`
- `from apps.common.response import success, error, flatten_errors`

### Step 3: Add routes to merchant/urls_admin.py

Replace the entire file content:

```python
from django.urls import path

from . import views

urlpatterns = [
    path("merchants", views.AdminMerchantListView.as_view(), name="admin-merchant-list"),
    path("merchants/<int:pk>/review", views.AdminMerchantReviewView.as_view(), name="admin-merchant-review"),
    path("merchants/<int:pk>/status", views.AdminMerchantStatusView.as_view(), name="admin-merchant-status"),
    path("products", views.AdminProductListView.as_view(), name="admin-product-list"),
    path("products/<int:pk>/review", views.AdminProductReviewView.as_view(), name="admin-product-review"),
]
```

### Step 4: Verify

Run: `cd back-end && python manage.py check`
Expected: No errors

---

## Task 5: Backend -- Order Management Admin APIs

**Files:**
- Modify: `back-end/apps/orders/serializers.py` (append admin serializer)
- Modify: `back-end/apps/orders/views.py` (append admin views)
- Modify: `back-end/apps/orders/urls_admin.py` (add routes)

### Step 1: Add admin serializer to orders/serializers.py

Append at the end of the file:

```python
# ==================== 管理端 ====================


class AdminOrderSerializer(serializers.ModelSerializer):
    """订单列表序列化器（管理端）"""

    orderNo = serializers.CharField(source="order_no", read_only=True)
    assetName = serializers.CharField(source="asset_name", read_only=True)
    assetImage = serializers.CharField(source="asset_image", read_only=True)
    userName = serializers.CharField(source="user.username", read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    shippedAt = serializers.DateTimeField(source="shipped_at", read_only=True)
    completedAt = serializers.DateTimeField(source="completed_at", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "orderNo", "type", "assetName", "assetImage",
            "status", "userName",
            "receiver_name", "receiver_phone", "receiver_address",
            "logistics_company", "tracking_no",
            "createdAt", "shippedAt", "completedAt",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return keys_to_camel(data)


class AdminOrderShipSerializer(serializers.Serializer):
    """订单发货序列化器"""

    logistics_company = serializers.CharField(max_length=100)
    tracking_no = serializers.CharField(max_length=100)
```

Make sure `keys_to_camel` is imported at the top of the file.

### Step 2: Add admin views to orders/views.py

Append at the end of the file:

```python
# ==================== 管理端 ====================


class AdminOrderListView(CSRFExemptView):
    """订单列表（管理端）"""

    permission_classes = [IsAdmin]

    def get(self, request):
        qs = Order.objects.select_related("user").all().order_by("-created_at")
        status = request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        order_type = request.query_params.get("type")
        if order_type:
            qs = qs.filter(type=order_type)
        return success(data=AdminOrderSerializer(qs[:100], many=True).data)


class AdminOrderShipView(CSRFExemptView):
    """订单发货（管理端）"""

    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, status="pending")
        except Order.DoesNotExist:
            return error(message="订单不存在或不在待处理状态", http_status=404)

        serializer = AdminOrderShipSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        order.logistics_company = serializer.validated_data["logistics_company"]
        order.tracking_no = serializer.validated_data["tracking_no"]
        order.shipped_at = timezone.now()
        order.status = "shipped"
        order.save()
        return success(data=AdminOrderSerializer(order).data)
```

Make sure these imports exist at the top of `orders/views.py`:
- `from django.utils import timezone`
- `from apps.common.permissions import IsAdmin`
- `from apps.common.views import CSRFExemptView`
- `from apps.common.response import success, error, flatten_errors`

### Step 3: Add routes to orders/urls_admin.py

Replace the entire file content:

```python
from django.urls import path

from . import views

urlpatterns = [
    path("orders", views.AdminOrderListView.as_view(), name="admin-order-list"),
    path("orders/<int:pk>/ship", views.AdminOrderShipView.as_view(), name="admin-order-ship"),
]
```

### Step 4: Verify

Run: `cd back-end && python manage.py check`
Expected: No errors

---

## Task 6: Backend -- Operations / System Config Admin APIs

**Files:**
- Create/Modify: `back-end/apps/operations/serializers.py` (currently empty)
- Create/Modify: `back-end/apps/operations/views.py` (currently empty)
- Modify: `back-end/apps/operations/urls.py` (currently empty)

### Step 1: Write serializers in operations/serializers.py

Write the full file:

```python
from rest_framework import serializers

from apps.common.utils import keys_to_camel

from .models import RuleConfig, OpLog, ExceptionRecord, TransactionLedger


class RuleConfigSerializer(serializers.ModelSerializer):
    """规则配置序列化器"""

    class Meta:
        model = RuleConfig
        fields = [
            "recycle_rate", "new_user_points", "max_draw_per_day",
            "min_points_to_draw", "order_auto_confirm_days",
            "exchange_lock_hours", "updated_by", "updated_at",
        ]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))


class RuleConfigWriteSerializer(serializers.Serializer):
    """规则配置写入序列化器"""

    recycle_rate = serializers.IntegerField(min_value=0, max_value=100, required=False)
    new_user_points = serializers.IntegerField(min_value=0, required=False)
    max_draw_per_day = serializers.IntegerField(min_value=1, required=False)
    min_points_to_draw = serializers.IntegerField(min_value=0, required=False)
    order_auto_confirm_days = serializers.IntegerField(min_value=1, required=False)
    exchange_lock_hours = serializers.IntegerField(min_value=1, required=False)

    def to_internal_value(self, data):
        from apps.common.utils import keys_to_snake
        return super().to_internal_value(keys_to_snake(data))


class OpLogSerializer(serializers.ModelSerializer):
    """操作日志序列化器"""

    class Meta:
        model = OpLog
        fields = ["id", "operator", "action", "target", "detail", "created_at"]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))


class ExceptionRecordSerializer(serializers.ModelSerializer):
    """异常工单序列化器"""

    class Meta:
        model = ExceptionRecord
        fields = [
            "id", "type", "description", "related_id",
            "status", "result", "resolved_at", "created_at",
        ]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))


class ExceptionResolveSerializer(serializers.Serializer):
    """异常工单处理序列化器"""

    result = serializers.CharField()


class TransactionLedgerSerializer(serializers.ModelSerializer):
    """交易账本序列化器"""

    class Meta:
        model = TransactionLedger
        fields = ["id", "type", "description", "amount", "created_at"]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))
```

### Step 2: Write views in operations/views.py

Write the full file:

```python
from django.utils import timezone

from apps.common.views import CSRFExemptView
from apps.common.permissions import IsAdmin
from apps.common.response import success, error, flatten_errors

from .models import RuleConfig, OpLog, ExceptionRecord, TransactionLedger
from .serializers import (
    RuleConfigSerializer,
    RuleConfigWriteSerializer,
    OpLogSerializer,
    ExceptionRecordSerializer,
    ExceptionResolveSerializer,
    TransactionLedgerSerializer,
)


class AdminRuleConfigView(CSRFExemptView):
    """规则配置（管理端）"""

    permission_classes = [IsAdmin]

    def get(self, request):
        config = RuleConfig.get()
        return success(data=RuleConfigSerializer(config).data)

    def post(self, request):
        config = RuleConfig.get()
        serializer = RuleConfigWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        for field, value in serializer.validated_data.items():
            setattr(config, field, value)
        config.updated_by = request.user.username
        config.save()
        return success(data=RuleConfigSerializer(config).data)


class AdminOpLogListView(CSRFExemptView):
    """操作日志列表（管理端）"""

    permission_classes = [IsAdmin]

    def get(self, request):
        qs = OpLog.objects.all().order_by("-created_at")[:100]
        return success(data=OpLogSerializer(qs, many=True).data)


class AdminExceptionListView(CSRFExemptView):
    """异常工单列表（管理端）"""

    permission_classes = [IsAdmin]

    def get(self, request):
        qs = ExceptionRecord.objects.all().order_by("-created_at")
        status = request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return success(data=ExceptionRecordSerializer(qs[:100], many=True).data)


class AdminExceptionResolveView(CSRFExemptView):
    """异常工单处理（管理端）"""

    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            record = ExceptionRecord.objects.get(pk=pk)
        except ExceptionRecord.DoesNotExist:
            return error(message="工单不存在", http_status=404)

        if record.status == "resolved":
            return error(message="工单已解决", http_status=400)

        serializer = ExceptionResolveSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), http_status=400)

        record.result = serializer.validated_data["result"]
        record.status = "resolved"
        record.resolved_at = timezone.now()
        record.save()
        return success(data=ExceptionRecordSerializer(record).data)


class AdminLedgerListView(CSRFExemptView):
    """交易账本列表（管理端）"""

    permission_classes = [IsAdmin]

    def get(self, request):
        qs = TransactionLedger.objects.all().order_by("-created_at")
        ledger_type = request.query_params.get("type")
        if ledger_type:
            qs = qs.filter(type=ledger_type)
        start_date = request.query_params.get("start_date")
        if start_date:
            qs = qs.filter(created_at__date__gte=start_date)
        end_date = request.query_params.get("end_date")
        if end_date:
            qs = qs.filter(created_at__date__lte=end_date)
        return success(data=TransactionLedgerSerializer(qs[:200], many=True).data)
```

### Step 3: Write routes in operations/urls.py

Replace the entire file content:

```python
from django.urls import path

from . import views

urlpatterns = [
    path("rules", views.AdminRuleConfigView.as_view(), name="admin-rule-config"),
    path("logs", views.AdminOpLogListView.as_view(), name="admin-op-log"),
    path("exceptions", views.AdminExceptionListView.as_view(), name="admin-exception-list"),
    path("exceptions/<int:pk>/resolve", views.AdminExceptionResolveView.as_view(), name="admin-exception-resolve"),
    path("ledger", views.AdminLedgerListView.as_view(), name="admin-ledger"),
]
```

### Step 4: Verify

Run: `cd back-end && python manage.py check`
Expected: No errors

---

## Task 7: Final Verification

### Step 1: Run Django system check

```bash
cd back-end && python manage.py check
```

Expected: `System check identified no issues (0 silenced).`

### Step 2: Check for pending migrations

```bash
cd back-end && python manage.py makemigrations --check --dry-run
```

Expected: No new migrations needed (all models already exist).

### Step 3: Run frontend build check

```bash
cd front-end && npm run build 2>&1 | tail -20
```

Expected: Build succeeds without errors.

### Step 4: Start dev server and test admin login

```bash
cd front-end && npm run dev
```

Navigate to `http://localhost:5173/admin`, login with admin/admin123, verify:
- Dashboard loads
- Product template save works (add + edit)
- Blind box config save works (add + edit)
- All pages load without errors

---

## Commit Strategy

After each task, commit with a descriptive message:

```bash
# Task 1-2: Frontend fixes
git add front-end/src/stores/admin/product.ts front-end/src/stores/admin/blindbox.ts front-end/src/views/admin/ProductTemplate.vue front-end/src/views/admin/BlindBoxConfig.vue
git commit -m "fix: wire admin product and blindbox save buttons to API"

# Task 3: User management
git add back-end/apps/accounts/serializers.py back-end/apps/accounts/views.py back-end/apps/accounts/urls_admin.py
git commit -m "feat: add admin user management API (list + status toggle)"

# Task 4: Merchant management
git add back-end/apps/merchant/serializers.py back-end/apps/merchant/views.py back-end/apps/merchant/urls_admin.py
git commit -m "feat: add admin merchant and product review API"

# Task 5: Order management
git add back-end/apps/orders/serializers.py back-end/apps/orders/views.py back-end/apps/orders/urls_admin.py
git commit -m "feat: add admin order management API (list + ship)"

# Task 6: Operations
git add back-end/apps/operations/serializers.py back-end/apps/operations/views.py back-end/apps/operations/urls.py
git commit -m "feat: add admin operations API (rules, logs, exceptions, ledger)"
```
