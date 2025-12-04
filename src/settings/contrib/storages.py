"""Django storages configuration for S3-compatible storage (MinIO/AWS S3)."""

from storages.backends.s3 import S3Storage

from src.settings.environment import env


# AWS S3 / MinIO Configuration
AWS_ACCESS_KEY_ID = env.str("ISHFLOW_AWS_ACCESS_KEY_ID", default="")  # type: ignore
AWS_SECRET_ACCESS_KEY = env.str("ISHFLOW_AWS_SECRET_ACCESS_KEY", default="")  # type: ignore
AWS_S3_ENDPOINT_URL = env.str("ISHFLOW_AWS_S3_ENDPOINT_URL", default=None)  # type: ignore
AWS_S3_USE_SSL = env.bool("ISHFLOW_AWS_S3_USE_SSL", default=True)  # type: ignore
AWS_S3_REGION_NAME = env.str("ISHFLOW_AWS_S3_REGION_NAME", default="us-east-1")  # type: ignore
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False

# Bucket names
AWS_STORAGE_BUCKET_NAME = env.str("ISHFLOW_AWS_STORAGE_BUCKET_NAME", default="media")  # type: ignore
AWS_STATIC_BUCKET_NAME = env.str("ISHFLOW_AWS_STATIC_BUCKET_NAME", default="static")  # type: ignore

# Custom domains for external access
AWS_S3_CUSTOM_DOMAIN = env.str("ISHFLOW_AWS_S3_CUSTOM_DOMAIN", default=None)  # type: ignore
AWS_STATIC_CUSTOM_DOMAIN = env.str("ISHFLOW_AWS_STATIC_CUSTOM_DOMAIN", default=None)  # type: ignore


# Media and Static URLs
_url_protocol = "https" if AWS_S3_USE_SSL else "http"


class MediaStorage(S3Storage):
    """Custom storage class for media files."""

    bucket_name = AWS_STORAGE_BUCKET_NAME
    file_overwrite = False
    custom_domain = AWS_S3_CUSTOM_DOMAIN
    url_protocol = _url_protocol + ":"
    object_parameters = {"CacheControl": "max-age=86400"}
    location = ""


class StaticStorage(S3Storage):
    """Custom storage class for static files."""

    bucket_name = AWS_STATIC_BUCKET_NAME
    file_overwrite = True
    custom_domain = AWS_STATIC_CUSTOM_DOMAIN
    url_protocol = _url_protocol + ":"
    object_parameters = {"CacheControl": "max-age=31536000"}
    location = ""


MEDIA_URL = (
    f"{_url_protocol}://{AWS_S3_CUSTOM_DOMAIN}/"
    if AWS_S3_CUSTOM_DOMAIN
    else f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/"
)

STATIC_URL = (
    f"{_url_protocol}://{AWS_STATIC_CUSTOM_DOMAIN}/"
    if AWS_STATIC_CUSTOM_DOMAIN
    else f"{AWS_S3_ENDPOINT_URL}/{AWS_STATIC_BUCKET_NAME}/"
)
