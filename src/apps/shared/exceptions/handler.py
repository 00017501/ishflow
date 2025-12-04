"""Custom exception handler for Blog API."""

import logging
import uuid

from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from django.http import Http404, HttpRequest
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    MethodNotAllowed,
    NotAuthenticated,
    NotFound,
    ParseError,
    PermissionDenied,
    Throttled,
    UnsupportedMediaType,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from src.apps.shared.exceptions.base import IshflowAPIException
from src.apps.shared.utils import datetime as dt_utils


logger = logging.getLogger(__name__)


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """Custom exception handler to standardise API error responses."""
    # Call DRF's default handler first
    response: Response | None = drf_exception_handler(exc, context)

    view = context.get("view")  # noqa: F841
    request: HttpRequest | None = context.get("request")

    # Unique error identifier for tracking
    error_id: str = str(uuid.uuid4())[:8]

    log_exception(exc, context, error_id)

    if response is not None:
        # Standardise an existing DRF response
        response.data = build_error_response(exc, response.data, request, error_id)
        add_error_headers(response, exc)
    elif isinstance(exc, DjangoValidationError):
        # DRF did not handle the exception - deal with it ourselves
        response = handle_django_validation_error(exc, request, error_id)
    elif isinstance(exc, IntegrityError):
        response = handle_integrity_error(exc, request, error_id)
    elif isinstance(exc, Http404):
        response = handle_http_404(exc, request, error_id)
    else:
        response = handle_unexpected_error(exc, request, error_id)

    return response  # type: ignore[return-value]


def build_error_response(  # noqa
    exc: Exception,
    original_data: dict[str, Any],
    request: HttpRequest | None,
    error_id: str,
) -> dict[str, Any]:
    """Build a standardised error response dictionary."""
    base: dict[str, Any] = {
        "error": True,
        "error_id": error_id,
        "timestamp": dt_utils.utc_now().isoformat(),
        "path": request.path if request else None,
        "method": request.method if request else None,
    }

    match exc:
        case ValidationError():
            base.update(
                {
                    "error_type": "validation_error",
                    "message": "Data validation failed",
                    "details": format_validation_errors(original_data),
                    "code": getattr(exc, "default_code", "validation_error"),
                }
            )

        case PermissionDenied():
            message = exc.detail.get("detail") if isinstance(exc.detail, dict) else str(exc.detail)
            base.update(
                {
                    "error_type": "permission_denied",
                    "message": message or "Permission denied",
                    "code": getattr(exc, "default_code", "permission_denied"),
                    "help": "Check your permissions or log in",
                }
            )

        case NotAuthenticated():
            base.update(
                {
                    "error_type": "authentication_required",
                    "message": "Authentication required",
                    "code": "not_authenticated",
                    "help": "Provide a valid authentication token",
                }
            )

        case AuthenticationFailed():
            message = exc.detail.get("detail") if isinstance(exc.detail, dict) else str(exc.detail)

            base.update(
                {
                    "error_type": "authentication_failed",
                    "message": message or "Authentication failed",
                    "code": getattr(exc, "default_code", "authentication_failed"),
                    "help": "Verify your credentials",
                }
            )

        case NotFound():
            message = exc.detail.get("detail") if isinstance(exc.detail, dict) else str(exc.detail)

            base.update(
                {
                    "error_type": "not_found",
                    "message": message or "Resource not found",
                    "code": getattr(exc, "default_code", "not_found"),
                    "help": "Check the URL and request parameters",
                }
            )

        case MethodNotAllowed():
            message = exc.detail.get("detail") if isinstance(exc.detail, dict) else str(exc.detail)

            base.update(
                {
                    "error_type": "method_not_allowed",
                    "message": f"Method {message} not allowed",
                    "code": "method_not_allowed",
                    "allowed_methods": getattr(exc, "detail", []),
                }
            )

        case Throttled():
            base.update(
                {
                    "error_type": "rate_limit_exceeded",
                    "message": "Rate limit exceeded",
                    "code": "throttled",
                    "retry_after": exc.wait,  # type: ignore[attr-defined]
                    "help": f"Retry after {exc.wait} seconds",  # type: ignore[attr-defined]
                }
            )

        case ParseError():
            base.update(
                {
                    "error_type": "parse_error",
                    "message": "Data parsing error",
                    "code": "parse_error",
                    "details": str(exc.detail) if hasattr(exc, "detail") else None,
                    "help": "Check the format of the submitted data",
                }
            )

        case UnsupportedMediaType():
            base.update(
                {
                    "error_type": "unsupported_media_type",
                    "message": "Unsupported media type",
                    "code": "unsupported_media_type",
                    "help": "Check the Content-Type header",
                }
            )

        case IshflowAPIException():
            message = exc.detail.get("detail") if isinstance(exc.detail, dict) else str(exc.detail)
            base.update(
                {
                    "error_type": "business_error",
                    "message": message or str(exc),
                    "code": getattr(exc, "default_code", "business_error"),
                }
            )

        case _:
            base.update(
                {
                    "error_type": "api_error",
                    "message": str(original_data.get("detail", "An API error occurred")),
                    "code": getattr(exc, "default_code", "api_error"),
                }
            )

    return base


