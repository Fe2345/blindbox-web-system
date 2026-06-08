from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    assetId = serializers.IntegerField(source="asset.id", read_only=True)
    orderNo = serializers.CharField(source="order_no", read_only=True)
    assetName = serializers.CharField(source="asset_name", read_only=True)
    assetImage = serializers.CharField(source="asset_image", read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    shippedAt = serializers.DateTimeField(source="shipped_at", read_only=True)
    completedAt = serializers.DateTimeField(source="completed_at", read_only=True)
    address = serializers.SerializerMethodField()
    logistics = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "orderNo",
            "type",
            "assetId",
            "assetName",
            "assetImage",
            "status",
            "address",
            "logistics",
            "createdAt",
            "shippedAt",
            "completedAt",
        ]

    def get_address(self, obj):
        return {
            "name": obj.receiver_name,
            "phone": obj.receiver_phone,
            "fullAddress": obj.receiver_address,
        }

    def get_logistics(self, obj):
        if not obj.logistics_company and not obj.tracking_no:
            return None
        return {
            "company": obj.logistics_company,
            "trackingNo": obj.tracking_no,
        }
