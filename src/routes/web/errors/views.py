"""Custom error handlers."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def page_not_found_view(request: HttpRequest, exception: object = None) -> HttpResponse:  # noqa: ARG001
    """Handle 404 errors."""
    return render(request, "errors/404.html", status=404)


def forbidden_view(request: HttpRequest, exception: object = None) -> HttpResponse:  # noqa: ARG001
    """Handle 403 errors."""
    return render(request, "errors/403.html", status=403)


def server_error_view(request: HttpRequest) -> HttpResponse:
    """Handle 500 errors."""
    return render(request, "errors/500.html", status=500)


def too_many_requests_view(request: HttpRequest, exception: object = None) -> HttpResponse:  # noqa: ARG001
    """Handle 429 errors (rate limiting/too many requests)."""
    return render(request, "errors/429.html", status=429)
