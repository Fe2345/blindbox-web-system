import re

from rest_framework import serializers

from apps.common.utils import keys_to_camel, keys_to_snake

from .models import Address, Division, User


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ["code", "name", "level"]


class AddressSerializer(serializers.ModelSerializer):
    """地址读取序列化器"""

    province = DivisionSerializer(read_only=True)
    city = DivisionSerializer(read_only=True)
    district = DivisionSerializer(read_only=True)

    class Meta:
        model = Address
        fields = [
            "id", "receiver_name", "receiver_phone",
            "province", "city", "district",
            "street", "detail", "is_default",
        ]
        read_only_fields = ["id"]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))


class AddressWriteSerializer(serializers.Serializer):
    """地址写入序列化器"""

    receiver_name = serializers.CharField(max_length=30)
    receiver_phone = serializers.CharField(max_length=11)
    province_code = serializers.CharField(max_length=6)
    city_code = serializers.CharField(max_length=6)
    district_code = serializers.CharField(max_length=6)
    street = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")
    detail = serializers.CharField(max_length=200)
    is_default = serializers.BooleanField(default=False)

    def to_internal_value(self, data):
        return super().to_internal_value(keys_to_snake(data))

    def validate_receiver_phone(self, value):
        if not re.match(r"^1[3-9]\d{9}$", value):
            raise serializers.ValidationError("请输入有效的 11 位手机号")
        return value

    def validate(self, attrs):
        codes = [attrs["province_code"], attrs["city_code"], attrs["district_code"]]
        divisions = Division.objects.filter(code__in=codes)
        found = {d.code: d for d in divisions}
        for code in codes:
            if code not in found:
                raise serializers.ValidationError(f"行政区划代码 {code} 不存在")
        return attrs


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=150)
    phone = serializers.CharField(max_length=11)
    password = serializers.CharField(min_length=6, max_length=128)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_phone(self, value):
        if not re.match(r"^1[3-9]\d{9}$", value):
            raise serializers.ValidationError("请输入有效的 11 位手机号")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserInfoSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=150, required=False)
    phone = serializers.CharField(max_length=11, required=False)
    avatar = serializers.CharField(max_length=500, required=False, allow_blank=True)

    def validate_username(self, value):
        user = self.context["request"].user
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_phone(self, value):
        if not re.match(r"^1[3-9]\d{9}$", value):
            raise serializers.ValidationError("请输入有效的 11 位手机号")
        return value
