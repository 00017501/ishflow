"""Signals for candidate profile management."""

from typing import Any

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from src.apps.accounts.models import UserORM
from src.apps.accounts.models.users import UserTypeOptions
from src.apps.candidates.models import CandidateORM


@receiver(pre_save, sender=UserORM)
def track_previous_type(sender: UserORM, instance: UserORM, **kwargs: Any) -> None:  # noqa
    """Track previous user type before saving."""
    if instance.pk:
        instance._previous_type = UserORM.objects.get(pk=instance.pk).type  # type: ignore
    else:
        instance._previous_type = None  # type: ignore


@receiver(post_save, sender=UserORM)
def create_candidate_profile(sender: UserORM, instance: UserORM, created: bool, **kwargs: Any) -> None:  # noqa
    """Create or delete candidate profile based on user type changes."""
    previous_type = getattr(instance, "_previous_type", None)

    # If user just became a candidate
    if instance.type == UserTypeOptions.CANDIDATE and (created or previous_type != UserTypeOptions.CANDIDATE):
        CandidateORM.objects.get_or_create(user=instance)

    # Delete profile if switched away from candidate
    elif previous_type == UserTypeOptions.CANDIDATE and instance.type != UserTypeOptions.CANDIDATE:
        CandidateORM.objects.filter(user=instance).delete()
