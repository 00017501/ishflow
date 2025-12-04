"""Applications models module."""

from django.db import models

from src.apps.shared.models.core import BaseORM


class ApplicationStatus(models.TextChoices):
    """Enumeration of possible application statuses."""

    APPLIED = "applied", "Applied"
    UNDER_REVIEW = "under_review", "Under Review"
    INTERVIEW_SCHEDULED = "interview_scheduled", "Interview Scheduled"
    OFFERED = "offered", "Offered"
    REJECTED = "rejected", "Rejected"


class ApplicationORM(BaseORM):
    """Model representing a job application."""

    # =================== RELATIONSHIPS =================== #

    # NOTE: The combination of applicant and post should be unique
    # because these two are a composite primary key.
    applicant = models.ForeignKey(
        to="candidates.CandidateORM",
        on_delete=models.CASCADE,
        related_name="applications",
        null=False,
        blank=False,
        verbose_name="applicant",
        help_text="The candidate who applied for the job",
    )

    post = models.ForeignKey(
        to="jobs.JobPostORM",
        on_delete=models.CASCADE,
        related_name="applications",
        null=False,
        blank=False,
        verbose_name="job post",
        help_text="The job post this application is for",
    )

    # =================== DETAILS =================== #

    cover_letter = models.TextField(
        verbose_name="cover letter",
        help_text="Cover letter provided by the applicant",
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.APPLIED,
        verbose_name="application status",
        help_text="Current status of the application",
    )

    def __str__(self) -> str:
        """String representation of the ApplicationORM."""
        return f"Application by {self.applicant} for {self.post.title}"

    class Meta:
        """Meta options for ApplicationORM model."""

        unique_together = ("applicant", "post")

        verbose_name = "job application"
        verbose_name_plural = "job applications"
        ordering: list[str] = ["-created_at"]
