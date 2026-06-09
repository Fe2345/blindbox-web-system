from django.urls import path

from apps.accounts.views import CookieTokenRefreshView
from apps.merchant.views import (
    MerchantRegisterView,
    MerchantLoginView, MerchantLogoutView, MerchantInfoView,
    MerchantApplicationView,
    MerchantDashboardView,
    ProductListView, ProductDetailView, ProductImageUploadView,
    InventoryListView, InventoryUpdateView, InventoryRecordListView,
    ShipmentTaskListView, ShipmentTaskDetailView, ShipmentConfirmView,
    RecordListView,
)

urlpatterns = [
    # 认证
    path("register", MerchantRegisterView.as_view(), name="merchant-register"),
    path("login", MerchantLoginView.as_view(), name="merchant-login"),
    path("logout", MerchantLogoutView.as_view(), name="merchant-logout"),
    path("token/refresh", CookieTokenRefreshView.as_view(), name="merchant-token-refresh"),
    path("info", MerchantInfoView.as_view(), name="merchant-info"),
    # 入驻申请（GET 查状态 / POST 提交）
    path("application", MerchantApplicationView.as_view(), name="merchant-application"),
    # 工作台
    path("dashboard", MerchantDashboardView.as_view(), name="merchant-dashboard"),
    # 商品（GET 列表 / POST 新增）
    path("products", ProductListView.as_view(), name="merchant-product-list"),
    # 商品图片上传（必须在 <int:pk> 之前）
    path("products/upload-image", ProductImageUploadView.as_view(), name="merchant-product-image-upload"),
    # 商品（GET 详情 / PUT 编辑）
    path("products/<int:pk>", ProductDetailView.as_view(), name="merchant-product-detail"),
    # 库存
    path("inventory", InventoryListView.as_view(), name="merchant-inventory-list"),
    path("inventory/records", InventoryRecordListView.as_view(), name="merchant-inventory-records"),
    path("inventory/<int:product_id>", InventoryUpdateView.as_view(), name="merchant-inventory-update"),
    # 发货
    path("shipments", ShipmentTaskListView.as_view(), name="merchant-shipment-list"),
    path("shipments/<int:pk>", ShipmentTaskDetailView.as_view(), name="merchant-shipment-detail"),
    path("shipments/<int:pk>/ship", ShipmentConfirmView.as_view(), name="merchant-shipment-confirm"),
    # 记录
    path("records", RecordListView.as_view(), name="merchant-records"),
]
