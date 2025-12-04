"""Interview scheduling views."""

from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView

from src.apps.accounts.models.users import UserORM
from src.apps.applications.models.applications import ApplicationORM
from src.apps.interviews.models.interviews import InterviewORM, InterviewSlotORM, SlotStatus
from src.apps.interviews.services.main import (
    accept_interview_slot,
    create_interview_slot,
    get_interview_slots,
    get_or_create_interview,
    reject_interview_slot,
)
from src.routes.web.interviews.forms import InterviewSlotForm


class ProposeInterviewSlotView(LoginRequiredMixin, FormView):  # type: ignore[type-arg]
    """Employer proposes interview time slots for an application."""

    template_name = "pages/interviews/propose_slot.html"
    form_class = InterviewSlotForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401
        """Verify the application belongs to employer's company."""
        self.application = get_object_or_404(
            ApplicationORM.objects.select_related("post", "post__company", "applicant__user"),
            pk=kwargs["application_pk"],
            post__company=request.user.company,  # type: ignore
        )
        self.interview = get_or_create_interview(self.application, request.user.company)  # type: ignore
        return super().dispatch(request, *args, **kwargs)  # type: ignore

    def form_valid(self, form: InterviewSlotForm) -> HttpResponse:  # type: ignore[override]
        """Create interview slot."""
        create_interview_slot(
            interview=self.interview,
            proposed_by=self.request.user,  # type: ignore
            start_time=form.cleaned_data["start_time"],
            end_time=form.cleaned_data["end_time"],
            location=form.cleaned_data["location"],
            meeting_link=form.cleaned_data.get("meeting_link"),
            notes=form.cleaned_data.get("notes", ""),
            is_counter_proposal=False,
        )
        messages.success(self.request, f"Interview slot proposed to {self.application.applicant.user.full_name}.")
        return redirect("jobs:applicants", pk=self.application.post.pk)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Add application and existing slots to context."""
        context = super().get_context_data(**kwargs)
        context["application"] = self.application
        context["existing_slots"] = get_interview_slots(self.interview)
        return context


propose_interview_slot_view = ProposeInterviewSlotView.as_view()


class ViewInterviewSlotsView(LoginRequiredMixin, FormView):  # type: ignore[type-arg]
    """Candidate views proposed interview slots for their application."""

    template_name = "pages/interviews/view_slots.html"
    form_class = InterviewSlotForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401
        """Get application and interview data."""
        self.application = get_object_or_404(
            ApplicationORM.objects.select_related("post", "post__company"),
            pk=kwargs["application_pk"],
        )
        try:
            self.interview = InterviewORM.objects.get(application=self.application)
            self.slots = get_interview_slots(self.interview)
        except InterviewORM.DoesNotExist:
            self.interview = None
            self.slots = []
        return super().dispatch(request, *args, **kwargs)  # type: ignore

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Add application and slots to context."""
        context = super().get_context_data(**kwargs)
        context["application"] = self.application
        context["slots"] = self.slots
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401, ARG002
        """Handle GET request."""
        return self.render_to_response(self.get_context_data())


view_interview_slots_view = ViewInterviewSlotsView.as_view()


@login_required
@require_http_methods(["POST"])
def accept_interview_slot_view(request: HttpRequest, slot_pk: int) -> HttpResponse:
    """Candidate accepts a proposed interview slot."""
    slot = get_object_or_404(
        InterviewSlotORM.objects.select_related("interview__application__applicant__user", "interview"),
        pk=slot_pk,
        interview__application__applicant__user=request.user,
    )

    # Use service layer to handle acceptance logic
    accept_interview_slot(slot)

    messages.success(request, "Interview slot accepted! The employer has been notified.")
    return redirect("jobs:my_applications")


class CounterProposeSlotView(LoginRequiredMixin, FormView):  # type: ignore[type-arg]
    """Candidate proposes alternative interview time slot."""

    template_name = "pages/interviews/counter_propose.html"
    form_class = InterviewSlotForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: ANN401
        """Verify application belongs to the candidate."""
        self.application = get_object_or_404(
            ApplicationORM.objects.select_related("post", "post__company"),
            pk=kwargs["application_pk"],
            applicant__user=request.user,
        )
        self.interview = get_or_create_interview(self.application, self.application.post.company)
        return super().dispatch(request, *args, **kwargs)  # type: ignore

    def form_valid(self, form: InterviewSlotForm) -> HttpResponse:  # type: ignore[override]
        """Create counter-proposal slot."""
        user: UserORM = self.request.user  # type: ignore
        create_interview_slot(
            interview=self.interview,
            proposed_by=user,
            start_time=form.cleaned_data["start_time"],
            end_time=form.cleaned_data["end_time"],
            location=form.cleaned_data["location"],
            meeting_link=form.cleaned_data.get("meeting_link"),
            notes=form.cleaned_data.get("notes", ""),
            is_counter_proposal=True,
        )
        messages.success(self.request, f"Alternative time slot proposed to {self.application.post.company.name}.")
        return redirect("jobs:my_applications")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Add application and existing slots to context."""
        context = super().get_context_data(**kwargs)
        context["application"] = self.application
        context["existing_slots"] = get_interview_slots(self.interview)
        return context


counter_propose_slot_view = CounterProposeSlotView.as_view()


@login_required
@require_http_methods(["POST"])
def reject_interview_slot_view(request: HttpRequest, slot_pk: int) -> HttpResponse:
    """Candidate or employer rejects a proposed interview slot."""
    slot = get_object_or_404(
        InterviewSlotORM.objects.select_related("interview__application", "interview__application__post__company"),
        pk=slot_pk,
    )

    # Check permissions: either candidate or company can reject
    is_candidate = slot.interview.application.applicant.user == request.user
    is_employer = slot.interview.application.post.company == request.user.company  # type: ignore

    if not (is_candidate or is_employer):
        raise PermissionDenied("You don't have permission to reject this slot.")

    # Use service layer to handle rejection
    reject_interview_slot(slot)

    messages.info(request, "Interview slot rejected.")

    # Redirect based on user type
    if is_candidate:
        return redirect("interviews:view_slots", application_pk=slot.interview.application.pk)
    return redirect("interviews:propose_slot", application_pk=slot.interview.application.pk)


@login_required
@require_http_methods(["POST"])
def accept_counter_proposal_view(request: HttpRequest, slot_pk: int) -> HttpResponse:
    """Employer accepts a counter-proposed slot from candidate."""
    slot = get_object_or_404(
        InterviewSlotORM.objects.select_related("interview__application__post__company", "interview"),
        pk=slot_pk,
        interview__application__post__company=request.user.company,  # type: ignore
        status=SlotStatus.COUNTER_PROPOSED,
    )

    # Use service layer to handle acceptance logic
    accept_interview_slot(slot)

    messages.success(request, "Counter-proposal accepted! Interview has been scheduled.")
    return redirect("jobs:applicants", pk=slot.interview.application.post.pk)
