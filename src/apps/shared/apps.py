"""App configuration for the common app."""

from django.apps import AppConfig


class SharedConfig(AppConfig):
    """App configuration for the shared app."""

    name = "src.apps.shared"
