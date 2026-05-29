from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # 用户端
    path("user/api/", include("apps.accounts.urls_user")),
    path("user/api/", include("apps.blindbox.urls_user")),
    path("user/api/", include("apps.assets.urls")),
    path("user/api/", include("apps.orders.urls_user")),
    path("user/api/", include("apps.exchange.urls")),
    path("user/api/", include("apps.points.urls")),
    # 商家端
    path("merchant/api/", include("apps.merchant.urls_merchant")),
    # 管理端
    path("admin/api/", include("apps.accounts.urls_admin")),
    path("admin/api/", include("apps.blindbox.urls_admin")),
    path("admin/api/", include("apps.orders.urls_admin")),
    path("admin/api/", include("apps.merchant.urls_admin")),
    path("admin/api/", include("apps.operations.urls")),
]
