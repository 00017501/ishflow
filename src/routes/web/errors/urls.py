"""Error URL patterns."""

from django.urls import path

from src.routes.web.errors import views


urlpatterns = [
    path("403/", views.forbidden_view, name="forbidden"),
    path("404/", views.page_not_found_view, name="not_found"),
    path("429/", views.too_many_requests_view, name="too_many_requests"),
    path("500/", views.server_error_view, name="server_error"),
]
