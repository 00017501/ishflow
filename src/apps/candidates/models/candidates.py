"""ORM model for candidate profiles."""

from django.core.validators import FileExtensionValidator
from django.db import models

from src.apps.shared.models import fields as custom_fields
from src.apps.shared.models.core import BaseORM
from src.apps.shared.utils.validators import FileSizeValidator


class SalaryCurrencyOptions(models.TextChoices):
    """Currency options for salary fields."""

    USD = "USD", "US Dollar"
    EUR = "EUR", "Euro"
    UZS = "UZS", "Uzbekistani Sum"
    RUB = "RUB", "Russian Ruble"


class CandidateORM(BaseORM):
    """Extended profile for users with type='candidate'.

    Automatically created via signals when a user becomes a candidate.
    """

    user = models.OneToOneField(
        to="accounts.UserORM",
        on_delete=models.CASCADE,
        related_name="candidate_profile",
        primary_key=True,
        verbose_name="user",
    )

    # -------------------- CORE PROFILE -------------------- #
    resume = models.FileField(
        upload_to="resumes/%Y/%m/%d/",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"]),
            FileSizeValidator(max_size_mb=5),  # 5MB limit
        ],
        blank=True,
        null=True,
        help_text="Candidate's resume (PDF preferred, max 5MB)",
    )

    cover_letter = models.TextField(
        blank=True,
        null=True,
        help_text="Default cover letter or personal statement",
    )

    bio = models.TextField(
        blank=True,
        null=True,
        help_text="Short professional bio (for public profile)",
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="City, State/Province, Country (e.g. Berlin, Germany)",
    )

    # -------------------- PROFESSIONAL INFO -------------------- #
    skills = custom_fields.CommaSeparatedCharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Comma-separated list of skills (e.g. Python, Django, React)",
    )

    years_of_experience = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Total years of professional experience",
    )

    current_title = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Current or most recent job title",
    )

    linkedin_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="LinkedIn URL",
        help_text="LinkedIn profile URL",
    )

    github_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="GitHub URL",
        help_text="GitHub profile URL",
    )

    portfolio_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Portfolio URL",
        help_text="Personal portfolio URL",
    )

    # -------------------- PREFERENCES -------------------- #
    is_open_to_work = models.BooleanField(
        default=True, help_text="Indicates if the candidate is open to new job opportunities"
    )
    is_searching_actively = models.BooleanField(
        default=False, help_text="Indicates if the candidate is actively searching for a job"
    )

    desired_salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum desired salary",
    )
    desired_salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum desired salary",
    )
    salary_currency = models.CharField(
        max_length=3,
        choices=SalaryCurrencyOptions.choices,
        default=SalaryCurrencyOptions.USD,
        help_text="Currency for desired salary",
    )

    # -------------------- AVAILABILITY -------------------- #
    available_from = models.DateField(
        null=True,
        blank=True,
        help_text="When the candidate can start working",
    )

    class Meta:
        """Meta options for CandidateORM model."""

        verbose_name = "candidate profile"
        verbose_name_plural = "candidate profiles"

    def __str__(self) -> str:
        """String representation of the candidate profile."""
        return f"{self.user.full_name} (Candidate)"

    @property
    def has_completed_profile(self) -> bool:
        """Used for profile completion percentage in UI."""
        required = [self.resume, self.skills]
        return all(bool(field) for field in required)
