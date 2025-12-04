from django.apps import AppConfig


class CompaniesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.companies"

    def ready(self) -> None:
        """Import signal handlers when the app is ready."""
        import src.apps.companies.signals  # noqa: F401
