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
    ip_name = models.CharField(max_length=100, blank=True, default="", verbose_name="所属IP")
    cost_points = models.PositiveIntegerField(verbose_name="消耗积分")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.INACTIVE,
        verbose_name="状态",
    )
    start_time = models.DateTimeField(verbose_name="活动开始时间")
    end_time = models.DateTimeField(verbose_name="活动结束时间")
    max_draw_count = models.PositiveIntegerField(default=10, verbose_name="单次最大抽取次数")
    allow_simulation = models.BooleanField(default=True, verbose_name="是否允许模拟抽取")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="展示排序")

    class Meta:
        db_table = "blindbox"
        verbose_name = "盲盒"
        verbose_name_plural = verbose_name
        ordering = ["sort_order", "-created_at"]


class Prize(BaseModel):
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
    probability = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="概率(%)")
    weight = models.PositiveIntegerField(default=0, verbose_name="抽取权重")
    quantity = models.PositiveIntegerField(default=0, verbose_name="奖品总数量")
    remaining_quantity = models.PositiveIntegerField(default=0, verbose_name="奖品剩余数量")
    is_active = models.BooleanField(default=True, verbose_name="是否参与抽取")
    ip_name_snapshot = models.CharField(max_length=100, blank=True, default="", verbose_name="奖品IP快照")

    class Meta:
        db_table = "blindbox_prize"
        verbose_name = "奖品"
        verbose_name_plural = verbose_name
        ordering = ["rarity"]


class DrawRecord(BaseModel):
    """抽盒记录"""

    class DrawType(models.TextChoices):
        REAL = "real", "真实抽取"
        SIMULATION = "simulation", "模拟抽取"

    class DrawStatus(models.TextChoices):
        SUCCESS = "success", "成功"
        FAILED = "failed", "失败"

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
    asset = models.ForeignKey(
        "assets.Asset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="draw_records",
        verbose_name="关联资产",
    )
    prize_name = models.CharField(max_length=100, verbose_name="奖品名称（快照）")
    prize_image = models.CharField(max_length=500, verbose_name="奖品图片（快照）")
    rarity = models.CharField(max_length=10, verbose_name="稀有度（快照）")
    ip_name_snapshot = models.CharField(max_length=100, blank=True, default="", verbose_name="IP快照")
    cost_points = models.PositiveIntegerField(verbose_name="消耗积分")
    remaining_points = models.PositiveIntegerField(default=0, verbose_name="抽取后剩余积分")
    batch_no = models.CharField(max_length=50, blank=True, default="", verbose_name="抽取批次号")
    draw_type = models.CharField(
        max_length=20,
        choices=DrawType.choices,
        default=DrawType.REAL,
        verbose_name="抽取类型",
    )
    draw_status = models.CharField(
        max_length=20,
        choices=DrawStatus.choices,
        default=DrawStatus.SUCCESS,
        verbose_name="抽取状态",
    )

    class Meta:
        db_table = "blindbox_draw_record"
        verbose_name = "抽盒记录"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
