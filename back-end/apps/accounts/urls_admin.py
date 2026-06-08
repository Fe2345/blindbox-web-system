from django.urls import path

from . import views

urlpatterns = [
    path("users", views.AdminUserListView.as_view(), name="admin-user-list"),
    path("users/<int:pk>/status", views.AdminUserStatusView.as_view(), name="admin-user-status"),
]
