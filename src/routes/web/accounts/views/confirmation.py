"""Email confirmation views."""

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

from src.apps.accounts.services.password import accept_invitation
from src.apps.accounts.services.tokens import get_user_from_token


@require_GET
def confirm_email_view(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    """Confirm user email address."""
    if user := get_user_from_token.get_user(uidb64, token):
        # Activate user account
        accept_invitation(user)

        messages.success(
            request,
            "Your email has been confirmed successfully! You can now use all features.",
        )
        return redirect("home:home")
    messages.error(
        request,
        "The confirmation link is invalid or has expired. Please request a new one.",
    )
    return redirect("home:home")
