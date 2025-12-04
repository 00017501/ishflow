"""URL configuration for the accounts app."""

from django.urls import path

from src.routes.api.accounts.v1.views.login import LoginView, LogoutView, RefreshView
from src.routes.api.accounts.v1.views.profile import RetrieveProfileView, UpdateProfileView


urlpatterns = [
    # Authentication endpoints
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", RefreshView.as_view(), name="token_refresh"),
    # Profile management endpoints
    path("profile/", RetrieveProfileView.as_view(), name="retrieve-profile"),
    path("profile/update/", UpdateProfileView.as_view(), name="update-profile"),
]
