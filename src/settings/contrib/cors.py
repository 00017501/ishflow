"""CORS Settings.

It configures Cross-Origin Resource Sharing (CORS) policies for the application.
"""

import logging

from src.settings.environment import env


logger = logging.getLogger(__name__)

if env.str("ISHFLOW_ENVIRONMENT") != "local":
    CORS_ALLOWED_ORIGINS = env.list("ISHFLOW_CORS_ALLOWED_ORIGINS", default=[])  # type: ignore

    CORS_ALLOWED_ORIGIN_REGEXES = env.list(
        "ISHFLOW_CORS_ALLOWED_ORIGIN_REGEXES",
        default=[r"^https:\/\/([a-z0-9-]+\.)*ishflow\.uz$"],  # type: ignore
    )

    CORS_ORIGIN_ALLOW_ALL = env.bool("ISHFLOW_CORS_ALLOW_ALL", default=False)  # type: ignore

    logger.info(f"CORS_ALLOWED_ORIGINS set to: {CORS_ALLOWED_ORIGINS}")
    logger.info(f"CORS_ALLOWED_ORIGIN_REGEXES set to: {CORS_ALLOWED_ORIGIN_REGEXES}")
    logger.info(f"CORS_ORIGIN_ALLOW_ALL set to: {CORS_ORIGIN_ALLOW_ALL}")
