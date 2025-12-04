"""Logout views."""

from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def logout_view(request: HttpRequest) -> HttpResponse:
    """Handle user logout."""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been successfully logged out.")

    return redirect("home:home")
