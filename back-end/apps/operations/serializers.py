from rest_framework import serializers

from apps.common.utils import keys_to_camel, keys_to_snake

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

    def to_internal_value(self, data):
        return super().to_internal_value(keys_to_snake(data))


class TransactionLedgerSerializer(serializers.ModelSerializer):
    """交易账本序列化器"""

    class Meta:
        model = TransactionLedger
        fields = ["id", "type", "description", "amount", "created_at"]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))
