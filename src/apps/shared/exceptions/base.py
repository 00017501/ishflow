"""Base Exception Classes for the project."""

from typing import Any

from rest_framework import status
from rest_framework.exceptions import APIException


class IshflowAPIException(APIException):
    """Base exception for ISHFLOW API."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail: str = "A server error occurred"
    default_code: str = "server_error"

    def __init__(
        self,
        detail: str | dict[str, Any] | list[Any] | None = None,
        code: str | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(detail, code)
        if status_code is not None:
            self.status_code = status_code
