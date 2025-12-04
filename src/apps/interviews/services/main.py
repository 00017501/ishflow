"""Interview scheduling service layer."""

from datetime import datetime

from django.db import transaction

from src.apps.accounts.models.users import UserORM
from src.apps.applications.models.applications import ApplicationORM, ApplicationStatus
from src.apps.companies.models.companies import CompanyORM
from src.apps.interviews.models.interviews import InterviewORM, InterviewSlotORM, InterviewStatusOptions, SlotStatus


def get_or_create_interview(application: ApplicationORM, company: CompanyORM) -> InterviewORM:
    """Get or create an interview for the given application."""
    interview, _ = InterviewORM.objects.get_or_create(
        application=application,
        company=company,
        defaults={
            "status": InterviewStatusOptions.PENDING,
        },
    )
    return interview


def create_interview_slot(  # noqa: PLR0913
    interview: InterviewORM,
    proposed_by: UserORM,
    start_time: datetime,
    end_time: datetime,
    location: str,
    meeting_link: str | None = None,
    notes: str = "",
    is_counter_proposal: bool = False,
) -> InterviewSlotORM:
    """Create a new interview slot."""
    status = SlotStatus.COUNTER_PROPOSED if is_counter_proposal else SlotStatus.PROPOSED

    return InterviewSlotORM.objects.create(
        interview=interview,
        proposed_by=proposed_by,
        start_time=start_time,
        end_time=end_time,
        location=location,
        meeting_link=meeting_link,
        notes=notes,
        status=status,
    )


@transaction.atomic
def accept_interview_slot(slot: InterviewSlotORM) -> None:
    """Accept an interview slot and update related records."""
    # Update slot status
    slot.status = SlotStatus.ACCEPTED
    slot.save()

    # Update interview status
    interview = slot.interview
    interview.status = InterviewStatusOptions.SCHEDULED
    interview.save()

    # Reject all other slots for this interview
    InterviewSlotORM.objects.filter(interview=interview).exclude(pk=slot.pk).update(status=SlotStatus.REJECTED)

    # Update application status to interview_scheduled
    interview.application.status = ApplicationStatus.INTERVIEW_SCHEDULED
    interview.application.save()


def reject_interview_slot(slot: InterviewSlotORM) -> None:
    """Reject an interview slot."""
    slot.status = SlotStatus.REJECTED
    slot.save()


def get_interview_slots(interview: InterviewORM) -> list[InterviewSlotORM]:
    """Get all slots for an interview, ordered by creation date."""
    return list(
        InterviewSlotORM.objects.filter(interview=interview).select_related("proposed_by").order_by("-created_at")
    )
