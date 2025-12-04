"""Configuration for Django REST Framework settings."""

from typing import Any, Final

from django.conf import settings


# Configuration is inspired from:
# Youtube Tutorial: https://www.youtube.com/watch?v=JXB1L-4005I
# GitHub Repo: https://github.com/Afaneor/drf-tutorial

# ===============================
# RENDERERS (how data is returned)
# ===============================
DEFAULT_RENDERER_CLASSES: list[str] = [
    "rest_framework.renderers.JSONRenderer",  # JSON format (primary)
    # DRF web interface (disable in production)
    # 'rest_framework.renderers.TemplateHTMLRenderer',  # HTML templates
    # 'rest_framework.renderers.StaticHTMLRenderer',   # Static HTML
    # 'rest_framework.renderers.XMLRenderer',          # XML format
]

if settings.ENVIRONMENT == "local":
    DEFAULT_RENDERER_CLASSES += [
        "rest_framework.renderers.BrowsableAPIRenderer",
    ]

# ===============================
# PARSERS (how data is received)
# ===============================
DEFAULT_PARSER_CLASSES: Final[list[str]] = [
    "rest_framework.parsers.JSONParser",  # JSON data (primary)
    "rest_framework.parsers.FormParser",  # HTML forms
    "rest_framework.parsers.MultiPartParser",  # Files + forms
    # 'rest_framework.parsers.FileUploadParser',  # Files only
    # 'rest_framework.parsers.XMLParser',         # XML data
]

# ===============================
# AUTHENTICATION (who is making the request)
# ===============================
DEFAULT_AUTHENTICATION_CLASSES: Final[list[str]] = [
    "rest_framework_simplejwt.authentication.JWTAuthentication",  # JWT tokens
    #  'rest_framework.authentication.SessionAuthentication',  # Django sessions (for web)  # noqa: ERA001
    #  'rest_framework.authentication.BasicAuthentication',  # HTTP Basic Auth
]
# ===============================
# PERMISSIONS (what actions are allowed)
# ===============================
DEFAULT_PERMISSION_CLASSES: Final[list[str]] = [
    "rest_framework.permissions.IsAuthenticated",  # Only authenticated users
    # 'rest_framework.permissions.AllowAny',               # Anyone
    # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',  # Read: all, Write: authenticated # noqa
    # 'rest_framework.permissions.IsAdminUser',           # Only admins
]

# ===============================
# THROTTLING (rate limiting)
# ===============================
DEFAULT_THROTTLE_CLASSES: Final[list[str]] = [
    "rest_framework.throttling.AnonRateThrottle",  # For anonymous users
    "rest_framework.throttling.UserRateThrottle",  # For authenticated users
    # 'rest_framework.throttling.ScopedRateThrottle',  # By scope
]

DEFAULT_THROTTLE_RATES: Final[dict[str, str]] = {
    "anon": "60/min",  # Anonymous: 60 requests per minute
    "user": "1000/min",  # Authenticated: 1000 requests per minute
}

# ===============================
# PAGINATION (splitting results into pages)
# ===============================
DEFAULT_PAGINATION_CLASS: Final[str] = "rest_framework.pagination.LimitOffsetPagination"
PAGE_SIZE: Final[int] = 20  # Default number of items per page

# Alternative pagination classes:
# 'rest_framework.pagination.PageNumberPagination'  # ?page=2  # noqa: ERA001
# 'rest_framework.pagination.CursorPagination'       # For large datasets

# ===============================
# FILTERING & SEARCH
# ===============================
DEFAULT_FILTER_BACKENDS: Final[list[str]] = [
    "django_filters.rest_framework.DjangoFilterBackend",  # django-filter
    # "rest_framework.filters.SearchFilter",  # Search by fields
    # "rest_framework.filters.OrderingFilter",  # Sorting
]

SEARCH_PARAM: Final[str] = "search"  # ?search=query
ORDERING_PARAM: Final[str] = "ordering"  # ?ordering=field_name

# ===============================
# API VERSIONING
# ===============================
DEFAULT_VERSIONING_CLASS: Final[str] = "rest_framework.versioning.URLPathVersioning"
DEFAULT_VERSION: Final[str] = "v1"
ALLOWED_VERSIONS: Final[list[str]] = ["v1", "v2"]
VERSION_PARAM: Final[str] = "version"

# ===============================
# EXCEPTION HANDLING
# ===============================
EXCEPTION_HANDLER: Final[str] = "src.apps.shared.exceptions.handler.custom_exception_handler"

# ===============================
# SCHEMA & DOCUMENTATION
# ===============================
DEFAULT_SCHEMA_CLASS: Final[str] = "drf_spectacular.openapi.AutoSchema"  # For drf-spectacular

# ===============================
# METADATA (for OPTIONS requests)
# ===============================
DEFAULT_METADATA_CLASS: Final[str] = "rest_framework.metadata.SimpleMetadata"

# ===============================
# CONTENT NEGOTIATION
# ===============================
DEFAULT_CONTENT_NEGOTIATION_CLASS: Final[str] = "rest_framework.negotiation.DefaultContentNegotiation"

# ===============================
# DATE/TIME FORMATS
# ===============================
DATETIME_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
DATETIME_INPUT_FORMATS: Final[list[str]] = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%dT%H:%M:%S.%fZ",
    "iso-8601",
]

