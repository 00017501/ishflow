"""Utility functions for handling datetime objects."""

import datetime as dt

from django.conf import settings


def utc_now() -> dt.datetime:
    """Get the current UTC datetime.

    Returns:
        dt.datetime: The current UTC datetime.
    """
    return dt.datetime.now(dt.UTC)


def local_now() -> dt.datetime:
    """Get the current local datetime.

    The timezone is determined by the application's general settings.
    See `src/settings/django.py` for more details.

    Returns:
        dt.datetime: The current local datetime.
    """
    return dt.datetime.now(tz=settings.TIME_ZONE)


def convert_to_utc(dt_obj: dt.datetime) -> dt.datetime:
    """Convert a datetime object to UTC timezone.

    Args:
        dt_obj (dt.datetime): The datetime object to convert.

    Returns:
        dt.datetime: The datetime object in UTC timezone.
    """
    return dt_obj.astimezone(dt.UTC)


def convert_to_local(dt_obj: dt.datetime) -> dt.datetime:
    """Convert a datetime object to the local timezone.

    Args:
        dt_obj (dt.datetime): The datetime object to convert.

    Returns:
        dt.datetime: The datetime object in the local timezone.
    """
    return dt_obj.astimezone(tz=settings.TIME_ZONE)
