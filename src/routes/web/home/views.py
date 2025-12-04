"""Home views."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_view(request: HttpRequest) -> HttpResponse:
    """Render the home page."""
    return render(request, "pages/views/home.html")
