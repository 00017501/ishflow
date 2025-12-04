"""Employee management views."""

from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.forms import Form
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from src.apps.accounts.models.users import UserORM, UserTypeOptions
from src.apps.accounts.schemas.registration import EmployeeInvitationDataSchema
from src.apps.accounts.services.registration import create_employee_user_flow
from src.routes.web.accounts.forms.invitation import InviteEmployeeForm


User = get_user_model()


class CompanyRequiredMixin:
    """Mixin to ensure user has a company and is an employer."""

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401
        """Check if user is employer and has a company."""
        user: UserORM = request.user  # type: ignore

        if user.type != UserTypeOptions.EMPLOYER:
            raise PermissionDenied("Only employers can access this page.")

        if not user.company:
            raise PermissionDenied("You must be associated with a company.")

        return super().dispatch(request, *args, **kwargs)  # type: ignore


class EmployeesListView(LoginRequiredMixin, PermissionRequiredMixin, CompanyRequiredMixin, ListView):
    """Display list of employees in the company."""

    model = UserORM
    template_name = "pages/accounts/employees/list.html"
    context_object_name = "employees"
    permission_required = "accounts.view_employees"
    raise_exception = True

    def get_queryset(self) -> QuerySet[UserORM]:
        """Get employees for the current user's company."""
        user: UserORM = self.request.user  # type: ignore
        return user.company.employees.all().order_by("-created_at")  # type: ignore

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Add company to context."""
        context = super().get_context_data(**kwargs)
        user: UserORM = self.request.user  # type: ignore
        context["company"] = user.company
        return context


class InviteEmployeeView(LoginRequiredMixin, PermissionRequiredMixin, CompanyRequiredMixin, FormView):
    """Invite a new employee to the company."""

    template_name = "pages/accounts/employees/invite.html"
    form_class = InviteEmployeeForm
    success_url = reverse_lazy("accounts:employees_list")
    permission_required = "accounts.invite_employees"
    raise_exception = True

    def form_valid(self, form: Form) -> HttpResponse:
        """Process the invitation."""
        user: UserORM = self.request.user  # type: ignore

        # Create user with invited status and send invitation email
        new_user = create_employee_user_flow(
            EmployeeInvitationDataSchema(**form.cleaned_data),
            request=self.request,
            company=user.company,
        )

        messages.success(
            self.request,
            f"Invitation sent to {new_user.full_name} ({new_user.email}).",
        )

        return super().form_valid(form)


employees_list_view = EmployeesListView.as_view()
invite_employee_view = InviteEmployeeView.as_view()
