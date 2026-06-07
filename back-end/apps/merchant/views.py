import logging

from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import Q, Sum
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from apps.common.permissions import IsAuthenticated
from apps.common.response import error, flatten_errors, paginated, success

from .models import Inventory, InventoryRecord, Merchant, Product, ShipmentTask
from .permissions import IsMerchant
from .serializers import (
    InventoryListSerializer,
    InventoryRecordSerializer,
    InventoryUpdateSerializer,
    MerchantApplicationSerializer,
    MerchantInfoSerializer,
    OperationRecordSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ProductWriteSerializer,
    ShipmentDetailSerializer,
    ShipmentListSerializer,
    ShipmentShipSerializer,
)

logger = logging.getLogger("blindbox")


# ==================== 商家登录 ====================


class MerchantLoginView(APIView):
    """商家登录"""

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return error(message="请输入用户名和密码", code=400)

        user = authenticate(username=username, password=password)
        if user is None:
            return error(message="用户名或密码错误", code=401)

        if not user.is_active:
            return error(message="账号已被禁用", code=403)

        # 检查是否有商家身份
        try:
            merchant = user.merchant
        except Merchant.DoesNotExist:
            return error(message="该账号不是商家账号", code=403)

        token, _ = Token.objects.get_or_create(user=user)
        logger.info(f"商家登录: {username}")

        return success(data={
            "token": token.key,
            "merchant": MerchantInfoSerializer(merchant).data,
        })


# ==================== 商家信息 ====================


class MerchantInfoView(APIView):
    """商家信息查询"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        merchant = request.user.merchant
        return success(data=MerchantInfoSerializer(merchant).data)


class MerchantApplicationView(APIView):
    """商家入驻申请"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """查询当前用户的入驻申请状态"""
        try:
            merchant = request.user.merchant
            return success(data=MerchantInfoSerializer(merchant).data)
        except Merchant.DoesNotExist:
            return success(data=None)

    def post(self, request):
        """提交入驻申请"""
        # 已有商家信息则不能重复申请
        if hasattr(request.user, "merchant"):
            merchant = request.user.merchant
            if merchant.status == Merchant.Status.APPROVED:
                return error(message="您已是认证商家，无需重复申请", code=400)
            if merchant.status == Merchant.Status.PENDING:
                return error(message="您已有待审核的申请，请耐心等待", code=400)
            if merchant.status == Merchant.Status.FROZEN:
                return error(message="您的商家账号已被冻结，无法重新申请", code=400)
            # 被驳回可以重新申请
            serializer = MerchantApplicationSerializer(data=request.data)
            if not serializer.is_valid():
                return error(message=flatten_errors(serializer.errors), code=400)
            data = serializer.validated_data
            for key, value in data.items():
                setattr(merchant, key, value)
            merchant.status = Merchant.Status.PENDING
            merchant.review_note = ""
            merchant.reviewed_at = None
            merchant.save()
            return success(data=MerchantInfoSerializer(merchant).data)

        serializer = MerchantApplicationSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), code=400)

        data = serializer.validated_data
        merchant = Merchant.objects.create(
            user=request.user,
            name=data["name"],
            contact_name=data["contact_name"],
            phone=data["phone"],
            email=data.get("email", ""),
            license=data.get("license", ""),
            business_scope=data.get("business_scope", ""),
            supply_desc=data.get("supply_desc", ""),
            status=Merchant.Status.PENDING,
        )
        logger.info(f"商家入驻申请提交: user={request.user.id}, merchant={merchant.id}")
        return success(data=MerchantInfoSerializer(merchant).data)


# ==================== 工作台 ====================


class MerchantDashboardView(APIView):
    """商户工作台"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        merchant = request.user.merchant

        # 统计数据
        total_products = Product.objects.filter(merchant=merchant).count()
        pending_products = Product.objects.filter(
            merchant=merchant, status=Product.Status.PENDING
        ).count()
        approved_products = Product.objects.filter(
            merchant=merchant, status=Product.Status.APPROVED
        )

        # 库存不足商品数（库存低于 10）
        low_stock_products = Inventory.objects.filter(
            product__in=approved_products, current_stock__lt=10
        ).count()

        # 待发货任务数
        pending_shipments = ShipmentTask.objects.filter(
            product__merchant=merchant, status=ShipmentTask.Status.PENDING
        ).count()

        # 总库存数
        total_stock = Inventory.objects.filter(
            product__in=approved_products
        ).aggregate(total=Sum("current_stock"))["total"] or 0

        # 待办事项
        todos = []
        if pending_products > 0:
            todos.append({
                "id": "pending_products",
                "title": f"有 {pending_products} 个商品待审核",
                "link": "/products",
            })
        if low_stock_products > 0:
            todos.append({
                "id": "low_stock",
                "title": f"有 {low_stock_products} 个商品库存不足",
                "link": "/inventory",
            })
        if pending_shipments > 0:
            todos.append({
                "id": "pending_shipments",
                "title": f"有 {pending_shipments} 个发货任务待处理",
                "link": "/shipments",
            })

        return success(data={
            "totalProducts": total_products,
            "pendingProducts": pending_products,
            "lowStockProducts": low_stock_products,
            "pendingShipments": pending_shipments,
            "totalStock": total_stock,
            "todos": todos,
        })


