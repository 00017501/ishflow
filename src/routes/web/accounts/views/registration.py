"""Registration views."""

from typing import Any

from django.contrib import messages
from django.contrib.auth import login
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from src.apps.accounts.models.users import UserORM
from src.apps.accounts.services.registration import send_confirmation_email
from src.routes.web.accounts.forms import RegistrationForm


class RegisterView(FormView):
    """Handle user registration for both candidates and employers."""

    template_name = "pages/accounts/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("home:home")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401
        """Redirect if user is already authenticated."""
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in.")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)  # type: ignore

    def get_initial(self) -> dict[str, Any]:
        """Pre-fill user type from query parameter."""
        initial = super().get_initial()
        user_type = self.request.GET.get("type")
        if user_type in ["candidate", "employer"]:
            initial["user_type"] = user_type
        return initial

    def form_valid(self, form: RegistrationForm) -> HttpResponse:
        """Handle successful registration."""
        with transaction.atomic():
            # Create user
            user: UserORM = form.save()

            # Send confirmation email
            send_confirmation_email(self.request, user)

        # Log the user in with Django's default backend
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")

        # Show success message
        messages.success(
            self.request,
            f"Welcome, {user.full_name}! Please check your email to confirm your account.",
        )

        return super().form_valid(form)


register_view = RegisterView.as_view()
