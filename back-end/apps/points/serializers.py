from rest_framework import serializers

from apps.common.utils import keys_to_camel, keys_to_snake

from .models import PointsRecord, TransactionRecord


class PointsRechargeSerializer(serializers.Serializer):
    amount_yuan = serializers.DecimalField(max_digits=8, decimal_places=2, min_value=1, max_value=9999)

    def to_internal_value(self, data):
        return super().to_internal_value(keys_to_snake(data))


class PointsRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsRecord
        fields = [
            "id",
            "type",
            "amount",
            "balance",
            "description",
            "related_id",
            "created_at",
        ]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))


class TransactionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionRecord
        fields = [
            "id",
            "type",
            "description",
            "related_asset_name",
            "status_change",
            "created_at",
        ]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))
