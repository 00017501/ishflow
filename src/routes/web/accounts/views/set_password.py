"""Set password views for invited employees."""

from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from src.apps.accounts.services.password import set_password_at_invitation
from src.apps.accounts.services.tokens import get_user_from_token
from src.routes.web.accounts.forms.password import SetPasswordForm


@require_http_methods(["GET", "POST"])
def set_password_view(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    """Set password for invited employee."""
    # Retrieve user from token
    user = get_user_from_token.get_user(uidb64, token)
    if user is None:
        messages.error(
            request,
            "The invitation link is invalid or has expired. Please contact your company administrator.",
        )
        return redirect("home:home")

    # Check if user has already accepted
    if user.has_accepted_invitation:
        messages.info(request, "You have already accepted this invitation.")
        return redirect("accounts:login")

    if request.method == "POST":
        form = SetPasswordForm(request.POST)

        if form.is_valid():
            # Set password and activate user
            user = set_password_at_invitation.set_password(user, form.cleaned_data["password"])

            # Log the user in
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")

            messages.success(
                request,
                f"Welcome to {user.company.name}, {user.full_name}! Your account is now active.",
            )
            return redirect("home:home")
    else:
        form = SetPasswordForm()

    context = {
        "form": form,
        "user": user,
    }

    return render(request, "pages/accounts/set_password.html", context)
