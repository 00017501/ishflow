"""Utility functions for humanizing various data types.

This module provides functions to convert numbers, dates, and other data types.
"""

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Literal

import humanize

from src.apps.shared.utils import datetime as dt


def humanize_number(value: int | float) -> str:
    """Converts a number into a human-readable format (e.g., 1,000 -> '1 thousand').

    Args:
        value (int or float): The number to humanize.

    Returns:
        str: Human-readable string.

    Example:
        >>> humanize_number(12345)
        '12 thousand'
    """
    return humanize.intword(value)


def humanize_bytes(num_bytes: int) -> str:
    """Converts a byte value into a human-readable file size.

    Args:
        num_bytes (int): Number of bytes.

    Returns:
        str: Human-readable file size.

    Example:
        >>> humanize_bytes(1048576)
        '1.0 MB'
    """
    return humanize.naturalsize(num_bytes, binary=True)


def humanize_time_delta(dt: datetime | timedelta, now: datetime | None = None) -> str:
    """Converts a datetime or timedelta into a human-readable relative time.

    Args:
        dt (datetime or timedelta): The datetime or timedelta to humanize.
        now (datetime, optional): Reference time. Defaults to current time.

    Returns:
        str: Human-readable relative time.

    Example:
        >>> from datetime import datetime, timedelta
        >>> humanize_time_delta(datetime.now() - timedelta(hours=2))
        '2 hours ago'
    """
    if isinstance(dt, timedelta):
        return humanize.naturaltime(dt)
    if now is None:
        now = datetime.now(UTC)
    return humanize.naturaltime(now - dt)


def humanize_ordinal(number: int) -> str:
    """Converts a number to its ordinal representation (e.g., 1 -> '1st').

    Args:
        number (int): The number to convert.

    Returns:
        str: Ordinal string.

    Example:
        >>> humanize_ordinal(3)
        '3rd'
    """
    return humanize.ordinal(number)


def humanize_list(items: list[str]) -> str:
    """Converts a list of items into a human-readable list.

    Args:
        items (list): List of strings.

    Returns:
        str: Human-readable list.

    Example:
        >>> humanize_list(['apples', 'bananas', 'cherries'])
        'apples, bananas, and cherries'
    """
    return humanize.natural_list(items)


def humanize_date(date_obj: datetime, format_type: Literal["default", "full", "short"] = "default") -> str:
    """Converts a date to a human-readable format.

    Args:
        date_obj (datetime): Date to humanize.
        format_type (str): Format type - 'default', 'full', or 'short'.

    Returns:
        str: Human-readable date.

    Example:
        >>> humanize_date(datetime(2024, 3, 15))
        'Mar 15 2024'
    """
    formats_mapping: dict[str, str] = {
        "full": date_obj.strftime("%A, %B %d, %Y"),
        "short": date_obj.strftime("%m/%d/%y"),
    }
    return formats_mapping.get(format_type, date_obj.strftime("%b %d %Y"))


def humanize_duration(seconds: int | float) -> str:
    """Converts seconds into a human-readable duration.

    Args:
        seconds (int or float): Duration in seconds.

    Returns:
        str: Human-readable duration.

    Example:
        >>> humanize_duration(3661)
        '1 hour, 1 minute and 1 second'
    """
    return humanize.naturaldelta(timedelta(seconds=seconds))


def humanize_frequency(count: int, period: Literal["day", "week", "month", "year"] = "day") -> str:
    """Converts a count and period into human-readable frequency.

    Args:
        count (int): Number of occurrences.
        period (str): Time period ('day', 'week', 'month', 'year').

    Returns:
        str: Human-readable frequency.

    Example:
        >>> humanize_frequency(5, 'day')
        '5 times per day'
    """
    frequency_mapping: dict[int, str] = {
        0: "never",
        1: "once",
        2: "twice",
    }

    return f"{frequency_mapping.get(count, f'{count} times')} per {period}"


