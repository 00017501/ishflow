"""Custom permissions for job management."""

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from src.apps.accounts.models.users import UserORM, UserTypeOptions
from src.apps.jobs.models.jobs import JobPostORM


class IsEmployerWithCompany(BasePermission):
    """Allows access only to authenticated employers with a company.

    This permission ensures:
    1. User is authenticated
    2. User is an employer
    3. User is associated with a company
    """

    def has_permission(self, request: Request, view: APIView) -> bool:  # noqa: ARG002
        """Check if user is an employer with a company.

        Args:
            request: The HTTP request being made
            view: The view being accessed

        Returns:
            bool: True if user is employer with company, False otherwise
        """
        user: UserORM = request.user  # type: ignore

        if not user.is_authenticated:
            return False

        if user.type != UserTypeOptions.EMPLOYER:
            raise PermissionDenied("Only employers can manage job posts.")

        if not hasattr(user, "company") or not user.company:
            raise PermissionDenied("You must be associated with a company to manage job posts.")

        return True


class CanManageJob(BasePermission):
    """Permission to check if user can manage (edit/delete) a specific job.

    This permission ensures:
    1. User is authenticated employer with company (via IsEmployerWithCompany)
    2. Job belongs to the user's company
    """

    def has_object_permission(self, request: Request, view: APIView, obj: JobPostORM) -> bool:  # noqa: ARG002
        """Check if user can manage this specific job.

        Args:
            request: The HTTP request being made
            view: The view being accessed
            obj: The job object being accessed

        Returns:
            bool: True if user can manage the job, False otherwise
        """
        user: UserORM = request.user  # type: ignore

        if not user.is_authenticated:
            return False

        # Check if job belongs to user's company
        if hasattr(obj, "company") and hasattr(user, "company"):
            return obj.company == user.company

        return False
