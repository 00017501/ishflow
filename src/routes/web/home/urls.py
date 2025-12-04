"""Home URL patterns."""

from django.urls import path

from src.routes.web.home import views


urlpatterns = [
    path("", views.home_view, name="home"),
]
