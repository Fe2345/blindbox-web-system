from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class Asset(BaseModel):
    """用户资产（抽盒或换物获得的物品）"""

    class SourceType(models.TextChoices):
        BLINDBOX = "blindbox", "盲盒抽取"
        EXCHANGE = "exchange", "换物获得"

    class Status(models.TextChoices):
        AVAILABLE = "available", "可操作"
        EXCHANGE_PUBLISHED = "exchange_published", "换物发布中"
        EXCHANGE_LOCKED = "exchange_locked", "换物锁定中"
        PENDING_SHIPMENT = "pending_shipment", "待发货"
        SHIPPED = "shipped", "已发货"
        RECYCLED = "recycled", "已回收"
        COMPLETED = "completed", "已完成"

    class Rarity(models.TextChoices):
        N = "N", "N"
        R = "R", "R"
        SR = "SR", "SR"
        SSR = "SSR", "SSR"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assets",
        verbose_name="用户",
    )
    product = models.ForeignKey(
        "merchant.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assets",
        verbose_name="关联商品",
    )
    draw_record = models.ForeignKey(
        "blindbox.DrawRecord",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assets",
        verbose_name="抽盒记录",
    )
    # 快照字段（保留获得时的信息）
    product_name = models.CharField(max_length=100, verbose_name="商品名称")
    product_image = models.CharField(max_length=500, verbose_name="商品图片")
    category = models.CharField(max_length=50, verbose_name="分类")
    rarity = models.CharField(max_length=10, choices=Rarity.choices, verbose_name="稀有度")
    description = models.TextField(blank=True, default="", verbose_name="描述")
    source_type = models.CharField(max_length=20, choices=SourceType.choices, verbose_name="来源类型")
    source_name = models.CharField(max_length=100, verbose_name="来源名称")
    obtained_at = models.DateTimeField(verbose_name="获得时间")
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.AVAILABLE,
        verbose_name="状态",
    )
    estimated_points = models.PositiveIntegerField(default=0, verbose_name="估值积分")
    recyclable_points = models.PositiveIntegerField(default=0, verbose_name="可回收积分")

    class Meta:
        db_table = "user_asset"
        verbose_name = "用户资产"
        verbose_name_plural = verbose_name
        ordering = ["-obtained_at"]
