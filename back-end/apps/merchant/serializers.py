from rest_framework import serializers

from .models import Inventory, InventoryRecord, Merchant, Product, ShipmentTask


# ==================== 商家信息 ====================


class MerchantInfoSerializer(serializers.ModelSerializer):
    """商家信息序列化器（只读）"""

    username = serializers.CharField(source="user.username", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Merchant
        fields = [
            "id", "username", "name", "contact_name", "phone", "email",
            "license", "business_scope", "supply_desc", "status", "status_display",
            "credit_score", "review_note", "reviewed_at", "created_at",
        ]


class MerchantApplicationSerializer(serializers.Serializer):
    """商家入驻申请序列化器"""

    name = serializers.CharField(max_length=100, label="商家名称")
    contact_name = serializers.CharField(max_length=50, label="联系人")
    phone = serializers.CharField(max_length=20, label="联系电话")
    email = serializers.EmailField(max_length=100, required=False, default="", label="联系邮箱")
    license = serializers.CharField(max_length=200, required=False, default="", label="营业执照编号")
    business_scope = serializers.CharField(required=False, default="", label="经营范围")
    supply_desc = serializers.CharField(required=False, default="", label="供货说明")

    def validate_name(self, value):
        if Merchant.objects.filter(name=value).exists():
            raise serializers.ValidationError("该商家名称已存在")
        return value


# ==================== 商品管理 ====================


class ProductListSerializer(serializers.ModelSerializer):
    """商品列表序列化器（只读）"""

    status_display = serializers.CharField(source="get_status_display", read_only=True)
    rarity_display = serializers.CharField(source="get_rarity_display", read_only=True)
    inventory_stock = serializers.IntegerField(source="inventory.current_stock", read_only=True, default=0)

    class Meta:
        model = Product
        fields = [
            "id", "name", "image", "category", "rarity", "rarity_display",
            "estimated_points", "status", "status_display", "inventory_stock",
            "review_note", "created_at",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """商品详情序列化器（只读）"""

    status_display = serializers.CharField(source="get_status_display", read_only=True)
    rarity_display = serializers.CharField(source="get_rarity_display", read_only=True)
    inventory_stock = serializers.IntegerField(source="inventory.current_stock", read_only=True, default=0)

    class Meta:
        model = Product
        fields = [
            "id", "name", "image", "category", "rarity", "rarity_display",
            "description", "estimated_points", "status", "status_display",
            "inventory_stock", "review_note", "created_at", "updated_at",
        ]


class ProductWriteSerializer(serializers.Serializer):
    """商品新增/编辑序列化器"""

    name = serializers.CharField(max_length=100, label="商品名称")
    image = serializers.CharField(max_length=500, label="商品图片")
    category = serializers.CharField(max_length=50, label="分类")
    rarity = serializers.ChoiceField(choices=Product.Rarity.choices, label="稀有度")
    description = serializers.CharField(required=False, default="", label="描述")
    estimated_points = serializers.IntegerField(min_value=0, required=False, default=0, label="预估积分")


# ==================== 库存管理 ====================


class InventoryListSerializer(serializers.ModelSerializer):
    """库存列表序列化器"""

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.CharField(source="product.image", read_only=True)
    product_category = serializers.CharField(source="product.category", read_only=True)
    product_rarity = serializers.CharField(source="product.rarity", read_only=True)
    product_status = serializers.CharField(source="product.status", read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id", "product", "product_name", "product_image", "product_category",
            "product_rarity", "product_status", "current_stock", "updated_at",
        ]


class InventoryUpdateSerializer(serializers.Serializer):
    """库存修改序列化器"""

    change_type = serializers.ChoiceField(
        choices=InventoryRecord.ChangeType.choices,
        label="变动类型",
    )
    quantity = serializers.IntegerField(min_value=1, label="变动数量")
    reason = serializers.CharField(max_length=200, required=False, default="", label="变动原因")

    def validate(self, attrs):
        change_type = attrs["change_type"]
        quantity = attrs["quantity"]
        if change_type == InventoryRecord.ChangeType.MODIFY and quantity < 0:
            raise serializers.ValidationError({"quantity": "调整类型时数量不能为负数"})
        return attrs


class InventoryRecordSerializer(serializers.ModelSerializer):
    """库存变动记录序列化器"""

    product_name = serializers.CharField(source="product.name", read_only=True)
    type_display = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        model = InventoryRecord
        fields = [
            "id", "product", "product_name", "type", "type_display",
            "before_stock", "after_stock", "reason", "created_at",
        ]


# ==================== 发货管理 ====================


class ShipmentListSerializer(serializers.ModelSerializer):
    """发货任务列表序列化器"""

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.CharField(source="product.image", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = ShipmentTask
        fields = [
            "id", "task_no", "order_no", "product", "product_name", "product_image",
            "receiver_name", "receiver_phone", "status", "status_display",
            "logistics_company", "tracking_no", "shipped_at", "created_at",
        ]


class ShipmentDetailSerializer(serializers.ModelSerializer):
    """发货任务详情序列化器"""

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.CharField(source="product.image", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = ShipmentTask
        fields = [
            "id", "task_no", "order_no", "product", "product_name", "product_image",
            "receiver_name", "receiver_phone", "receiver_address",
            "status", "status_display", "logistics_company", "tracking_no",
            "shipped_at", "created_at", "updated_at",
        ]


class ShipmentShipSerializer(serializers.Serializer):
    """执行发货序列化器"""

    logistics_company = serializers.CharField(max_length=100, label="物流公司")
    tracking_no = serializers.CharField(max_length=100, label="运单号")


# ==================== 操作记录 ====================


class OperationRecordSerializer(serializers.Serializer):
    """操作记录序列化器"""

    id = serializers.IntegerField()
    type = serializers.CharField()
    type_display = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField()
