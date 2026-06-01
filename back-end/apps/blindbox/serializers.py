from rest_framework import serializers

from apps.common.utils import keys_to_camel, keys_to_snake

from .models import BlindBox, Prize, DrawRecord


# ==================== 奖品 ====================


class PrizeSerializer(serializers.ModelSerializer):
    """奖品读取序列化器（用户端）"""

    class Meta:
        model = Prize
        fields = [
            "id", "name", "image", "rarity",
            "probability", "weight", "quantity", "remaining_quantity",
            "is_active", "ip_name_snapshot",
        ]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))


class AdminPrizeSerializer(serializers.ModelSerializer):
    """奖品读取序列化器（管理端）"""

    product_id = serializers.PrimaryKeyRelatedField(
        source="product", read_only=True,
    )

    class Meta:
        model = Prize
        fields = [
            "id", "product_id", "name", "image", "rarity",
            "probability", "weight", "quantity", "remaining_quantity",
            "is_active", "ip_name_snapshot",
            "created_at", "updated_at",
        ]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))


class PrizeWriteSerializer(serializers.Serializer):
    """奖品写入序列化器"""

    id = serializers.IntegerField(required=False, help_text="奖品ID，编辑时传入")
    product_id = serializers.IntegerField(required=False, allow_null=True, default=None)
    name = serializers.CharField(max_length=100)
    image = serializers.CharField(max_length=500)
    rarity = serializers.ChoiceField(choices=Prize.Rarity.choices)
    probability = serializers.IntegerField(min_value=0, max_value=100)
    weight = serializers.IntegerField(min_value=0, default=0)
    quantity = serializers.IntegerField(min_value=0, default=0)
    remaining_quantity = serializers.IntegerField(min_value=0, default=0)
    is_active = serializers.BooleanField(default=True)
    ip_name_snapshot = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")

    def to_internal_value(self, data):
        return super().to_internal_value(keys_to_snake(data))


# ==================== 盲盒 ====================


class BlindBoxSerializer(serializers.ModelSerializer):
    """盲盒读取序列化器（用户端）"""

    prizes = PrizeSerializer(many=True, read_only=True)

    class Meta:
        model = BlindBox
        fields = [
            "id", "name", "cover", "description", "category", "ip_name",
            "cost_points", "status", "start_time", "end_time",
            "max_draw_count", "allow_simulation", "sort_order",
            "prizes",
        ]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))


class AdminBlindBoxSerializer(serializers.ModelSerializer):
    """盲盒读取序列化器（管理端）"""

    prizes = AdminPrizeSerializer(many=True, read_only=True)

    class Meta:
        model = BlindBox
        fields = [
            "id", "name", "cover", "description", "category", "ip_name",
            "cost_points", "status", "start_time", "end_time",
            "max_draw_count", "allow_simulation", "sort_order",
            "prizes", "created_at", "updated_at",
        ]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))


class BlindBoxWriteSerializer(serializers.Serializer):
    """盲盒写入序列化器"""

    name = serializers.CharField(max_length=100)
    cover = serializers.CharField(max_length=500)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    category = serializers.CharField(max_length=50)
    ip_name = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")
    cost_points = serializers.IntegerField(min_value=1)
    status = serializers.ChoiceField(choices=BlindBox.Status.choices, required=False, default="inactive")
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    max_draw_count = serializers.IntegerField(min_value=1, required=False, default=10)
    allow_simulation = serializers.BooleanField(required=False, default=True)
    sort_order = serializers.IntegerField(min_value=0, required=False, default=0)

    def to_internal_value(self, data):
        return super().to_internal_value(keys_to_snake(data))

    def validate(self, attrs):
        if attrs.get("start_time") and attrs.get("end_time"):
            if attrs["start_time"] >= attrs["end_time"]:
                raise serializers.ValidationError("结束时间必须晚于开始时间")
        return attrs


class BlindBoxStatusSerializer(serializers.Serializer):
    """盲盒状态切换序列化器"""

    status = serializers.ChoiceField(choices=BlindBox.Status.choices)


# ==================== 抽取记录 ====================


class DrawResultSerializer(serializers.ModelSerializer):
    """抽取结果序列化器"""

    blindbox_id = serializers.PrimaryKeyRelatedField(source="blindbox", read_only=True)
    blindbox_name = serializers.CharField(source="blindbox.name", read_only=True)
    prize_id = serializers.PrimaryKeyRelatedField(source="prize", read_only=True)

    class Meta:
        model = DrawRecord
        fields = [
            "id", "prize_id", "prize_name", "prize_image", "rarity",
            "blindbox_id", "blindbox_name",
            "cost_points", "remaining_points",
            "batch_no", "draw_type", "draw_status",
            "created_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # created_at → draw_time
        if "created_at" in data:
            data["draw_time"] = data.pop("created_at")
        return keys_to_camel(data)


class DrawRecordSerializer(serializers.ModelSerializer):
    """抽取记录序列化器（列表查询）"""

    blindbox_name = serializers.CharField(source="blindbox.name", read_only=True)

    class Meta:
        model = DrawRecord
        fields = [
            "id", "blindbox_name", "prize_name", "prize_image", "rarity",
            "cost_points", "remaining_points",
            "draw_type", "draw_status", "created_at",
        ]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))
