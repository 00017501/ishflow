"""Custom mixins for DRF views with read/write serializer separation.

This module provides enhanced versions of DRF's standard mixins that work
with our custom GenericAPIView to support separate read and write serializers.
"""

from rest_framework import mixins, status
from rest_framework.request import Request
from rest_framework.response import Response


class UpdateModelMixin(mixins.UpdateModelMixin):
    """Mixin to handle updating a model instance with separate read/write serializers."""

    def update(self, request: Request, *_args: str, **kwargs: bool | str) -> Response:
        """Update a model instance.

        Uses write_serializer for validation and deserialization,
        then uses read_serializer for the response.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()  # type: ignore[attr-defined]
        write_serializer = self.get_write_serializer(instance, data=request.data, partial=partial)  # type: ignore[attr-defined]
        write_serializer.is_valid(raise_exception=True)
        self.perform_update(write_serializer)  # type: ignore[attr-defined]

        if getattr(instance, "_prefetched_objects_cache", None) is not None:
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        read_serializer = self.get_read_serializer(write_serializer.instance)  # type: ignore[attr-defined]

        return Response(read_serializer.data)


class CreateModelMixin(mixins.CreateModelMixin):
    """Mixin to handle creating a model instance with separate read/write serializers."""

    def create(self, request: Request, *_args: str, **_kwargs: bool | str) -> Response:
        """Create a model instance.

        Uses write_serializer for validation and deserialization,
        then uses read_serializer for the response.
        """
        write_serializer = self.get_write_serializer(data=request.data)  # type: ignore[attr-defined]
        write_serializer.is_valid(raise_exception=True)
        self.perform_create(write_serializer)  # type: ignore[attr-defined]

        read_serializer = self.get_read_serializer(write_serializer.instance)  # type: ignore[attr-defined]
        headers = self.get_success_headers(read_serializer.data)  # type: ignore[attr-defined]

        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListModelMixin(mixins.ListModelMixin):
    """Mixin to handle listing a queryset using read serializer."""

    def list(self, _request: Request, *_args: str, **_kwargs: bool | str) -> Response:
        """List model instances.

        Uses read_serializer for serializing the queryset.
        Supports pagination.
        """
        queryset = self.filter_queryset(self.get_queryset())  # type: ignore[attr-defined]

        page = self.paginate_queryset(queryset)  # type: ignore[attr-defined]
        if page is not None:
            serializer = self.get_read_serializer(page, many=True)  # type: ignore[attr-defined]
            return self.get_paginated_response(serializer.data)  # type: ignore[attr-defined]

        serializer = self.get_read_serializer(queryset, many=True)  # type: ignore[attr-defined]
        return Response(serializer.data)


class RetrieveModelMixin(mixins.RetrieveModelMixin):
    """Mixin to handle retrieving a model instance using read serializer."""

    def retrieve(self, _request: Request, *_args: str, **_kwargs: bool | str) -> Response:
        """Retrieve a model instance.

        Uses read_serializer for serializing the instance.
        """
        instance = self.get_object()  # type: ignore[attr-defined]
        serializer = self.get_read_serializer(instance)  # type: ignore[attr-defined]
        return Response(serializer.data)
