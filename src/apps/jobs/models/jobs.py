"""Jobs models module."""

from django.db import models

from src.apps.shared.models.core import CompanyIncludedBaseORM


class EmploymentType(models.TextChoices):
    """Employment type choices."""

    FULL_TIME = "full_time", "Full Time"
    PART_TIME = "part_time", "Part Time"
    CONTRACT = "contract", "Contract"
    INTERN = "intern", "Intern"
    FREELANCE = "freelance", "Freelance"


class JobPostORM(CompanyIncludedBaseORM):
    """Model representing a job post."""

    # =================== RELATIONSHIPS =================== #
    company = models.ForeignKey(
        to="companies.CompanyORM",
        on_delete=models.CASCADE,
        related_name="posts",
        null=False,
        blank=False,
        verbose_name="company",
        help_text="The company this job post is associated with",
    )

    # =================== DETAILS =================== #

    title = models.CharField(
        max_length=255,
        verbose_name="job title",
        help_text="Title of the job position",
    )

    description = models.TextField(
        verbose_name="job description",
        help_text="Detailed description of the job",
    )

    location = models.CharField(
        max_length=255,
        verbose_name="job location",
        help_text="Location of the job",
    )

    type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME,
        verbose_name="employment type",
        help_text="Type of employment for the job",
    )

    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="minimum salary",
        help_text="Minimum salary for the job",
    )

    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="maximum salary",
        help_text="Maximum salary for the job",
    )

    class Meta:
        """Meta class for JobPostORM."""

        verbose_name = "Job Post"
        verbose_name_plural = "Job Posts"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """String representation of the JobPostORM."""
        return f"{self.title} at {self.company.name}"
