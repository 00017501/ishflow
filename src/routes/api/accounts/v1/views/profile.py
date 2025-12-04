"""User profile views."""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.shared.views.generics import GenericAPIView
from src.routes.api.accounts.v1.permissions import BaseVerifiedUserPermission
from src.routes.api.accounts.v1.serializers.profile import ReadUserProfileSerializer, UpdateUserProfileSerializer


class RetrieveProfileView(GenericAPIView):
    """View for retrieving user profile."""

    serializer_class = ReadUserProfileSerializer

    permission_classes = [BaseVerifiedUserPermission]

    @extend_schema(
        summary="Retrieve User Profile",
        description="Retrieve the profile information of the authenticated user.",
        tags=["Accounts"],
    )
    def get(self, request: Request) -> Response:
        """Handle requests to retrieve user profile.

        Returns:
            Response: User profile data
        """
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileView(GenericAPIView):
    """View for updating user profile."""

    serializer_class = UpdateUserProfileSerializer

    write_serializer_class = UpdateUserProfileSerializer
    read_serializer_class = ReadUserProfileSerializer

    permission_classes = [BaseVerifiedUserPermission]

    @extend_schema(
        summary="Update User Profile",
        description="Update the profile information of the authenticated user.",
        tags=["Accounts"],
        responses={200: ReadUserProfileSerializer},
    )
    def put(self, request: Request) -> Response:
        """Handle requests to update user profile.

        Returns:
            Response: Updated user profile data
        """
        user = request.user

        write_serializer = self.get_write_serializer(user, data=request.data, partial=True)
        write_serializer.is_valid(raise_exception=True)
        write_serializer.save()

        read_serializer = self.get_read_serializer(user)

        return Response(read_serializer.data, status=status.HTTP_200_OK)
