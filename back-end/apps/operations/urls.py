from django.urls import path

from . import views

urlpatterns = [
    path("rules", views.AdminRuleConfigView.as_view(), name="admin-rule-config"),
    path("logs", views.AdminOpLogListView.as_view(), name="admin-op-log"),
    path("exceptions", views.AdminExceptionListView.as_view(), name="admin-exception-list"),
    path("exceptions/<int:pk>/resolve", views.AdminExceptionResolveView.as_view(), name="admin-exception-resolve"),
    path("ledger", views.AdminLedgerListView.as_view(), name="admin-ledger"),
]
