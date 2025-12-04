"""Views for user profile editing."""

from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from src.apps.accounts.models.users import UserORM, UserTypeOptions
from src.apps.candidates.models.candidates import CandidateORM
from src.apps.companies.models.companies import CompanyORM
from src.routes.web.accounts.forms.profile import CandidateProfileForm, CompanyProfileForm, UserProfileForm


class UserProfileView(LoginRequiredMixin, UpdateView):
    """Display and edit user profile."""

    model = UserORM
    form_class = UserProfileForm
    template_name = "pages/accounts/profile/edit.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset: QuerySet[UserORM] | None = None) -> UserORM:  # noqa: ARG002
        """Return the current user."""
        return self.request.user  # type: ignore[return-value]

    def form_valid(self, form: UserProfileForm) -> HttpResponse:
        """Handle successful form submission."""
        messages.success(self.request, "Your profile has been updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Add form to context as user_form for template compatibility."""
        context = super().get_context_data(**kwargs)
        context["user_form"] = context["form"]
        return context


class CandidateProfileView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Display and edit candidate profile."""

    model = CandidateORM
    form_class = CandidateProfileForm
    template_name = "pages/accounts/profile/candidate.html"
    success_url = reverse_lazy("accounts:candidate_profile")
    permission_required = "candidates.change_candidateorm"
    raise_exception = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401
        """Ensure user is a candidate."""
        user: UserORM = request.user  # type: ignore[assignment]
        if user.type != UserTypeOptions.CANDIDATE:
            raise PermissionDenied("Only candidates can access candidate profile.")
        return super().dispatch(request, *args, **kwargs)  # type: ignore

    def get_object(self, queryset: QuerySet[CandidateORM] | None = None) -> CandidateORM:  # noqa: ARG002
        """Get or create candidate profile for current user."""
        candidate_profile, _ = CandidateORM.objects.get_or_create(user=self.request.user)
        return candidate_profile

    def form_valid(self, form: CandidateProfileForm) -> HttpResponse:  # type: ignore[override]
        """Handle successful form submission."""
        messages.success(self.request, "Your candidate profile has been updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Add candidate profile to context."""
        context = super().get_context_data(**kwargs)
        context["candidate_profile"] = self.get_object()
        return context


class CompanyProfileView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):  # type: ignore[type-arg]
    """Display and edit company profile."""

    model = CompanyORM
    form_class = CompanyProfileForm
    template_name = "pages/accounts/profile/company.html"
    success_url = reverse_lazy("accounts:company_profile")
    permission_required = "companies.view_companyorm"
    raise_exception = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401
        """Ensure user is an employer with a company."""
        user: UserORM = request.user  # type: ignore[assignment]
        if user.type != UserTypeOptions.EMPLOYER:
            raise PermissionDenied("Only employers can access company profile.")
        if not user.company:
            raise PermissionDenied("You must be associated with a company to edit company profile.")
        return super().dispatch(request, *args, **kwargs)  # type: ignore

    def get_object(self, queryset: QuerySet[CompanyORM] | None = None) -> CompanyORM:  # noqa: ARG002
        """Return the current user's company."""
        return self.request.user.company  # type: ignore[return-value]

    def form_valid(self, form: CompanyProfileForm) -> HttpResponse:  # type: ignore[override]
        """Handle successful form submission - requires change permission."""
        # When user is saving company profile, ensure they have change permission
        user: UserORM = self.request.user  # type: ignore[assignment]
        if not user.has_perm("companies.change_companyorm"):
            raise PermissionDenied("You don't have permission to edit company profile.")
        messages.success(self.request, "Company profile has been updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Add company to context."""
        context = super().get_context_data(**kwargs)
        context["company"] = self.get_object()
        return context


profile_view = UserProfileView.as_view()
candidate_profile_view = CandidateProfileView.as_view()
company_profile_view = CompanyProfileView.as_view()
