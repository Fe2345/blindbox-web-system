from django.urls import path

from . import views

urlpatterns = [
    path("blindboxes", views.AdminBlindBoxListView.as_view(), name="admin-blindbox-list"),
    path("blindboxes/<int:pk>", views.AdminBlindBoxDetailView.as_view(), name="admin-blindbox-detail"),
    path("blindboxes/<int:pk>/status", views.AdminBlindBoxStatusView.as_view(), name="admin-blindbox-status"),
    path("blindboxes/<int:pk>/prizes", views.AdminPrizePoolView.as_view(), name="admin-blindbox-prizes"),
    path("blindbox/draw-records", views.AdminDrawRecordListView.as_view(), name="admin-draw-records"),
]
