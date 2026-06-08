from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """仅允许已登录用户访问，未登录返回 401"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdmin(BasePermission):
    """仅允许管理员 (role='admin') 访问"""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsMerchant(BasePermission):
    """仅商家用户可访问，返回 403。"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == "merchant"
