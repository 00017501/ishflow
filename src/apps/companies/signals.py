"""Signal handlers for the accounts app."""

from typing import Any

from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.apps.accounts.models.users import UserORM
from src.apps.companies.models.companies import CompanyORM


@receiver(post_save, sender=CompanyORM)
def assign_owner_to_group(
    sender: type[CompanyORM], instance: CompanyORM, created: bool, **kwargs: Any  # noqa: ANN401, ARG001
) -> None:
    """Assign company owner to Company Owners group when a new company is created.

    Args:
        sender: The model class (CompanyORM)
        instance: The actual company instance being saved
        created: Boolean indicating if this is a new record
        **kwargs: Additional keyword arguments
    """
    if not created:
        return

    group_name = "Company Owners"

    # Get or create the group
    group, _ = Group.objects.get_or_create(name=group_name)

    # Add user to the group
    owner: UserORM = instance.owner
    owner.groups.add(group)
