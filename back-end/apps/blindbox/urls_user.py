from django.urls import path

from . import views

urlpatterns = [
    path("blindboxes", views.BlindBoxListView.as_view(), name="blindbox-list"),
    path("blindboxes/<int:pk>", views.BlindBoxDetailView.as_view(), name="blindbox-detail"),
    path("blindboxes/<int:pk>/draw", views.DrawView.as_view(), name="blindbox-draw"),
]
