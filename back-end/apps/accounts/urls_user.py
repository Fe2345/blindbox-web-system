from django.urls import path

from .views import AddressDetailView, AddressListView, DivisionListView

urlpatterns = [
    path("divisions/", DivisionListView.as_view(), name="division-list"),
    path("user/addresses/", AddressListView.as_view(), name="address-list"),
    path("user/addresses/<int:pk>/", AddressDetailView.as_view(), name="address-detail"),
]
