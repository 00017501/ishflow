from django.apps import AppConfig


class CandidatesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.candidates"

    def ready(self):
        import src.apps.candidates.signals
