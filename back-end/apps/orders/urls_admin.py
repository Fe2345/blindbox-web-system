from django.urls import path

from . import views

urlpatterns = [
    path("orders", views.AdminOrderListView.as_view(), name="admin-order-list"),
    path("orders/<int:pk>/ship", views.AdminOrderShipView.as_view(), name="admin-order-ship"),
]
