from django.urls import path

from .views import (
    AddressDetailView,
    AddressListView,
    CookieTokenRefreshView,
    DivisionListView,
    LoginView,
    LogoutView,
    RegisterView,
)

urlpatterns = [
    path("divisions/", DivisionListView.as_view(), name="division-list"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="token-refresh"),
    path("user/addresses/", AddressListView.as_view(), name="address-list"),
    path("user/addresses/<int:pk>/", AddressDetailView.as_view(), name="address-detail"),
]
