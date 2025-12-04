"""Application views for candidates and employers."""

from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, ListView

from src.apps.applications.models.applications import ApplicationORM, ApplicationStatus
from src.apps.applications.services.main import (
    check_already_applied,
    create_application,
    filter_applications,
    send_status_update_email,
    update_application_status,
)
from src.apps.candidates.models import CandidateORM
from src.apps.jobs.models.jobs import JobPostORM
from src.routes.web.jobs.forms import JobApplicationForm


class JobApplyView(LoginRequiredMixin, PermissionRequiredMixin, FormView):  # type: ignore[type-arg]
    """Apply to a job post."""

    template_name = "pages/jobs/apply.html"
    form_class = JobApplicationForm
    permission_required = "applications.add_applicationorm"
    raise_exception = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401
        """Verify candidate profile and check if already applied."""
        self.job = get_object_or_404(JobPostORM.objects.select_related("company"), pk=kwargs["pk"])

        if not hasattr(request.user, "candidate_profile"):
            messages.error(request, "You must have a candidate profile to apply for jobs.")
            return redirect("accounts:candidate_profile")

        self.candidate: CandidateORM = request.user.candidate_profile  # type: ignore

        if check_already_applied(self.job, self.candidate):
            messages.warning(request, "You have already applied to this job.")
            return redirect("jobs:detail", pk=kwargs["pk"])

        return super().dispatch(request, *args, **kwargs)  # type: ignore

    def get_initial(self) -> dict[str, Any]:
        """Pre-fill with candidate's default cover letter if available."""
        initial = super().get_initial()
        if self.candidate.cover_letter:
            initial["cover_letter"] = self.candidate.cover_letter
        return initial

    def form_valid(self, form: JobApplicationForm) -> HttpResponse:  # type: ignore[override]
        """Create application using service layer."""
        create_application(
            job=self.job,
            candidate=self.candidate,
            cover_letter=form.cleaned_data.get("cover_letter", ""),
        )
        messages.success(
            self.request,
            f"Your application to '{self.job.title}' has been submitted successfully!",
        )
        return redirect("jobs:my_applications")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Add job to context."""
        context = super().get_context_data(**kwargs)
        context["job"] = self.job
        return context


job_apply_view = JobApplyView.as_view()


class MyApplicationsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):  # type: ignore[type-arg]
    """Display list of applications submitted by the candidate."""

    model = ApplicationORM
    template_name = "pages/jobs/my_applications.html"
    context_object_name = "applications"
    paginate_by = 10
    permission_required = "applications.view_applicationorm"
    raise_exception = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401
        """Verify candidate profile exists."""
        if not hasattr(request.user, "candidate_profile"):
            messages.error(request, "You must have a candidate profile to view applications.")
            return redirect("accounts:candidate_profile")
        return super().dispatch(request, *args, **kwargs)  # type: ignore

    def get_queryset(self) -> QuerySet[ApplicationORM]:
        """Get applications for the current candidate."""
        return (
            ApplicationORM.objects.filter(applicant=self.request.user.candidate_profile)  # type: ignore
            .select_related("post", "post__company")
            .order_by("-created_at")
        )


my_applications_view = MyApplicationsView.as_view()


class ReceivedApplicationsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Display all applications received by the company (employer view)."""

    model = ApplicationORM
    template_name = "pages/jobs/received_applications.html"
    context_object_name = "applications"
    paginate_by = 20
    permission_required = "applications.view_applicationorm"
    raise_exception = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401
        """Verify company exists."""
        if not request.user.company:  # type: ignore
            messages.error(request, "You must be associated with a company to view applications.")
            return redirect("jobs:list")
        return super().dispatch(request, *args, **kwargs)  # type: ignore

    def get_queryset(self) -> QuerySet[ApplicationORM]:
        """Get filtered applications for the company."""
        applications = (
            ApplicationORM.objects.filter(post__company=self.request.user.company)  # type: ignore
            .select_related("post", "applicant", "applicant__user")
            .order_by("-created_at")
        )

        # Apply filters using service layer
        return filter_applications(
            applications,
            status=self.request.GET.get("status", ""),
            job_id=self.request.GET.get("job", ""),
            skill=self.request.GET.get("skill", ""),
            title=self.request.GET.get("title", ""),
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Add filter parameters and company jobs to context."""
        context = super().get_context_data(**kwargs)
        context["company_jobs"] = JobPostORM.objects.filter(company=self.request.user.company).values("id", "title")  # type: ignore
        context["status_filter"] = self.request.GET.get("status", "")
        context["job_filter"] = self.request.GET.get("job", "")
        context["skill_filter"] = self.request.GET.get("skill", "")
        context["title_search"] = self.request.GET.get("title", "")
        return context


received_applications_view = ReceivedApplicationsView.as_view()


class JobApplicantsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):  # type: ignore[type-arg]
    """Display list of applications for a specific job post (employer view)."""

    model = ApplicationORM
    template_name = "pages/jobs/applicants.html"
    context_object_name = "applications"
    paginate_by = 15
    permission_required = "applications.view_applicationorm"
    raise_exception = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401
        """Get job and verify it belongs to the company."""
        self.job = get_object_or_404(JobPostORM, pk=kwargs["pk"], company=request.user.company)  # type: ignore
        return super().dispatch(request, *args, **kwargs)  # type: ignore

    def get_queryset(self) -> QuerySet[ApplicationORM]:
        """Get filtered applications for the job."""
        applications = (
            ApplicationORM.objects.filter(post=self.job)
            .select_related("applicant", "applicant__user")
            .order_by("-created_at")
        )

        # Apply filters using service layer
        return filter_applications(
            applications,
            status=self.request.GET.get("status", ""),
            skill=self.request.GET.get("skill", ""),
            title=self.request.GET.get("title", ""),
            min_experience=self.request.GET.get("min_experience", ""),
            has_resume=self.request.GET.get("has_resume", ""),
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Add job and filter parameters to context."""
        context = super().get_context_data(**kwargs)
        context["job"] = self.job
        context["status_filter"] = self.request.GET.get("status", "")
        context["skill_filter"] = self.request.GET.get("skill", "")
        context["title_search"] = self.request.GET.get("title", "")
        context["min_experience"] = self.request.GET.get("min_experience", "")
        context["has_resume"] = self.request.GET.get("has_resume", "")
        return context


job_applicants_view = JobApplicantsView.as_view()


@login_required
@permission_required("applications.change_applicationorm", raise_exception=True)
@require_http_methods(["POST"])
def application_status_update_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Update application status (employer only)."""
    application = get_object_or_404(
        ApplicationORM.objects.select_related("post", "post__company", "applicant__user"),
        pk=pk,
        post__company=request.user.company,  # type: ignore
    )

    old_status = application.status
    new_status: ApplicationStatus = request.POST.get("status", old_status)  # type: ignore

    # Use service layer to update status
    if update_application_status(application, new_status):
        # Send email notification using service layer
        send_status_update_email(application, request, old_status)

        messages.success(
            request,
            f"Application status updated to '{application.get_status_display()}'.",  # type: ignore
        )
    else:
        messages.error(request, "Invalid status value.")

    # Redirect back to applicants page
    return redirect("jobs:applicants", pk=application.post.pk)