# ==================== 商品管理 ====================


class ProductListView(APIView):
    """商品列表"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        merchant = request.user.merchant
        qs = Product.objects.filter(merchant=merchant)

        # 筛选
        status = request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)

        category = request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)

        rarity = request.query_params.get("rarity")
        if rarity:
            qs = qs.filter(rarity=rarity)

        keyword = request.query_params.get("keyword")
        if keyword:
            qs = qs.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))

        # 排序
        order_by = request.query_params.get("order_by", "-created_at")
        if order_by in ["created_at", "-created_at", "name", "-name", "estimated_points", "-estimated_points"]:
            qs = qs.order_by(order_by)

        # 分页
        page_size = min(int(request.query_params.get("page_size", 10)), 100)
        page = int(request.query_params.get("page", 1))
        total = qs.count()
        start = (page - 1) * page_size
        items = qs[start:start + page_size]

        return success(data={
            "count": total,
            "page": page,
            "page_size": page_size,
            "results": ProductListSerializer(items, many=True).data,
        })


class ProductDetailView(APIView):
    """商品详情"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request, pk):
        merchant = request.user.merchant
        try:
            product = Product.objects.get(pk=pk, merchant=merchant)
        except Product.DoesNotExist:
            return error(message="商品不存在", code=404)
        return success(data=ProductDetailSerializer(product).data)


class ProductSubmitView(APIView):
    """新增商品"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def post(self, request):
        merchant = request.user.merchant
        if merchant.status != Merchant.Status.APPROVED:
            return error(message="商家未通过审核，无法提交商品", code=403)

        serializer = ProductWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), code=400)

        data = serializer.validated_data
        with transaction.atomic():
            product = Product.objects.create(
                merchant=merchant,
                name=data["name"],
                image=data["image"],
                category=data["category"],
                rarity=data["rarity"],
                description=data.get("description", ""),
                estimated_points=data.get("estimated_points", 0),
                status=Product.Status.PENDING,
            )
            # 自动创建库存记录
            Inventory.objects.create(product=product, current_stock=0)

        logger.info(f"商家提交商品: merchant={merchant.id}, product={product.id}")
        return success(data=ProductDetailSerializer(product).data)


class ProductEditView(APIView):
    """修改商品"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def put(self, request, pk):
        merchant = request.user.merchant
        try:
            product = Product.objects.get(pk=pk, merchant=merchant)
        except Product.DoesNotExist:
            return error(message="商品不存在", code=404)

        # 只有待审核和已驳回的商品可以修改
        if product.status not in [Product.Status.PENDING, Product.Status.REJECTED]:
            return error(message="当前状态不允许修改商品", code=400)

        serializer = ProductWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), code=400)

        data = serializer.validated_data
        product.name = data["name"]
        product.image = data["image"]
        product.category = data["category"]
        product.rarity = data["rarity"]
        product.description = data.get("description", "")
        product.estimated_points = data.get("estimated_points", 0)
        # 如果是被驳回重新编辑，状态改回待审核
        if product.status == Product.Status.REJECTED:
            product.status = Product.Status.PENDING
            product.review_note = ""
        product.save()

        logger.info(f"商家修改商品: merchant={merchant.id}, product={product.id}")
        return success(data=ProductDetailSerializer(product).data)


# ==================== 库存管理 ====================


