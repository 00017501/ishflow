"""Simple JWT settings."""

from datetime import timedelta

from src.settings.environment import env


SIMPLE_JWT = {
    # For production, we keep access token lifetime short (5 minutes)
    # and for non-production environments, set it longer (1 hour)
    "ACCESS_TOKEN_LIFETIME": (
        timedelta(minutes=5) if env.str("ISHFLOW_ENVIRONMENT") in ["prod"] else timedelta(hours=1)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env.str("ISHFLOW_SECRET_KEY"),
    "ISSUER": "ishflow_api",
}
