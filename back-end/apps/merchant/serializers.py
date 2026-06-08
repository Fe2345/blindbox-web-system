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
        data["supply_count"] = instance.products.count()
        data["violation_count"] = 0
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


class MerchantRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=150)
    password = serializers.CharField(min_length=6, max_length=128)
    phone = serializers.CharField(max_length=11)

    def to_internal_value(self, data):
        return super().to_internal_value(keys_to_snake(data))

    def validate_username(self, value):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_phone(self, value):
        if not re.match(r"^1[3-9]\d{9}$", value):
            raise serializers.ValidationError("请输入有效的 11 位手机号")
        return value
