"""Custom permissions for user management."""

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from src.apps.accounts.models.users import UserORM, UserTypeOptions


class IsNotAuthenticated(BasePermission):
    """Allows access only to unauthenticated users.

    Use this permission for registration, login, and other public endpoints
    that should only be accessible to anonymous users.
    """

    def has_permission(self, request: Request, view: object) -> bool:  # noqa: ARG002
        """Check if the user is not authenticated.

        Args:
            request: The HTTP request being made
            view: The view being accessed

        Returns:
            bool: True if user is not authenticated, False otherwise
        """
        return not request.user.is_authenticated


class BaseVerifiedUserPermission(BasePermission):
    """Base permission requiring authenticated user with verified product.

    This base class ensures that:
    1. User is authenticated
    2. User is a UserORM instance

    All product-specific permissions should inherit from this class.
    """

    def has_permission(self, request: Request, view: object) -> bool:  # noqa: ARG002
        """Check if the user has a verified product.

        Args:
            request: The HTTP request being made
            view: The view being accessed

        Returns:
            bool: True if user has verified product, False otherwise
        """
        # User must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # User must be a UserORM instance
        if not isinstance(request.user, UserORM):
            return False

        user: UserORM = request.user

        # User must have confirmed email
        if not user.has_confirmed_email:
            raise PermissionDenied("Your account is inactive. Please confirm your email or contact support.")

        return True


class IsCompanyOwnerUser(BaseVerifiedUserPermission):
    """Allows access only to company owner users.

    This permission ensures the user is the owner of their company.
    Owners have full control over their company and all associated data.
    """

    def has_permission(self, request: Request, view: object) -> bool:
        """Check if the user is the company owner.

        Args:
            request: The HTTP request being made
            view: The view being accessed

        Returns:
            bool: True if user is company owner, False otherwise
        """
        # First, ensure the company is verified
        if not super().has_permission(request, view):
            return False

        user: UserORM = request.user  # type: ignore[assignment]
        if not user.is_owner:
            raise PermissionDenied("Only company owners can perform this action.")
        return True


class IsCompanyEmployeeUser(BaseVerifiedUserPermission):
    """Allows access only to manager users.

    This permission ensures the user has an manager role within their company.

    Note: Manager is second to owner in terms of permissions.
    """

    def has_permission(self, request: Request, view: object) -> bool:
        """Check if the user is a manager.

        Args:
            request: The HTTP request being made
            view: The view being accessed

        Returns:
            bool: True if user is admin, False otherwise
        """
        # First, ensure the product is verified
        if not super().has_permission(request, view):
            return False

        user: UserORM = request.user  # type: ignore[assignment]
        if user.type != UserTypeOptions.EMPLOYER:
            raise PermissionDenied("Only admins can perform this action.")
        return True