DATE_FORMAT: Final[str] = "%Y-%m-%d"
DATE_INPUT_FORMATS: Final[list[str]] = [
    "%Y-%m-%d",
    "iso-8601",
]

TIME_FORMAT: Final[str] = "%H:%M:%S"
TIME_INPUT_FORMATS: Final[list[str]] = [
    "%H:%M:%S",
    "%H:%M:%S.%f",
    "%H:%M",
]

# ===============================
# JSON & UNICODE SETTINGS
# ===============================
UNICODE_JSON: Final[bool] = True
COMPACT_JSON: Final[bool] = False  # Set to True in production for smaller payloads
STRICT_JSON: Final[bool] = True
COERCE_DECIMAL_TO_STRING: Final[bool] = True  # Avoids floating-point precision issues

# ===============================
# TESTING SETTINGS
# ===============================
TEST_REQUEST_DEFAULT_FORMAT: Final[str] = "json"
TEST_REQUEST_RENDERER_CLASSES: Final[list[str]] = [
    "rest_framework.renderers.MultiPartRenderer",
    "rest_framework.renderers.JSONRenderer",
]

# ===============================
# URL FORMAT OVERRIDE
# ===============================
URL_FORMAT_OVERRIDE: Final[str] = "format"  # ?format=json
FORMAT_SUFFIX_KWARG: Final[str] = "format"  # URL suffix like .json

# ===============================
# BROWSABLE API SETTINGS
# ===============================
HTML_SELECT_CUTOFF: Final[int] = 1000
HTML_SELECT_CUTOFF_TEXT: Final[str] = "More than {count} items..."

# ===============================
# PERFORMANCE
# ===============================
UPLOADED_FILES_USE_URL: Final[bool] = True
URL_FIELD_NAME: Final[str] = "url"  # Field name in HyperlinkedModelSerializer

# ===============================
# SECURITY
# ===============================
NUM_PROXIES: Final[int | None] = None  # Number of proxy servers (for real IP detection)


# ===============================
# FINAL REST_FRAMEWORK CONFIGURATION
# ===============================
REST_FRAMEWORK: Final[dict[str, Any]] = {
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "DEFAULT_PARSER_CLASSES": DEFAULT_PARSER_CLASSES,
    "DEFAULT_AUTHENTICATION_CLASSES": DEFAULT_AUTHENTICATION_CLASSES,
    "DEFAULT_PERMISSION_CLASSES": DEFAULT_PERMISSION_CLASSES,
    "DEFAULT_THROTTLE_CLASSES": DEFAULT_THROTTLE_CLASSES,
    "DEFAULT_THROTTLE_RATES": DEFAULT_THROTTLE_RATES,
    "DEFAULT_PAGINATION_CLASS": DEFAULT_PAGINATION_CLASS,
    "PAGE_SIZE": PAGE_SIZE,
    "DEFAULT_FILTER_BACKENDS": DEFAULT_FILTER_BACKENDS,
    "SEARCH_PARAM": SEARCH_PARAM,
    "ORDERING_PARAM": ORDERING_PARAM,
    "DEFAULT_VERSIONING_CLASS": DEFAULT_VERSIONING_CLASS,
    "DEFAULT_VERSION": DEFAULT_VERSION,
    "ALLOWED_VERSIONS": ALLOWED_VERSIONS,
    "VERSION_PARAM": VERSION_PARAM,
    "EXCEPTION_HANDLER": EXCEPTION_HANDLER,
    "DEFAULT_SCHEMA_CLASS": DEFAULT_SCHEMA_CLASS,
    "DEFAULT_METADATA_CLASS": DEFAULT_METADATA_CLASS,
    "DEFAULT_CONTENT_NEGOTIATION_CLASS": DEFAULT_CONTENT_NEGOTIATION_CLASS,
    "DATETIME_FORMAT": DATETIME_FORMAT,
    "DATETIME_INPUT_FORMATS": DATETIME_INPUT_FORMATS,
    "DATE_FORMAT": DATE_FORMAT,
    "DATE_INPUT_FORMATS": DATE_INPUT_FORMATS,
    "TIME_FORMAT": TIME_FORMAT,
    "TIME_INPUT_FORMATS": TIME_INPUT_FORMATS,
    "UNICODE_JSON": UNICODE_JSON,
    "COMPACT_JSON": COMPACT_JSON,
    "STRICT_JSON": STRICT_JSON,
    "COERCE_DECIMAL_TO_STRING": COERCE_DECIMAL_TO_STRING,
    "TEST_REQUEST_DEFAULT_FORMAT": TEST_REQUEST_DEFAULT_FORMAT,
    "TEST_REQUEST_RENDERER_CLASSES": TEST_REQUEST_RENDERER_CLASSES,
    "URL_FORMAT_OVERRIDE": URL_FORMAT_OVERRIDE,
    "FORMAT_SUFFIX_KWARG": FORMAT_SUFFIX_KWARG,
    "HTML_SELECT_CUTOFF": HTML_SELECT_CUTOFF,
    "HTML_SELECT_CUTOFF_TEXT": HTML_SELECT_CUTOFF_TEXT,
    "UPLOADED_FILES_USE_URL": UPLOADED_FILES_USE_URL,
    "URL_FIELD_NAME": URL_FIELD_NAME,
    "NUM_PROXIES": NUM_PROXIES,
}
