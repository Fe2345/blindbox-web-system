from django.urls import path

from . import views

urlpatterns = [
    path("merchants", views.AdminMerchantListView.as_view(), name="admin-merchant-list"),
    path("merchants/<int:pk>/review", views.AdminMerchantReviewView.as_view(), name="admin-merchant-review"),
    path("merchants/<int:pk>/status", views.AdminMerchantStatusView.as_view(), name="admin-merchant-status"),
    path("products", views.AdminProductListView.as_view(), name="admin-product-list"),
    path("products/<int:pk>", views.AdminProductDetailView.as_view(), name="admin-product-detail"),
    path("products/<int:pk>/review", views.AdminProductReviewView.as_view(), name="admin-product-review"),
    path("products/<int:pk>/offline", views.AdminProductOfflineView.as_view(), name="admin-product-offline"),
]