class InventoryListView(APIView):
    """库存列表"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        merchant = request.user.merchant
        qs = Inventory.objects.filter(product__merchant=merchant)

        # 筛选
        keyword = request.query_params.get("keyword")
        if keyword:
            qs = qs.filter(
                Q(product__name__icontains=keyword) |
                Q(product__category__icontains=keyword)
            )

        # 库存状态筛选
        stock_status = request.query_params.get("stock_status")
        if stock_status == "low":
            qs = qs.filter(current_stock__lt=10)
        elif stock_status == "out":
            qs = qs.filter(current_stock=0)
        elif stock_status == "normal":
            qs = qs.filter(current_stock__gte=10)

        # 排序
        order_by = request.query_params.get("order_by", "-updated_at")
        if order_by in ["current_stock", "-current_stock", "updated_at", "-updated_at"]:
            qs = qs.order_by(order_by)

        # 分页
        page_size = min(int(request.query_params.get("page_size", 10)), 100)
        page = int(request.query_params.get("page", 1))
        total = qs.count()
        start = (page - 1) * page_size
        items = qs[start:start + page_size]

        return success(data={
            "count": total,
            "page": page,
            "page_size": page_size,
            "results": InventoryListSerializer(items, many=True).data,
        })


class InventoryUpdateView(APIView):
    """修改库存"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def put(self, request, pk):
        merchant = request.user.merchant
        try:
            inventory = Inventory.objects.select_related("product").get(
                pk=pk, product__merchant=merchant
            )
        except Inventory.DoesNotExist:
            return error(message="库存记录不存在", code=404)

        # 只有已通过的商品可以修改库存
        if inventory.product.status != Product.Status.APPROVED:
            return error(message="商品未通过审核，无法修改库存", code=400)

        serializer = InventoryUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), code=400)

        data = serializer.validated_data
        change_type = data["change_type"]
        quantity = data["quantity"]
        reason = data.get("reason", "")

        before_stock = inventory.current_stock

        with transaction.atomic():
            if change_type == InventoryRecord.ChangeType.INCREASE:
                after_stock = before_stock + quantity
            elif change_type == InventoryRecord.ChangeType.DECREASE:
                if quantity > before_stock:
                    return error(message="出库数量不能大于当前库存", code=400)
                after_stock = before_stock - quantity
            else:  # MODIFY
                after_stock = quantity

            inventory.current_stock = after_stock
            inventory.save(update_fields=["current_stock", "updated_at"])

            # 记录变动
            InventoryRecord.objects.create(
                product=inventory.product,
                type=change_type,
                before_stock=before_stock,
                after_stock=after_stock,
                reason=reason,
            )

        logger.info(
            f"商家修改库存: merchant={merchant.id}, product={inventory.product.id}, "
            f"type={change_type}, before={before_stock}, after={after_stock}"
        )
        return success(data=InventoryListSerializer(inventory).data)


class InventoryRecordListView(APIView):
    """库存变动记录"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        merchant = request.user.merchant
        qs = InventoryRecord.objects.filter(product__merchant=merchant)

        # 筛选
        product_id = request.query_params.get("product_id")
        if product_id:
            qs = qs.filter(product_id=product_id)

        change_type = request.query_params.get("type")
        if change_type:
            qs = qs.filter(type=change_type)

        # 时间范围
        start_date = request.query_params.get("start_date")
        if start_date:
            qs = qs.filter(created_at__date__gte=start_date)

        end_date = request.query_params.get("end_date")
        if end_date:
            qs = qs.filter(created_at__date__lte=end_date)

        # 分页
        page_size = min(int(request.query_params.get("page_size", 10)), 100)
        page = int(request.query_params.get("page", 1))
        total = qs.count()
        start = (page - 1) * page_size
        items = qs[start:start + page_size]

        return success(data={
            "count": total,
            "page": page,
            "page_size": page_size,
            "results": InventoryRecordSerializer(items, many=True).data,
        })


# ==================== 发货管理 ====================


class ShipmentListView(APIView):
    """发货任务列表"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        merchant = request.user.merchant
        qs = ShipmentTask.objects.filter(product__merchant=merchant)

        # 筛选
        status = request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)

        keyword = request.query_params.get("keyword")
        if keyword:
            qs = qs.filter(
                Q(task_no__icontains=keyword) |
                Q(order_no__icontains=keyword) |
                Q(receiver_name__icontains=keyword)
            )

        # 排序
        order_by = request.query_params.get("order_by", "-created_at")
        if order_by in ["created_at", "-created_at", "shipped_at", "-shipped_at"]:
            qs = qs.order_by(order_by)

        # 分页
        page_size = min(int(request.query_params.get("page_size", 10)), 100)
        page = int(request.query_params.get("page", 1))
        total = qs.count()
        start = (page - 1) * page_size
        items = qs[start:start + page_size]

        return success(data={
            "count": total,
            "page": page,
            "page_size": page_size,
            "results": ShipmentListSerializer(items, many=True).data,
        })


