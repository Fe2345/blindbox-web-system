from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class Merchant(BaseModel):
    """商家模型，与 User 一对一关联"""

    class Status(models.TextChoices):
        PENDING = "pending", "待审核"
        APPROVED = "approved", "已通过"
        REJECTED = "rejected", "已驳回"
        FROZEN = "frozen", "已冻结"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="merchant",
        verbose_name="关联用户",
    )
    name = models.CharField(max_length=100, verbose_name="商家名称")
    contact_name = models.CharField(max_length=50, verbose_name="联系人")
    phone = models.CharField(max_length=20, verbose_name="联系电话")
    email = models.EmailField(max_length=100, blank=True, default="", verbose_name="联系邮箱")
    license = models.CharField(max_length=200, blank=True, default="", verbose_name="营业执照编号")
    business_scope = models.TextField(blank=True, default="", verbose_name="经营范围")
    supply_desc = models.TextField(blank=True, default="", verbose_name="供货说明")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="状态",
    )
    credit_score = models.IntegerField(default=100, verbose_name="信用评分")
    review_note = models.TextField(blank=True, default="", verbose_name="审核意见")
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name="审核时间")

    class Meta:
        db_table = "merchant"
        verbose_name = "商家"
        verbose_name_plural = verbose_name


class Product(BaseModel):
    """商家提交的商品"""

    class Rarity(models.TextChoices):
        N = "N", "N"
        R = "R", "R"
        SR = "SR", "SR"
        SSR = "SSR", "SSR"

    class Status(models.TextChoices):
        PENDING = "pending", "待审核"
        APPROVED = "approved", "已通过"
        REJECTED = "rejected", "已驳回"
        OFFLINE = "offline", "已下架"

    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="所属商家",
    )
    name = models.CharField(max_length=100, verbose_name="商品名称")
    image = models.CharField(max_length=500, verbose_name="商品图片")
    category = models.CharField(max_length=50, verbose_name="分类")
    rarity = models.CharField(max_length=10, choices=Rarity.choices, verbose_name="稀有度")
    description = models.TextField(blank=True, default="", verbose_name="描述")
    estimated_points = models.PositiveIntegerField(default=0, verbose_name="预估积分")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="状态",
    )
    review_note = models.TextField(blank=True, default="", verbose_name="审核意见")

    class Meta:
        db_table = "merchant_product"
        verbose_name = "商家商品"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]


class Inventory(BaseModel):
    """商品库存"""

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory",
        verbose_name="商品",
    )
    current_stock = models.PositiveIntegerField(default=0, verbose_name="当前库存")

    class Meta:
        db_table = "merchant_inventory"
        verbose_name = "库存"
        verbose_name_plural = verbose_name


class InventoryRecord(BaseModel):
    """库存变动记录"""

    class ChangeType(models.TextChoices):
        INCREASE = "increase", "入库"
        DECREASE = "decrease", "出库"
        MODIFY = "modify", "调整"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory_records",
        verbose_name="商品",
    )
    type = models.CharField(max_length=20, choices=ChangeType.choices, verbose_name="变动类型")
    before_stock = models.PositiveIntegerField(verbose_name="变动前库存")
    after_stock = models.PositiveIntegerField(verbose_name="变动后库存")
    reason = models.CharField(max_length=200, blank=True, default="", verbose_name="变动原因")

    class Meta:
        db_table = "merchant_inventory_record"
        verbose_name = "库存变动记录"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]


class ShipmentTask(BaseModel):
    """发货任务"""

    class Status(models.TextChoices):
        PENDING = "pending", "待发货"
        SHIPPED = "shipped", "已发货"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="shipments",
        verbose_name="商品",
    )
    task_no = models.CharField(max_length=50, verbose_name="任务编号")
    order_no = models.CharField(max_length=50, verbose_name="关联订单号")
    receiver_name = models.CharField(max_length=30, verbose_name="收货人")
    receiver_phone = models.CharField(max_length=11, verbose_name="收货电话")
    receiver_address = models.TextField(verbose_name="收货地址")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="状态",
    )
    logistics_company = models.CharField(max_length=100, blank=True, default="", verbose_name="物流公司")
    tracking_no = models.CharField(max_length=100, blank=True, default="", verbose_name="运单号")
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name="发货时间")

    class Meta:
        db_table = "merchant_shipment"
        verbose_name = "发货任务"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
