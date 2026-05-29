from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class BlindBox(BaseModel):
    """盲盒配置"""

    class Status(models.TextChoices):
        ACTIVE = "active", "上架中"
        INACTIVE = "inactive", "已下架"
        ENDED = "ended", "已结束"

    name = models.CharField(max_length=100, verbose_name="盲盒名称")
    cover = models.CharField(max_length=500, verbose_name="封面图")
    description = models.TextField(blank=True, default="", verbose_name="描述")
    category = models.CharField(max_length=50, verbose_name="分类")
    cost_points = models.PositiveIntegerField(verbose_name="消耗积分")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.INACTIVE,
        verbose_name="状态",
    )
    start_time = models.DateTimeField(verbose_name="活动开始时间")
    end_time = models.DateTimeField(verbose_name="活动结束时间")

    class Meta:
        db_table = "blindbox"
        verbose_name = "盲盒"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]


class Prize(models.Model):
    """盲盒奖品（奖池配置）"""

    class Rarity(models.TextChoices):
        N = "N", "N"
        R = "R", "R"
        SR = "SR", "SR"
        SSR = "SSR", "SSR"

    blindbox = models.ForeignKey(
        BlindBox,
        on_delete=models.CASCADE,
        related_name="prizes",
        verbose_name="所属盲盒",
    )
    product = models.ForeignKey(
        "merchant.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prizes",
        verbose_name="关联商品",
    )
    name = models.CharField(max_length=100, verbose_name="奖品名称")
    image = models.CharField(max_length=500, verbose_name="奖品图片")
    rarity = models.CharField(max_length=10, choices=Rarity.choices, verbose_name="稀有度")
    probability = models.PositiveIntegerField(verbose_name="概率(%)")  # 0-100
    stock = models.PositiveIntegerField(default=0, verbose_name="库存")

    class Meta:
        db_table = "blindbox_prize"
        verbose_name = "奖品"
        verbose_name_plural = verbose_name
        ordering = ["rarity"]


class DrawRecord(BaseModel):
    """抽盒记录"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="draw_records",
        verbose_name="用户",
    )
    blindbox = models.ForeignKey(
        BlindBox,
        on_delete=models.CASCADE,
        related_name="draw_records",
        verbose_name="盲盒",
    )
    prize = models.ForeignKey(
        Prize,
        on_delete=models.CASCADE,
        related_name="draw_records",
        verbose_name="抽中奖品",
    )
    prize_name = models.CharField(max_length=100, verbose_name="奖品名称（快照）")
    prize_image = models.CharField(max_length=500, verbose_name="奖品图片（快照）")
    rarity = models.CharField(max_length=10, verbose_name="稀有度（快照）")
    cost_points = models.PositiveIntegerField(verbose_name="消耗积分")

    class Meta:
        db_table = "blindbox_draw_record"
        verbose_name = "抽盒记录"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
