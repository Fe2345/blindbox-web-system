from django.urls import path

from . import views

urlpatterns = [
    path("prize-stock", views.MerchantPrizeStockView.as_view(), name="merchant-prize-stock"),
    path("prize-stock/<int:prize_id>/replenish", views.MerchantPrizeReplenishView.as_view(), name="merchant-prize-replenish"),
    path("shipment-orders", views.MerchantShipmentOrderView.as_view(), name="merchant-shipment-orders"),
    path("shipment-orders/<int:record_id>/ship", views.MerchantShipView.as_view(), name="merchant-ship"),
]
