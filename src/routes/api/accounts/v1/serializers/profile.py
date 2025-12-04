"""User profile serializers."""

from rest_framework import serializers

from src.apps.accounts.models.users import UserORM


class ReadUserProfileSerializer(serializers.ModelSerializer):
    """Serializer for reading user profile information."""

    type = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        """Meta class for ReadUserProfileSerializer."""

        model = UserORM
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "type",
            "invitation_status",
            "has_confirmed_email",
        ]


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile information."""

    class Meta:
        """Meta class for UpdateUserProfileSerializer."""

        model = UserORM
        fields = [
            "first_name",
            "last_name",
            "phone_number",
        ]
