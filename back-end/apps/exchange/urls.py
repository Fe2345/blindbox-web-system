from django.urls import path

from . import views

urlpatterns = [
    path("exchange/posts", views.ExchangePostListView.as_view(), name="exchange-post-list"),
    path("exchange/posts/<int:pk>", views.ExchangePostDetailView.as_view(), name="exchange-post-detail"),
    path("exchange/posts/<int:pk>/apply", views.ExchangeApplyView.as_view(), name="exchange-apply"),
    path("exchange/applications", views.ExchangeApplicationListView.as_view(), name="exchange-application-list"),
    path("exchange/applications/<int:pk>", views.ExchangeApplicationDetailView.as_view(), name="exchange-application-detail"),
    path("exchange/applications/<int:pk>/accept", views.ExchangeApplicationAcceptView.as_view(), name="exchange-application-accept"),
    path("exchange/applications/<int:pk>/reject", views.ExchangeApplicationRejectView.as_view(), name="exchange-application-reject"),
]
