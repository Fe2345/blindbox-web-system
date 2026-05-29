from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class ExchangePost(BaseModel):
    """换物帖子（用户发布自己的资产，期望交换其他物品）"""

    class Status(models.TextChoices):
        PUBLISHED = "published", "发布中"
        LOCKED = "locked", "已锁定"  # 有人申请后锁定
        COMPLETED = "completed", "已完成"
        CANCELLED = "cancelled", "已取消"

    class Rarity(models.TextChoices):
        N = "N", "N"
        R = "R", "R"
        SR = "SR", "SR"
        SSR = "SSR", "SSR"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exchange_posts",
        verbose_name="发布人",
    )
    asset = models.ForeignKey(
        "assets.Asset",
        on_delete=models.PROTECT,
        related_name="exchange_posts",
        verbose_name="交换资产",
    )
    # 快照字段
    asset_name = models.CharField(max_length=100, verbose_name="资产名称")
    asset_image = models.CharField(max_length=500, verbose_name="资产图片")
    asset_rarity = models.CharField(max_length=10, choices=Rarity.choices, verbose_name="资产稀有度")
    asset_category = models.CharField(max_length=50, verbose_name="资产分类")
    expect_description = models.TextField(verbose_name="期望换取的物品描述")
    remark = models.TextField(blank=True, default="", verbose_name="备注")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PUBLISHED,
        verbose_name="状态",
    )

    class Meta:
        db_table = "exchange_post"
        verbose_name = "换物帖子"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]


class ExchangeApplication(BaseModel):
    """换物申请（他人申请交换帖子上的物品）"""

    class Status(models.TextChoices):
        PENDING = "pending", "待处理"
        ACCEPTED = "accepted", "已接受"
        REJECTED = "rejected", "已拒绝"
        CANCELLED = "cancelled", "已取消"

    post = models.ForeignKey(
        ExchangePost,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name="换物帖子",
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exchange_applications",
        verbose_name="申请人",
    )
    applicant_asset = models.ForeignKey(
        "assets.Asset",
        on_delete=models.PROTECT,
        related_name="exchange_applications",
        verbose_name="申请人资产",
    )
    # 快照字段
    applicant_asset_name = models.CharField(max_length=100, verbose_name="申请人资产名称")
    applicant_asset_image = models.CharField(max_length=500, verbose_name="申请人资产图片")
    applicant_asset_rarity = models.CharField(max_length=10, verbose_name="申请人资产稀有度")
    post_asset_name = models.CharField(max_length=100, verbose_name="目标资产名称")
    post_asset_image = models.CharField(max_length=500, verbose_name="目标资产图片")
    post_asset_rarity = models.CharField(max_length=10, verbose_name="目标资产稀有度")
    remark = models.TextField(blank=True, default="", verbose_name="申请备注")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="状态",
    )

    class Meta:
        db_table = "exchange_application"
        verbose_name = "换物申请"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
