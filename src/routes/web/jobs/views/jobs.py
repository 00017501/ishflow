"""Job post views."""

from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from src.apps.applications.models.applications import ApplicationORM
from src.apps.jobs.models.jobs import JobPostORM
from src.apps.jobs.services.main import search_and_filter_jobs
from src.routes.web.jobs.forms import JobPostForm


class JobListView(ListView):  # type: ignore[type-arg]
    """Display list of all published job posts."""

    model = JobPostORM
    template_name = "pages/jobs/list.html"
    context_object_name = "jobs"
    paginate_by = 5

    def get_queryset(self) -> QuerySet[JobPostORM]:
        """Get filtered and searched jobs using service layer."""
        return search_and_filter_jobs(
            search_query=self.request.GET.get("q", ""),
            job_type=self.request.GET.get("type", ""),
            location=self.request.GET.get("location", ""),
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Add search parameters to context."""
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        context["job_type"] = self.request.GET.get("type", "")
        context["location"] = self.request.GET.get("location", "")

        # Preserve GET parameters for pagination
        get_params = self.request.GET.copy()
        if "page" in get_params:
            get_params.pop("page")
        context["get_params"] = get_params.urlencode()

        return context


job_list_view = JobListView.as_view()


class JobDetailView(DetailView):  # type: ignore[type-arg]
    """Display detailed view of a job post."""

    model = JobPostORM
    template_name = "pages/jobs/detail.html"
    context_object_name = "job"

    def get_queryset(self) -> QuerySet[JobPostORM]:
        """Optimize query with company."""
        return JobPostORM.objects.select_related("company")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Check if user has already applied."""
        context = super().get_context_data(**kwargs)
        has_applied = False
        if self.request.user.is_authenticated and hasattr(self.request.user, "candidate_profile"):
            has_applied = ApplicationORM.objects.filter(
                post=self.object,
                applicant=self.request.user.candidate_profile,  # type: ignore
            ).exists()
        context["has_applied"] = has_applied
        return context


job_detail_view = JobDetailView.as_view()


class MyJobsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):  # type: ignore[type-arg]
    """Display list of jobs posted by the employer's company."""

    model = JobPostORM
    template_name = "pages/jobs/my_jobs.html"
    context_object_name = "jobs"
    paginate_by = 10
    permission_required = "jobs.view_jobpostorm"
    raise_exception = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401
        """Verify company exists."""
        if not request.user.company:  # type: ignore
            messages.error(request, "You must be associated with a company.")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)  # type: ignore

    def get_queryset(self) -> QuerySet[JobPostORM]:
        """Get jobs for the current company."""
        return JobPostORM.objects.filter(company=self.request.user.company).order_by("-created_at")  # type: ignore


my_jobs_view = MyJobsView.as_view()


class JobCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  # type: ignore[type-arg]
    """Create a new job post."""

    model = JobPostORM
    form_class = JobPostForm
    template_name = "pages/jobs/form.html"
    success_url = reverse_lazy("jobs:my_jobs")
    permission_required = "jobs.add_jobpostorm"
    raise_exception = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401
        """Verify company exists."""
        if not request.user.company:  # type: ignore
            messages.error(request, "You must be associated with a company to post jobs.")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)  # type: ignore

    def form_valid(self, form: JobPostForm) -> HttpResponse:
        """Associate job with company."""
        form.instance.company = self.request.user.company  # type: ignore
        messages.success(self.request, f"Job post '{form.instance.title}' created successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Add action to context."""
        context = super().get_context_data(**kwargs)
        context["action"] = "Create"
        return context


job_create_view = JobCreateView.as_view()


class JobEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Edit an existing job post."""

    model = JobPostORM
    form_class = JobPostForm
    template_name = "pages/jobs/form.html"
    success_url = reverse_lazy("jobs:my_jobs")
    permission_required = "jobs.change_jobpostorm"
    raise_exception = True

    def get_queryset(self) -> QuerySet[JobPostORM]:
        """Only allow editing jobs from user's company."""
        return JobPostORM.objects.filter(company=self.request.user.company)  # type: ignore

    def form_valid(self, form: JobPostForm) -> HttpResponse:
        """Show success message."""
        messages.success(self.request, f"Job post '{form.instance.title}' updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Add job and action to context."""
        context = super().get_context_data(**kwargs)
        context["job"] = self.object
        context["action"] = "Edit"
        return context


job_edit_view = JobEditView.as_view()


@login_required
@permission_required("jobs.delete_jobpostorm", raise_exception=True)
@require_http_methods(["POST"])
def job_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Delete a job post."""
    job = get_object_or_404(JobPostORM, pk=pk, company=request.user.company)  # type: ignore
    title = job.title
    job.delete()

    messages.success(request, f"Job post '{title}' deleted successfully!")
    return redirect("jobs:my_jobs")
