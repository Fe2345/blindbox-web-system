from rest_framework import serializers

from apps.common.utils import keys_to_camel

from .models import ExchangeApplication, ExchangePost


class ExchangePostSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    asset_id = serializers.IntegerField(source="asset.id", read_only=True)
    pending_count = serializers.SerializerMethodField()

    class Meta:
        model = ExchangePost
        fields = [
            "id",
            "user_id",
            "username",
            "asset_id",
            "asset_name",
            "asset_image",
            "asset_rarity",
            "asset_category",
            "expect_description",
            "remark",
            "status",
            "pending_count",
            "created_at",
        ]

    def get_pending_count(self, obj):
        return obj.applications.filter(status="pending").count()

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))


class ExchangeApplicationSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source="post.id", read_only=True)
    applicant_id = serializers.IntegerField(source="applicant.id", read_only=True)
    applicant_name = serializers.CharField(source="applicant.username", read_only=True)
    applicant_asset_id = serializers.IntegerField(source="applicant_asset.id", read_only=True)
    post_asset_id = serializers.IntegerField(source="post.asset.id", read_only=True)

    class Meta:
        model = ExchangeApplication
        fields = [
            "id",
            "post_id",
            "applicant_id",
            "applicant_name",
            "applicant_asset_id",
            "applicant_asset_name",
            "applicant_asset_image",
            "applicant_asset_rarity",
            "post_asset_id",
            "post_asset_name",
            "post_asset_image",
            "post_asset_rarity",
            "remark",
            "status",
            "created_at",
        ]

    def to_representation(self, instance):
        return keys_to_camel(super().to_representation(instance))
