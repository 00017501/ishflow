"""Environment settings and helpers."""

from pathlib import Path
from typing import Any, Literal

import environ

from django.core.exceptions import ImproperlyConfigured


def validate_environment_value(value: Any) -> Literal["local", "prod"]:  # noqa: ANN401
    """Convert environment variable to Enum value."""
    for x in ["local", "prod"]:
        if x == value:
            return value

    raise ImproperlyConfigured(f"Env value {value!r} is not one of 'local', 'prod'")


env = environ.Env(
    ISHFLOW_DEBUG=(bool, False),
    ISHFLOW_ENVIRONMENT=(validate_environment_value, "local"),
)

current_path = environ.Path(__file__) - 1
site_root = current_path - 2
env_file = site_root(".env")

if Path(env_file).exists():  # pragma: no cover
    environ.Env.read_env(env_file=env_file)
