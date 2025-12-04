"""Logging configuration."""

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # Keep third-party loggers (like DRF, gunicorn)
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",  # ← This sets default to INFO
    },
    "loggers": {
        # Optional: Silence noisy loggers
        "axes": {
            "handlers": ["console"],
            "level": "WARNING",  # Only show real issues
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",  # Only show real errors
            "propagate": False,
        },
        "gunicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "drf_spectacular": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        # Main app
        "src": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
