"""Password services."""

from src.apps.accounts.models.users import InvitationStatusOptions, UserORM


def accept_invitation(user: UserORM, extra_fields_to_update: list | None = None) -> UserORM:
    """Accept invitation for the user."""
    user.invitation_status = InvitationStatusOptions.ACCEPTED
    user.has_confirmed_email = True
    user.is_active = True
    user.save(update_fields=["invitation_status", "has_confirmed_email", "is_active", *(extra_fields_to_update or [])])

    return user


class SetPasswordAtInvitation:
    """Service to set password for invited users."""

    @staticmethod
    def set_password(user: UserORM, password: str) -> UserORM:
        """Set password and update invitation status."""
        # Set the user's password
        user.set_password(password)
        # Accept the invitation
        accept_invitation(user, extra_fields_to_update=["password"])
        return user


set_password_at_invitation = SetPasswordAtInvitation()
