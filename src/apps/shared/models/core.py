"""Core django models for the application."""

from django.db import models

from src.apps.shared.utils import humanization as humanize_utils


class BaseORM(models.Model):
    """Abstract base model with common fields."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        """Meta class for BaseORM."""

        abstract = True

    def __str__(self) -> str:
        """String representation of the model."""
        return str(self.pk)

    def __repr__(self) -> str:
        """String representation of the model."""
        return f"<{self.__class__.__name__} {self.pk}>"

    @property
    def humanized_created_at(self) -> str:
        """Humanized representation of the created_at field.

        Example:
            >>> instance.humanized_created_at
            '5 minutes ago'
        """
        return humanize_utils.humanize_time_delta(self.created_at)

    @property
    def humanized_updated_at(self) -> str:
        """Humanized representation of the updated_at field.

        Example:
            >>> instance.humanized_updated_at
            '3 days ago'
        """
        return humanize_utils.humanize_time_delta(self.updated_at)


class CompanyIncludedBaseORM(BaseORM):
    """Abstract base model for entities included in a Company."""

    company = models.ForeignKey(
        to="companies.CompanyORM",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="company",
        help_text="The company this entity is associated with",
    )

    class Meta:
        """Meta class for CompanyIncludedBaseModel."""

        abstract = True
