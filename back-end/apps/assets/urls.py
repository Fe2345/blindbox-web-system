from django.urls import path

from . import views

urlpatterns = [
    path("assets", views.AssetListView.as_view(), name="asset-list"),
    path("assets/<int:pk>", views.AssetDetailView.as_view(), name="asset-detail"),
    path("assets/<int:pk>/recycle", views.AssetRecycleView.as_view(), name="asset-recycle"),
    path("assets/<int:pk>/ship", views.AssetShipView.as_view(), name="asset-ship"),
    path("assets/<int:pk>/publish-exchange", views.AssetPublishExchangeView.as_view(), name="asset-publish-exchange"),
]
