"""Login serializer."""

from typing import ClassVar

from django.contrib.auth import authenticate as django_authenticate
from django.http import HttpRequest
from django.utils.translation import gettext
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.apps.accounts.models.users import UserORM


# Inspired from Django-Stars Backend Template: https://github.com/django-stars/backend-skeleton/tree/main
class LoginWriteSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.EmailField(write_only=True, max_length=254)
    password = serializers.CharField(max_length=128, style={"input_type": "password"}, write_only=True)

    @staticmethod
    def _authenticate(request: HttpRequest, email: str, password: str) -> UserORM | None:
        """Authenticate user with given email and password."""
        return django_authenticate(request=request, email=email, password=password)  # pragma: no cover # type: ignore

    def validate(self, attrs: dict) -> dict:
        """Validate the provided email and password."""
        request: HttpRequest = self.context.get("request")  # type: ignore

        user = self._authenticate(request, attrs["email"], attrs["password"])

        if user:
            return {"user": user}

        raise ValidationError(gettext("Incorrect email or password."))

    def create(self, validated_data: dict) -> UserORM:  # noqa: ARG002
        """Do not use create directly."""
        raise AssertionError("Do not use create directly")

    def update(self, instance: UserORM, validated_data: dict) -> UserORM:  # noqa: ARG002
        """Do not use update directly."""
        raise AssertionError("Do not use update directly")


class _UserInLoginSerializer(serializers.ModelSerializer):
    """Serializer for user details in login response."""

    class Meta:
        """Meta class for UserInLoginSerializer."""

        model = UserORM
        fields: ClassVar[list] = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "type",
            "invitation_status",
            "has_confirmed_email",
        ]


class LoginReadSerializer(serializers.Serializer):
    """Serializer for user login response."""

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    user = _UserInLoginSerializer(read_only=True)
