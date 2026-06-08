from django.urls import path

from . import views

urlpatterns = [
    path("points/balance", views.PointsBalanceView.as_view(), name="points-balance"),
    path("points/records", views.PointsRecordListView.as_view(), name="points-records"),
    path("transactions", views.TransactionRecordListView.as_view(), name="transaction-records"),
]
