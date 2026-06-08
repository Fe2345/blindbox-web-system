from rest_framework import serializers

from apps.common.utils import keys_to_camel

from .models import Asset


class AssetSerializer(serializers.ModelSerializer):
    """资产读取序列化器"""

    product_id = serializers.PrimaryKeyRelatedField(source="product", read_only=True)
    can_recycle = serializers.SerializerMethodField()
    can_ship = serializers.SerializerMethodField()
    can_exchange = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = [
            "id", "product_id", "product_name", "product_image",
            "category", "rarity", "description",
            "source_type", "source_name", "obtained_at",
            "status", "estimated_points", "recyclable_points",
            "can_recycle", "can_ship", "can_exchange",
        ]

    def get_can_recycle(self, obj):
        return obj.status == Asset.Status.AVAILABLE

    def get_can_ship(self, obj):
        return obj.status == Asset.Status.AVAILABLE

    def get_can_exchange(self, obj):
        return obj.status == Asset.Status.AVAILABLE

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))
