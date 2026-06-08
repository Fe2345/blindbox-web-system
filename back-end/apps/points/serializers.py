from rest_framework import serializers

from apps.common.utils import keys_to_camel

from .models import PointsRecord, TransactionRecord


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
