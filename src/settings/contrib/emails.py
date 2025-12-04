"""Settings for emails provider."""

from src.settings.environment import env


EMAIL_BACKEND = env.str(
    "ISHFLOW_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",  # type: ignore
)
if EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":  # pragma: no cover
    EMAIL_HOST = env.str("ISHFLOW_EMAIL_HOST")
    EMAIL_PORT = env.str("ISHFLOW_EMAIL_PORT")
    EMAIL_HOST_USER = env.str("ISHFLOW_EMAIL_HOST_USER", default=None)  # type: ignore
    EMAIL_HOST_PASSWORD = env.str("ISHFLOW_EMAIL_HOST_PASSWORD", default=None)  # type: ignore
    EMAIL_USE_TLS = env.bool("ISHFLOW_EMAIL_USE_TLS", default=True)  # type: ignore

DEFAULT_FROM_EMAIL = env.str("ISHFLOW_DEFAULT_FROM_EMAIL", default="noreply@ishflow.uz")  # type: ignore
