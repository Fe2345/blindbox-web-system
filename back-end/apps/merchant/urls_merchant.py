from django.urls import path

from . import views

urlpatterns = [
    # 登录
    path("login", views.MerchantLoginView.as_view(), name="merchant-login"),
    # 商家信息
    path("info", views.MerchantInfoView.as_view(), name="merchant-info"),
    path("application", views.MerchantApplicationView.as_view(), name="merchant-application"),
    # 工作台
    path("dashboard", views.MerchantDashboardView.as_view(), name="merchant-dashboard"),
    # 商品管理
    path("products", views.ProductListView.as_view(), name="merchant-product-list"),
    path("products/submit", views.ProductSubmitView.as_view(), name="merchant-product-submit"),
    path("products/<int:pk>", views.ProductDetailView.as_view(), name="merchant-product-detail"),
    path("products/<int:pk>/edit", views.ProductEditView.as_view(), name="merchant-product-edit"),
    # 库存管理
    path("inventory", views.InventoryListView.as_view(), name="merchant-inventory-list"),
    path("inventory/<int:pk>", views.InventoryUpdateView.as_view(), name="merchant-inventory-update"),
    path("inventory/records", views.InventoryRecordListView.as_view(), name="merchant-inventory-records"),
    # 发货管理
    path("shipments", views.ShipmentListView.as_view(), name="merchant-shipment-list"),
    path("shipments/<int:pk>", views.ShipmentDetailView.as_view(), name="merchant-shipment-detail"),
    path("shipments/<int:pk>/ship", views.ShipmentShipView.as_view(), name="merchant-shipment-ship"),
    # 操作记录
    path("records", views.MerchantRecordListView.as_view(), name="merchant-records"),
]
