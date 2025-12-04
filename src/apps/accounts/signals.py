"""Signal handlers for the accounts app."""

from typing import Any

from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.apps.accounts.models.users import UserORM, UserTypeOptions


@receiver(post_save, sender=UserORM)
def assign_user_to_group(
    sender: type[UserORM], instance: UserORM, created: bool, **kwargs: Any  # noqa: ANN401, ARG001
) -> None:
    """Assign user to appropriate group based on their type when created.

    Args:
        sender: The model class (UserORM)
        instance: The actual user instance being saved
        created: Boolean indicating if this is a new record
        **kwargs: Additional keyword arguments
    """
    if not created:
        return

    # Map user types to group names
    group_mapping = {
        UserTypeOptions.CANDIDATE: "Candidates",
        UserTypeOptions.EMPLOYER: "Company Managers",
    }

    group_name = group_mapping[instance.type]

    # Get or create the group
    group, _ = Group.objects.get_or_create(name=group_name)

    # Add user to the group
    instance.groups.add(group)
