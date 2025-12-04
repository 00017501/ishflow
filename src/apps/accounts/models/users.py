"""User ORM definitions for the accounts app."""

from typing import TYPE_CHECKING, ClassVar

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from src.apps.accounts.models._manager import UserManager
from src.apps.companies.models.companies import CompanyORM
from src.apps.shared.models import fields as custom_fields
from src.apps.shared.models.core import BaseORM


if TYPE_CHECKING:
    from src.apps.companies.models.companies import CompanyORM


class UserTypeOptions(models.TextChoices):
    """User type options."""

    CANDIDATE = "candidate", "Candidate"
    EMPLOYER = "employer", "Employer"


class InvitationStatusOptions(models.TextChoices):
    """Status options for contacts."""

    ACCEPTED = "accepted", "Accepted"
    INVITED = "invited", "Invited"


class UserORM(BaseORM, AbstractBaseUser, PermissionsMixin):
    """Custom user model that uses email as the primary identifier instead of username."""

    # -------------------- AUTHENTICATION -------------------- #
    email = models.EmailField(
        unique=True,
        db_index=True,
        verbose_name="email address",
        help_text="User's email address used for authentication",
        error_messages={
            "unique": "A user with this email already exists.",
        },
    )

    # -------------------- PERSONAL INFO -------------------- #
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="first name",
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="last name",
    )

    phone_number = custom_fields.PhoneNumberField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="phone number",
        help_text="User's contact phone number",
    )

    # -------------------- RELATIONS -------------------- #
    company: CompanyORM = models.ForeignKey(
        to="companies.CompanyORM",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="employees",
        verbose_name="company",
        help_text="The company this user is employed at",
    )  # type: ignore

    # -------------------- PERMISSIONS -------------------- #
    type = models.CharField(
        max_length=20,
        choices=UserTypeOptions.choices,
        default=UserTypeOptions.CANDIDATE,
        verbose_name="type",
        help_text="The user's type within the company",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="staff status",
        help_text="Designates whether the user can log into this admin site.",
    )

    # -------------------- STATUSES -------------------- #
    invitation_status = models.CharField(
        max_length=20,
        choices=InvitationStatusOptions.choices,
        default=InvitationStatusOptions.INVITED,
        verbose_name="invitation status",
        help_text="The invitation status of the contact",
    )

    has_confirmed_email = models.BooleanField(
        default=False,
        verbose_name="has confirmed email",
        help_text="Indicates whether the user has confirmed their email address",
    )

    # -------------------- EXTRA CONFIGS -------------------- #
    objects: ClassVar[UserManager] = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    class Meta:
        """Meta options for User model."""

        verbose_name = "user"
        verbose_name_plural = "users"
        ordering: ClassVar[list[str]] = ["-created_at"]
        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["email", "is_active"]),
        ]
        permissions: ClassVar[list[tuple[str, str]]] = [
            ("view_employees", "Can view employee list"),
            ("invite_employees", "Can invite new employees"),
            ("manage_employees", "Can manage employees"),
        ]

    def __str__(self) -> str:
        """String representation of the user."""
        return f"{self.first_name} {self.last_name}".strip() or self.email + " " + f"({self.get_type_display()})"  # type: ignore[attr-defined]

    def __repr__(self) -> str:
        """Developer-friendly representation of the user."""
        return f"<User {self.email} (ID: {self.pk})>"

    @property
    def is_owner(self) -> bool:
        """Checks if the user is the owner."""
        return self.company.owner == self  # type: ignore

    @property
    def is_employee(self) -> bool:
        """Checks if the user is an employee."""
        return self.type == UserTypeOptions.EMPLOYER

    @property
    def is_candidate(self) -> bool:
        """Checks if the user is a candidate."""
        return self.type == UserTypeOptions.CANDIDATE

    @property
    def full_name(self) -> str:
        """Return the user's full name.

        Returns:
            str: Full name or email if names are not set
        """
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email

    @property
    def short_name(self) -> str:
        """Return the user's short name.

        Returns:
            str: First name or email if first name is not set
        """
        return self.first_name or self.email

    @property
    def has_accepted_invitation(self) -> bool:
        """Check if the invitation has been accepted.

        Returns:
            bool: True if invitation is accepted
        """
        return self.invitation_status == InvitationStatusOptions.ACCEPTED
