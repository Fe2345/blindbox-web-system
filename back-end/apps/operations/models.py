from django.db import models

from apps.common.models import BaseModel


class RuleConfig(BaseModel):
    """系统规则配置（单例）"""

    recycle_rate = models.PositiveIntegerField(default=30, verbose_name="回收返还比例(%)")
    new_user_points = models.PositiveIntegerField(default=500, verbose_name="新用户赠送积分")
    max_draw_per_day = models.PositiveIntegerField(default=20, verbose_name="每日抽取上限")
    min_points_to_draw = models.PositiveIntegerField(default=60, verbose_name="最低抽取积分")
    order_auto_confirm_days = models.PositiveIntegerField(default=7, verbose_name="订单自动确认天数")
    exchange_lock_hours = models.PositiveIntegerField(default=48, verbose_name="换物锁定时长(小时)")
    updated_by = models.CharField(max_length=100, blank=True, default="", verbose_name="修改人")

    class Meta:
        db_table = "rule_config"
        verbose_name = "规则配置"
        verbose_name_plural = verbose_name

    @classmethod
    def get(cls):
        """获取全局规则单例，不存在时自动创建"""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class OpLog(BaseModel):
    """操作日志"""

    operator = models.CharField(max_length=100, verbose_name="操作人")
    action = models.CharField(max_length=50, verbose_name="操作类型")
    target = models.CharField(max_length=200, verbose_name="操作对象")
    detail = models.TextField(blank=True, default="", verbose_name="操作详情")

    class Meta:
        db_table = "operation_log"
        verbose_name = "操作日志"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]


class ExceptionRecord(BaseModel):
    """异常工单"""

    class ExceptionType(models.TextChoices):
        STOCK = "stock", "库存异常"
        ORDER = "order", "订单异常"
        DUPLICATE = "duplicate", "重复记录"
        APPEAL = "appeal", "用户申诉"
        OTHER = "other", "其他"

    class Status(models.TextChoices):
        OPEN = "open", "待处理"
        PROCESSING = "processing", "处理中"
        RESOLVED = "resolved", "已解决"

    type = models.CharField(max_length=20, choices=ExceptionType.choices, verbose_name="异常类型")
    description = models.TextField(verbose_name="异常描述")
    related_id = models.CharField(max_length=50, blank=True, default="", verbose_name="关联ID")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, verbose_name="状态")
    result = models.TextField(blank=True, default="", verbose_name="处理结果")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="处理时间")

    class Meta:
        db_table = "exception_record"
        verbose_name = "异常工单"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]


class TransactionLedger(BaseModel):
    """交易账本（只读流水聚合）"""

    class LedgerType(models.TextChoices):
        BLINDBOX_DRAW = "blindbox_draw", "盲抽"
        RECYCLE = "recycle", "回收"
        SHIPMENT = "shipment", "发货"
        EXCHANGE = "exchange", "换物"
        SYSTEM = "system", "系统"

    type = models.CharField(max_length=20, choices=LedgerType.choices, verbose_name="交易类型")
    description = models.CharField(max_length=500, verbose_name="说明")
    amount = models.IntegerField(default=0, verbose_name="积分变动")

    class Meta:
        db_table = "transaction_ledger"
        verbose_name = "交易账本"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
