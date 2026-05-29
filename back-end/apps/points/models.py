from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class PointsAccount(BaseModel):
    """用户积分账户"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="points_account",
        verbose_name="用户",
    )
    balance = models.IntegerField(default=0, verbose_name="积分余额")

    class Meta:
        db_table = "points_account"
        verbose_name = "积分账户"
        verbose_name_plural = verbose_name


class PointsRecord(BaseModel):
    """积分变动流水"""

    class RecordType(models.TextChoices):
        BLINDBOX_CONSUME = "blindbox_consume", "盲盒消耗"
        RECYCLE_RETURN = "recycle_return", "回收返还"
        SYSTEM_ADJUST = "system_adjust", "系统调整"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="points_records",
        verbose_name="用户",
    )
    type = models.CharField(max_length=30, choices=RecordType.choices, verbose_name="变动类型")
    amount = models.IntegerField(verbose_name="变动积分")
    balance = models.IntegerField(verbose_name="变动后余额")
    description = models.CharField(max_length=200, verbose_name="说明")
    related_id = models.CharField(max_length=50, blank=True, default="", verbose_name="关联业务ID")

    class Meta:
        db_table = "points_record"
        verbose_name = "积分流水"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]


class TransactionRecord(BaseModel):
    """用户交易记录（资产状态变更记录）"""

    class RecordType(models.TextChoices):
        BLINDBOX_DRAW = "blindbox_draw", "盲盒抽取"
        RECYCLE = "recycle", "回收"
        SHIPMENT = "shipment", "发货"
        EXCHANGE = "exchange", "换物"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transaction_records",
        verbose_name="用户",
    )
    type = models.CharField(max_length=30, choices=RecordType.choices, verbose_name="交易类型")
    description = models.CharField(max_length=200, verbose_name="说明")
    related_asset_name = models.CharField(max_length=100, verbose_name="关联资产名称")
    status_change = models.CharField(max_length=100, verbose_name="状态变更")

    class Meta:
        db_table = "transaction_record"
        verbose_name = "交易记录"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
