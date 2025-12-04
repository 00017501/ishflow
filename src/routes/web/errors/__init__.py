"""Error views."""

from src.routes.web.errors.views import forbidden_view, page_not_found_view, server_error_view


__all__ = [
    "forbidden_view",
    "page_not_found_view",
    "server_error_view",
]