def humanize_currency(
    amount: float | Decimal,
    currency: str = "USD",
    format_type: Literal["symbol", "code"] = "symbol",
) -> str:
    """Formats currency amounts in a human-readable way.

    Args:
        amount (float or Decimal): Amount to format.
        currency (str): Currency code.
        format_type (str): 'symbol' or 'code'.

    Returns:
        str: Formatted currency string.

    Example:
        >>> humanize_currency(1234.56)
        '$1,234.56'
    """
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "CAD": "C$",
        "AUD": "A$",
        "CNY": "¥",
    }

    if format_type == "symbol" and currency in symbols:
        return f"{symbols[currency]}{amount:,.2f}"
    return f"{amount:,.2f} {currency}"


def humanize_percentage(value: float, decimal_places: int = 1) -> str:
    """Formats a decimal value as a human-readable percentage.

    Args:
        value (float): Value between 0 and 1 (or percentage if > 1).
        decimal_places (int): Number of decimal places.

    Returns:
        str: Formatted percentage string.

    Example:
        >>> humanize_percentage(0.1234)
        '12.3%'
    """
    percentage = value * 100 if value <= 1 else value

    return f"{percentage:.{decimal_places}f}%"


def humanize_distance(meters: float, unit: Literal["auto", "metric", "imperial"] = "auto") -> str:
    """Converts meters to human-readable distance.

    Args:
        meters (float): Distance in meters.
        unit (str): Target unit ('auto', 'metric', 'imperial').

    Returns:
        str: Human-readable distance.

    Example:
        >>> humanize_distance(1500)
        '1.5 km'
    """
    if unit == "imperial":
        if meters < 304.8:  # noqa: PLR2004
            feet = meters * 3.28084
            return f"{feet:.0f} feet"

        miles = meters / 1609.34
        return f"{miles:.1f} miles"

    if meters < 1000:  # noqa: PLR2004
        return f"{meters:.0f} meters"
    km = meters / 1000
    return f"{km:.1f} km"


def humanize_age(birth_date: datetime, reference_date: datetime | None = None) -> str:
    """Calculates and formats age in a human-readable way.

    Args:
        birth_date (datetime): Birth date.
        reference_date (datetime, optional): Reference date. Defaults to now.

    Returns:
        str: Human-readable age.

    Example:
        >>> humanize_age(datetime(1990, 5, 15))
        '34 years old'
    """
    if reference_date is None:
        reference_date = dt.utc_now()

    age = reference_date.year - birth_date.year
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    if age == 0:
        months = reference_date.month - birth_date.month
        if reference_date.day < birth_date.day:
            months -= 1
        if months <= 0:
            days = (reference_date - birth_date).days
            return f"{days} days old"
        return f"{months} months old"

    if age == 1:
        return "1 year old"
    return f"{age} years old"


def humanize_score(
    score: int | float,
    max_score: int | float,
    format_type: Literal["fraction", "percentage", "grade"] = "fraction",
) -> str:
    """Formats scores in a human-readable way.

    Args:
        score (int or float): Achieved score.
        max_score (int or float): Maximum possible score.
        format_type (str): 'fraction', 'percentage', or 'grade'.

    Returns:
        str: Human-readable score.

    Example:
        >>> humanize_score(85, 100, 'percentage')
        '85%'
        >>> humanize_score(85, 100, 'grade')
        '85% (B)'
        >>> humanize_score(85, 100, 'fraction')
        '85/100'
    """
    if format_type == "percentage":
        percentage = (score / max_score) * 100
        return f"{percentage:.0f}%"
    elif format_type == "grade":  # noqa: RET505
        percentage = (score / max_score) * 100
        grade_map = [
            (90, "A"),
            (80, "B"),
            (70, "C"),
            (60, "D"),
            (0, "F"),
        ]
        for threshold, grade in grade_map:
            if percentage >= threshold:
                return f"{percentage:.0f}% ({grade})"
    return f"{score}/{max_score}"


def humanize_progress(current: int, total: int, show_percentage: bool = True) -> str:
    """Formats progress in a human-readable way.

    Args:
        current (int): Current progress.
        total (int): Total items.
        show_percentage (bool): Whether to show percentage.

    Returns:
        str: Human-readable progress.

    Example:
        >>> humanize_progress(75, 100)
        '75 of 100 (75%)'
    """
    if show_percentage:
        percentage = (current / total) * 100 if total > 0 else 0
        return f"{current:,} of {total:,} ({percentage:.0f}%)"
    return f"{current:,} of {total:,}"
