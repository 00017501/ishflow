"""User manager class for custom User model."""

from typing import TYPE_CHECKING

from django.contrib.auth.models import BaseUserManager


if TYPE_CHECKING:
    from src.apps.accounts.models.users import UserORM


class UserManager(BaseUserManager["UserORM"]):
    """Custom manager for User model with email as the unique identifier."""

    def create_user(self, email: str, password: str | None = None, **extra_fields: bool | str) -> "UserORM":
        """Create and save a regular user with the given email and password.

        Args:
            email: User's email address (required)
            password: User's password (optional)
            **extra_fields: Additional fields for the user model

        Returns:
            User: The created user instance

        Raises:
            ValueError: If email is not provided
        """
        if not email:
            raise ValueError("Users must provide an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: bool | str) -> "UserORM":
        """Create and save a superuser with the given email and password.

        Args:
            email: Superuser's email address (required)
            password: Superuser's password (required)
            **extra_fields: Additional fields for the user model

        Returns:
            User: The created superuser instance

        Raises:
            ValueError: If is_staff or is_superuser is not True
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("has_confirmed_email", True)
        extra_fields.setdefault("invitation_status", "accepted")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