class ShipmentDetailView(APIView):
    """发货任务详情"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request, pk):
        merchant = request.user.merchant
        try:
            shipment = ShipmentTask.objects.select_related("product").get(
                pk=pk, product__merchant=merchant
            )
        except ShipmentTask.DoesNotExist:
            return error(message="发货任务不存在", code=404)
        return success(data=ShipmentDetailSerializer(shipment).data)


class ShipmentShipView(APIView):
    """执行发货"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def post(self, request, pk):
        merchant = request.user.merchant
        try:
            shipment = ShipmentTask.objects.select_related("product").get(
                pk=pk, product__merchant=merchant
            )
        except ShipmentTask.DoesNotExist:
            return error(message="发货任务不存在", code=404)

        if shipment.status != ShipmentTask.Status.PENDING:
            return error(message="该任务已发货，不可重复操作", code=400)

        serializer = ShipmentShipSerializer(data=request.data)
        if not serializer.is_valid():
            return error(message=flatten_errors(serializer.errors), code=400)

        data = serializer.validated_data

        with transaction.atomic():
            shipment.logistics_company = data["logistics_company"]
            shipment.tracking_no = data["tracking_no"]
            shipment.status = ShipmentTask.Status.SHIPPED
            shipment.shipped_at = timezone.now()
            shipment.save()

            # 扣减库存
            try:
                inventory = Inventory.objects.select_for_update().get(
                    product=shipment.product
                )
                if inventory.current_stock <= 0:
                    raise error(message="库存不足，无法发货", code=400)

                before_stock = inventory.current_stock
                inventory.current_stock -= 1
                inventory.save(update_fields=["current_stock", "updated_at"])

                InventoryRecord.objects.create(
                    product=shipment.product,
                    type=InventoryRecord.ChangeType.DECREASE,
                    before_stock=before_stock,
                    after_stock=inventory.current_stock,
                    reason=f"发货出库 - 任务单号: {shipment.task_no}",
                )
            except Inventory.DoesNotExist:
                return error(message="商品库存记录不存在", code=400)

        logger.info(
            f"商家执行发货: merchant={merchant.id}, shipment={shipment.id}, "
            f"logistics={data['logistics_company']}, tracking={data['tracking_no']}"
        )
        return success(data=ShipmentDetailSerializer(shipment).data)


# ==================== 操作记录 ====================


class MerchantRecordListView(APIView):
    """商户操作记录"""

    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request):
        merchant = request.user.merchant
        records = []

        # 商品记录
        products = Product.objects.filter(merchant=merchant)
        for product in products:
            records.append({
                "id": f"product_{product.id}",
                "type": "product",
                "type_display": "商品",
                "description": f"提交商品「{product.name}」- {product.get_status_display()}",
                "created_at": product.created_at,
            })
            if product.review_note:
                records.append({
                    "id": f"product_review_{product.id}",
                    "type": "product_review",
                    "type_display": "商品审核",
                    "description": f"商品「{product.name}」审核意见: {product.review_note}",
                    "created_at": product.updated_at,
                })

        # 库存记录
        inventory_records = InventoryRecord.objects.filter(
            product__merchant=merchant
        ).order_by("-created_at")[:50]
        for record in inventory_records:
            records.append({
                "id": f"inventory_{record.id}",
                "type": "inventory",
                "type_display": "库存",
                "description": (
                    f"商品「{record.product.name}」{record.get_type_display()} "
                    f"{record.before_stock} → {record.after_stock}"
                    + (f" (原因: {record.reason})" if record.reason else "")
                ),
                "created_at": record.created_at,
            })

        # 发货记录
        shipments = ShipmentTask.objects.filter(
            product__merchant=merchant, status=ShipmentTask.Status.SHIPPED
        ).order_by("-shipped_at")[:50]
        for shipment in shipments:
            records.append({
                "id": f"shipment_{shipment.id}",
                "type": "shipment",
                "type_display": "发货",
                "description": (
                    f"发货任务「{shipment.task_no}」已发货 - "
                    f"{shipment.logistics_company} {shipment.tracking_no}"
                ),
                "created_at": shipment.shipped_at,
            })

        # 按时间排序
        records.sort(key=lambda x: x["created_at"] or timezone.now(), reverse=True)

        # 分页
        page_size = min(int(request.query_params.get("page_size", 10)), 100)
        page = int(request.query_params.get("page", 1))
        total = len(records)
        start = (page - 1) * page_size
        items = records[start:start + page_size]

        return success(data={
            "count": total,
            "page": page,
            "page_size": page_size,
            "results": OperationRecordSerializer(items, many=True).data,
        })
