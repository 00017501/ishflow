"""Login service implementation."""

from rest_framework_simplejwt.tokens import RefreshToken

from src.apps.accounts.models.users import UserORM


class LoginService:
    """Service for handling user login operations."""

    @classmethod
    def login(cls, user: UserORM) -> dict:
        """Authenticates the user and returns a dictionary with authentication tokens and user details."""
        refresh_token = RefreshToken.for_user(user)

        return cls._build_response(user, str(refresh_token.access_token), str(refresh_token))

    @staticmethod
    def _build_response(user: UserORM, access_token: str, refresh_token: str) -> dict:
        """Constructs the response data dictionary for a successful login."""
        return {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
            "user": user,
        }
