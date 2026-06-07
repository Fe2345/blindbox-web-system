from rest_framework.permissions import BasePermission

from .models import Merchant


class IsMerchant(BasePermission):
    """仅允许已认证商家访问"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            merchant = request.user.merchant
            return merchant.status == Merchant.Status.APPROVED
        except Merchant.DoesNotExist:
            return False


class IsPendingMerchant(BasePermission):
    """允许待审核或已驳回状态的商家访问（用于申请相关接口）"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            merchant = request.user.merchant
            return merchant.status in [Merchant.Status.PENDING, Merchant.Status.REJECTED]
        except Merchant.DoesNotExist:
            return True  # 没有商家记录也可以申请
