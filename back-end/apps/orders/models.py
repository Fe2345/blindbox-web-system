from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class Order(BaseModel):
    """订单（发货单 / 换物单）"""

    class OrderType(models.TextChoices):
        SHIPMENT = "shipment", "发货"
        EXCHANGE = "exchange", "换物"

    class Status(models.TextChoices):
        PENDING = "pending", "待处理"
        SHIPPED = "shipped", "已发货"
        COMPLETED = "completed", "已完成"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="用户",
    )
    order_no = models.CharField(max_length=50, unique=True, verbose_name="订单编号")
    type = models.CharField(max_length=20, choices=OrderType.choices, verbose_name="订单类型")
    asset = models.ForeignKey(
        "assets.Asset",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="关联资产",
    )
    # 快照字段
    asset_name = models.CharField(max_length=100, verbose_name="资产名称")
    asset_image = models.CharField(max_length=500, verbose_name="资产图片")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="状态",
    )
    # 收货信息
    receiver_name = models.CharField(max_length=30, verbose_name="收货人")
    receiver_phone = models.CharField(max_length=11, verbose_name="收货电话")
    receiver_address = models.TextField(verbose_name="收货地址")
    # 物流信息
    logistics_company = models.CharField(max_length=100, blank=True, default="", verbose_name="物流公司")
    tracking_no = models.CharField(max_length=100, blank=True, default="", verbose_name="运单号")
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name="发货时间")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="完成时间")

    class Meta:
        db_table = "order"
        verbose_name = "订单"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
