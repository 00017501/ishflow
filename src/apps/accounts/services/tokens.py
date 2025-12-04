"""Token generator for email confirmation."""

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from src.apps.accounts.models.users import UserORM


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Token generator for account activation emails."""

    def _make_hash_value(self, user: UserORM, timestamp: int) -> str:
        """Generate hash value for the token."""
        return f"{user.pk}{timestamp}{user.has_confirmed_email}"


account_activation_token = AccountActivationTokenGenerator()


class GetUserFromToken:
    """Utility to get user from token."""

    def __init__(self, token_generator: PasswordResetTokenGenerator) -> None:
        self._token_generator = token_generator

    def get_user(self, uidb64: str, token: str) -> UserORM | None:
        """Retrieve user based on uidb64 and token."""
        try:
            # Decode user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserORM.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserORM.DoesNotExist):
            return None

        # Validate token
        if user is not None and self._token_generator.check_token(user, token):
            return user
        return None


get_user_from_token = GetUserFromToken(token_generator=AccountActivationTokenGenerator())
