"""Utilities for generating MD5 hashes from strings or dictionaries.

This module provides functions to create MD5 hashes from string inputs or
dictionaries. It uses the `hashlib` library to compute the MD5 hash and the `json` module
for serializing dictionaries to JSON strings.
"""

import hashlib
import json

from collections.abc import Callable
from typing import Any


def md5_sha_from_str(val: str) -> str:
    """Generate an MD5 hash from a string.

    Args:
        val (str): The string to hash.

    Returns:
        str: The MD5 hash of the string.
    """
    return hashlib.md5(val.encode("utf-8")).hexdigest()  # noqa: S324


def md5_sha_from_dict(
    obj: dict[Any, Any],
    ignore_nan: bool = False,
    default: Callable[[Any], Any] | None = None,
) -> str:
    """Generate an MD5 hash from a dictionary by serializing it to a JSON string.

    Args:
        obj (dict[Any, Any]): The dictionary to hash.
        ignore_nan (bool): If True, NaN values will be ignored in the JSON serialization.
        default (Optional[Callable[[Any], Any]]): A function to handle non-serializable objects.

    Returns:
        str: The MD5 hash of the serialized JSON string.
    """
    json_data = json.dumps(obj, sort_keys=True, ignore_nan=ignore_nan, default=default, allow_nan=True)

    return md5_sha_from_str(json_data)
