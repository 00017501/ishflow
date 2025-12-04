"""Interview models."""

from django.db import models

from src.apps.shared.models.core import BaseORM, CompanyIncludedBaseORM


class InterviewStatusOptions(models.TextChoices):
    """Enumeration of possible interview statuses."""

    PENDING = "pending", "Pending Confirmation"
    SCHEDULED = "scheduled", "Scheduled"
    COMPLETED = "completed", "Completed"
    CANCELED = "canceled", "Canceled"


class SlotStatus(models.TextChoices):
    """Status of interview slot proposals."""

    PROPOSED = "proposed", "Proposed by Company"
    COUNTER_PROPOSED = "counter_proposed", "Counter-Proposed by Candidate"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"


class InterviewORM(CompanyIncludedBaseORM):
    """Model representing an interview for a job application."""

    # =================== RELATIONSHIPS =================== #

    application = models.ForeignKey(
        to="applications.ApplicationORM",
        on_delete=models.CASCADE,
        related_name="interviews",
        null=False,
        blank=False,
        verbose_name="application",
        help_text="The job application associated with this interview",
    )

    # =================== DETAILS =================== #
    status = models.CharField(
        max_length=20,
        choices=InterviewStatusOptions.choices,
        default=InterviewStatusOptions.PENDING,
        verbose_name="interview status",
        help_text="Current status of the interview",
    )

    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name="notes",
        help_text="Additional notes about the interview",
    )

    def __str__(self) -> str:
        """String representation of the InterviewORM."""
        accepted_slot = self.slots.filter(status=SlotStatus.ACCEPTED).first()
        if accepted_slot:
            return f"Interview for {self.application} on {accepted_slot.start_time}"
        return f"Interview for {self.application} (pending schedule)"

    class Meta:
        """Meta options for InterviewORM model."""

        verbose_name = "interview"
        verbose_name_plural = "interviews"


class InterviewSlotORM(BaseORM):
    """Model for managing interview time slot proposals."""

    # =================== RELATIONSHIPS =================== #

    interview = models.ForeignKey(
        to="interviews.InterviewORM",
        on_delete=models.CASCADE,
        related_name="slots",
        null=False,
        blank=False,
        verbose_name="interview",
        help_text="The interview this slot is for",
    )

    proposed_by = models.ForeignKey(
        to="accounts.UserORM",
        on_delete=models.CASCADE,
        related_name="proposed_slots",
        null=False,
        blank=False,
        verbose_name="proposed by",
        help_text="User who proposed this slot",
    )

    # =================== DETAILS =================== #

    start_time = models.DateTimeField(
        null=False,
        blank=False,
        verbose_name="start time",
        help_text="Proposed interview start time",
    )

    end_time = models.DateTimeField(
        null=False,
        blank=False,
        verbose_name="end time",
        help_text="Proposed interview end time",
    )

    status = models.CharField(
        max_length=20,
        choices=SlotStatus.choices,
        default=SlotStatus.PROPOSED,
        verbose_name="status",
        help_text="Status of this time slot proposal",
    )

    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="location",
        help_text="Interview location",
    )

    meeting_link = models.URLField(
        null=True,
        blank=True,
        verbose_name="meeting link",
        help_text="Online meeting link",
    )

    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name="notes",
        help_text="Additional notes about this slot",
    )

    def __str__(self) -> str:
        """String representation."""
        return f"Slot for {self.interview} - {self.start_time} ({self.get_status_display()})"

    class Meta:
        """Meta options."""

        verbose_name = "interview slot"
        verbose_name_plural = "interview slots"
        ordering = ["-created_at"]
