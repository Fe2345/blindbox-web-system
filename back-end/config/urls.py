from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # 用户端
    path("user/api/", include("apps.accounts.urls_user")),
    path("user/api/", include("apps.blindbox.urls_user")),
    path("user/api/", include("apps.assets.urls")),
    path("user/api/", include("apps.orders.urls_user")),
    path("user/api/", include("apps.exchange.urls")),
    path("user/api/", include("apps.points.urls")),
    # 商家端
    path("merchant/api/", include("apps.merchant.urls_merchant")),
    # 管理端（必须在 admin/ 之前，否则会被 Django admin 拦截）
    path("admin/api/", include("apps.accounts.urls_admin")),
    path("admin/api/", include("apps.blindbox.urls_admin")),
    path("admin/api/", include("apps.orders.urls_admin")),
    path("admin/api/", include("apps.merchant.urls_admin")),
    path("admin/api/", include("apps.operations.urls")),
    # Django 后台管理
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