def format_validation_errors(
    validation_errors: dict[str, Any] | list[Any] | Any,  # noqa: ANN401
) -> dict[str, list[str]] | list[str]:
    """Format validation errors into a readable structure."""
    if isinstance(validation_errors, dict):
        formatted: dict[str, list[str]] = {}
        for field, errors in validation_errors.items():
            formatted[field] = [str(e) for e in errors] if isinstance(errors, list) else [str(errors)]
        return formatted

    if isinstance(validation_errors, list):
        return [str(e) for e in validation_errors]

    return [str(validation_errors)]


def add_error_headers(response: Response, exc: Exception) -> None:
    """Add extra headers to the error response."""
    if isinstance(exc, Throttled):
        response["Retry-After"] = str(exc.wait)  # type: ignore[attr-defined]

    response["Access-Control-Expose-Headers"] = "Retry-After"


def handle_django_validation_error(exc: DjangoValidationError, request: HttpRequest | None, error_id: str) -> Response:
    """Handle Django ValidationError."""
    logger.warning("Django validation error [%s]: %s", error_id, exc)

    details = exc.message_dict if hasattr(exc, "message_dict") else [str(exc)]

    return Response(
        {
            "error": True,
            "error_id": error_id,
            "error_type": "validation_error",
            "message": "Data validation failed",
            "details": details,
            "code": "django_validation_error",
            "timestamp": dt_utils.utc_now().isoformat(),
            "path": request.path if request else None,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


def handle_integrity_error(exc: IntegrityError, request: HttpRequest | None, error_id: str) -> Response:
    """Handle database integrity errors."""
    logger.error("Database integrity error [%s]: %s", error_id, exc)

    msg = str(exc).lower()
    if "unique" in msg or "duplicate" in msg:
        message = "An object with this data already exists"
        code = "duplicate_entry"
        http_status = status.HTTP_409_CONFLICT
    elif "foreign key" in msg:
        message = "Foreign-key constraint violation"
        code = "foreign_key_violation"
        http_status = status.HTTP_400_BAD_REQUEST
    else:
        message = "Data integrity violation"
        code = "integrity_error"
        http_status = status.HTTP_400_BAD_REQUEST

    return Response(
        {
            "error": True,
            "error_id": error_id,
            "error_type": "integrity_error",
            "message": message,
            "code": code,
            "help": "Check uniqueness and referential integrity",
            "timestamp": dt_utils.utc_now().isoformat(),
            "path": request.path if request else None,
        },
        status=http_status,
    )


def handle_http_404(exc: Http404, request: HttpRequest | None, error_id: str) -> Response:  # noqa: ARG001
    """Handle 404 errors."""
    logger.warning(
        "HTTP 404 error [%s]: %s",
        error_id,
        request.path if request else "unknown path",
    )

    return Response(
        {
            "error": True,
            "error_id": error_id,
            "error_type": "not_found",
            "message": "The requested resource was not found",
            "code": "not_found",
            "help": "Verify the URL",
            "timestamp": dt_utils.utc_now().isoformat(),
            "path": request.path if request else None,
        },
        status=status.HTTP_404_NOT_FOUND,
    )


def handle_unexpected_error(exc: Exception, request: HttpRequest | None, error_id: str) -> Response:
    """Handle any unexpected exception."""
    logger.error("Unexpected error [%s]: %s", error_id, exc, exc_info=True)

    return Response(
        {
            "error": True,
            "error_id": error_id,
            "error_type": "server_error",
            "message": "Internal server error",
            "code": "internal_server_error",
            "help": "Contact the system administrator",
            "timestamp": dt_utils.utc_now().isoformat(),
            "path": request.path if request else None,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def log_exception(exc: Exception, context: dict[str, Any], error_id: str) -> None:
    """Log the exception with useful context."""
    view = context.get("view")
    request: HttpRequest | None = context.get("request")

    log_context: dict[str, Any] = {
        "error_id": error_id,
        "exception_type": type(exc).__name__,
        "view": (f"{view.__class__.__module__}.{view.__class__.__name__}" if view else None),
        "action": getattr(view, "action", None) if view else None,
        "user": str(request.user) if request and hasattr(request, "user") else None,
        "path": request.path if request else None,
        "method": request.method if request else None,
        "ip": get_client_ip(request) if request else None,
    }

    if isinstance(exc, (ValidationError | PermissionDenied | NotFound | NotAuthenticated)):
        logger.warning("API warning [%s]: %s", error_id, exc, extra=log_context)
    elif isinstance(exc, IshflowAPIException):
        logger.error("Business logic error [%s]: %s", error_id, exc, extra=log_context)
    else:
        logger.error("API error [%s]: %s", error_id, exc, extra=log_context, exc_info=True)


def get_client_ip(request: HttpRequest | None) -> str | None:
    """Return the client IP address."""
    if not request:
        return None

    if x_forwarded_for := request.META.get("HTTP_X_FORWARDED_FOR"):
        return x_forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")
