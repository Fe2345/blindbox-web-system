from django.urls import path

from . import views

urlpatterns = [
    path("login", views.AdminLoginView.as_view(), name="admin-login"),
    path("logout", views.LogoutView.as_view(), name="admin-logout"),
    path("token/refresh", views.CookieTokenRefreshView.as_view(), name="admin-token-refresh"),
    path("users", views.AdminUserListView.as_view(), name="admin-user-list"),
    path("users/<int:pk>/status", views.AdminUserStatusView.as_view(), name="admin-user-status"),
]
