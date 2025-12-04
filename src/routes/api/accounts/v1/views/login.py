"""Login and logout views."""

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

from src.apps.accounts.services.login import LoginService
from src.apps.shared.views.generics import CreateAPIView
from src.routes.api.accounts.v1.permissions import IsNotAuthenticated
from src.routes.api.accounts.v1.serializers.login import LoginReadSerializer, LoginWriteSerializer


class LoginView(CreateAPIView):
    """View for user login."""

    serializer_class = LoginWriteSerializer

    write_serializer_class = LoginWriteSerializer
    read_serializer_class = LoginReadSerializer

    login_service = LoginService

    permission_classes = [IsNotAuthenticated]

    @extend_schema(
        summary="Login",
        tags=["Accounts"],
        responses={200: LoginReadSerializer, 400: OpenApiResponse(description="Bad Request")},
    )
    def post(self, request: Request) -> Response:
        """Handle user login requests."""
        serializer = self.get_write_serializer(data=request.data, context={"request": request})

        # Validate the input data
        serializer.is_valid(raise_exception=True)

        # Get the authenticated user from validated data
        user = serializer.validated_data.get("user")

        # Get the response containing tokens and user details
        response = self.get_read_serializer(self.login_service.login(user))

        return Response(data=response.data)


class LogoutView(TokenBlacklistView):
    """View for user logout."""

    @extend_schema(
        summary="Logout",
        tags=["Accounts"],
        responses={
            200: OpenApiResponse(description="Successfully logged out"),
            400: OpenApiResponse(description="Bad Request"),
        },
    )
    def post(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle user logout requests."""
        return super().post(request, *args, **kwargs)


class RefreshView(TokenRefreshView):
    """View for refreshing JWT tokens."""

    @extend_schema(
        summary="Refresh Token",
        tags=["Accounts"],
        responses={
            400: OpenApiResponse(description="Bad Request"),
        },
    )
    def post(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle token refresh requests."""
        return super().post(request, *args, **kwargs)
