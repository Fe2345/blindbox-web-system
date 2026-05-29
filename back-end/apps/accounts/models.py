from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import BaseModel


class User(AbstractUser):
    """自定义用户模型，支持 用户/商家/管理员 三种角色"""

    class Role(models.TextChoices):
        USER = "user", "普通用户"
        MERCHANT = "merchant", "商家"
        ADMIN = "admin", "管理员"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        verbose_name="角色",
    )
    phone = models.CharField(max_length=20, blank=True, default="", verbose_name="手机号")
    avatar = models.CharField(max_length=500, blank=True, default="", verbose_name="头像")

    class Meta:
        db_table = "accounts_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Division(models.Model):
    """省/市/区 行政区划"""

    code = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=50)
    level = models.SmallIntegerField()  # 1=省 2=市 3=区
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    class Meta:
        db_table = "division"
        verbose_name = "行政区划"
        verbose_name_plural = verbose_name
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} {self.name}"


class Address(BaseModel):
    """收货地址"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name="用户",
    )
    receiver_name = models.CharField(max_length=30, verbose_name="收货人")
    receiver_phone = models.CharField(max_length=11, verbose_name="手机号")
    province = models.ForeignKey(
        Division,
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="省",
    )
    city = models.ForeignKey(
        Division,
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="市",
    )
    district = models.ForeignKey(
        Division,
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="区",
    )
    street = models.CharField(max_length=100, blank=True, default="", verbose_name="街道/镇")
    detail = models.CharField(max_length=200, verbose_name="详细地址")
    is_default = models.BooleanField(default=False, verbose_name="默认地址")

    class Meta:
        db_table = "user_address"
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name
        ordering = ["-is_default", "-updated_at"]

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
