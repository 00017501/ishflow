"""Authentication random code utilities."""

import secrets
import string


# Character sets
DIGITS = string.digits  # '0123456789'
LETTERS = string.ascii_uppercase  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHANUMERIC = LETTERS + DIGITS  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
READABLE_CHARS = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"  # No 0/O/1/I/l


def generate_numeric_code(length: int = 6) -> str:
    """Generate a secure numeric verification code.

    Args:
        length (int): Length of the verification code. Must be a positive integer. Default is 6.

    Returns:
        str: A string containing only digits (e.g., '493820').

    Example:
        >>> generate_numeric_code()
        '582749'
    """
    return _generate_code(DIGITS, length)


def generate_alpha_code(length: int = 6) -> str:
    """Generate a secure verification code using only uppercase letters.

    Args:
        length (int): Length of the verification code. Must be a positive integer. Default is 6.

    Returns:
        str: A string containing only uppercase letters (e.g., 'AZMQFB').

    Example:
        >>> generate_alpha_code()
        'VQKJTZ'
    """
    return _generate_code(LETTERS, length)


def generate_alphanumeric_code(length: int = 8) -> str:
    """Generate a secure alphanumeric verification code using uppercase letters and digits.

    Args:
        length (int): Length of the verification code. Must be a positive integer. Default is 8.

    Returns:
        str: A string like 'X7F2Z9AB'.

    Example:
        >>> generate_alphanumeric_code()
        'F2B7X8QR'
    """
    return _generate_code(ALPHANUMERIC, length)


def generate_readable_code(length: int = 6) -> str:
    """Generate a code avoiding visually ambiguous characters (e.g., '0', 'O', '1', 'I', 'l').

    Args:
        length (int): Length of the verification code. Must be a positive integer. Default is 6.

    Returns:
        str: A readable code like '7ZHK4M'.

    Example:
        >>> generate_readable_code()
        '3G9KZH'
    """
    return _generate_code(READABLE_CHARS, length)


def _generate_code(charset: str, length: int) -> str:
    """Internal helper to generate a random code from a given character set.

    Args:
        charset (str): The character set to sample from.
        length (int): Desired code length. Must be positive.

    Returns:
        str: A secure random string of given length from the charset.

    Raises:
        ValueError: If length is not a positive integer.

    Example:
        >>> _generate_code("ABC123", 4)
        'C1BE'
    """
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Code length must be a positive integer")
    return "".join(secrets.choice(charset) for _ in range(length))
