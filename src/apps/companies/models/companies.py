"""Companies models."""

from typing import ClassVar

from django.db import models

from src.apps.shared.models.core import BaseORM
from src.apps.shared.utils.validators import FileSizeValidator


class CompanyORM(BaseORM):
    """ORM model for Company."""

    # -------------------- RELATIONS -------------------- #
    owner = models.OneToOneField(
        to="accounts.UserORM",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="owned_company",
        verbose_name="owner",
        help_text="The user who owns the company",
    )

    # -------------------- DETAILS -------------------- #
    name = models.CharField(max_length=255, db_index=True, help_text="Name of the company")

    description = models.TextField(blank=True, null=True, help_text="Description of the company")

    website = models.URLField(blank=True, null=True, help_text="Website URL of the company")

    logo = models.ImageField(
        upload_to="companies/logos/%Y/%m/%d/",
        validators=[
            FileSizeValidator(max_size_mb=5),  # 5MB limit
        ],
        blank=True,
        null=True,
        help_text="Logo image for the company",
    )

    class Meta:
        """Meta options for Company model."""

        verbose_name = "company"
        verbose_name_plural = "companies"
        ordering: ClassVar[list[str]] = ["-created_at"]

    def __str__(self) -> str:
        """String representation of the company."""
        return self.name
