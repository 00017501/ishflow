"""Login views."""

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from src.apps.accounts.models.users import UserORM
from src.routes.web.accounts.forms import LoginForm


@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    """Handle user login."""
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("home:home")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Authenticate user
            user: UserORM = authenticate(request, username=email, password=password)  # type: ignore

            if user is not None:
                # Log the user in with Django's default backend (as I also use backend for JWT auth)
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")

                # Get redirect URL from next parameter or default to home
                next_url = request.GET.get("next", "home:home")

                messages.success(request, f"Welcome back, {user.full_name}!")
                return redirect(next_url)
            messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()

    context = {"form": form}

    return render(request, "pages/accounts/login.html", context)
