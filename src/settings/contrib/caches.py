"""Django cache settings."""

from src.settings.environment import env


# I decided to use Redis as the caching backend for better performance and scalability.
# Link: https://github.com/jazzband/django-redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("ISHFLOW_REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Ensure Axes uses the same cache as the default cache
AXES_CACHE = "default"
