"""Generic API views with separate read and write serializers.

This module provides enhanced DRF generic views that support:
- Separate serializers for read and write operations
- Full type annotations for better IDE support
- Custom mixins for additional functionality
"""

from rest_framework import generics, mixins, serializers
from rest_framework.request import Request
from rest_framework.response import Response

from .mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin


class GenericAPIView(generics.GenericAPIView):
    """Base class for all generic API views with separate read and write serializers.

    This view allows you to define different serializers for reading and writing,
    which is useful when you want to return more information than what's required
    for creation/updates, or when you need different validation logic.

    Attributes:
        read_serializer_class: Serializer used for GET requests
        write_serializer_class: Serializer used for POST, PUT, PATCH requests
    """

    read_serializer_class: type[serializers.Serializer] | None = None
    write_serializer_class: type[serializers.Serializer] | None = None

    def get_serializer_class(self) -> type[serializers.Serializer]:
        """Return the class to use for the serializer.

        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        if self.serializer_class is None and self.read_serializer_class is None:
            msg = (
                f"'{self.__class__.__name__}' should either include one of "
                "`serializer_class` and `read_serializer_class` attribute, "
                "or override one of the `get_serializer_class()`, "
                "`get_read_serializer_class()` method."
            )
            raise AssertionError(msg)

        return self.serializer_class  # type: ignore[return-value]

    def get_read_serializer(self, *args: object, **kwargs: object) -> serializers.Serializer:
        """Return the serializer instance that should be used for serializing output."""
        serializer_class = self.get_read_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_read_serializer_class(self) -> type[serializers.Serializer]:
        """Return the class to use for the read serializer.

        Defaults to using `self.read_serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        if self.read_serializer_class is None:
            return self.get_serializer_class()

        return self.read_serializer_class

    def get_write_serializer(self, *args: object, **kwargs: object) -> serializers.Serializer:
        """Return the serializer instance for validating and deserializing input."""
        serializer_class = self.get_write_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_write_serializer_class(self) -> type[serializers.Serializer]:
        """Return the class to use for the write serializer.

        Defaults to using `self.write_serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins can send extra fields, others cannot)
        """
        if self.write_serializer_class is None:
            return self.get_serializer_class()

        return self.write_serializer_class


class CreateAPIView(CreateModelMixin, GenericAPIView):
    """Concrete view for creating a model instance."""

    def post(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle POST request to create a new instance."""
        return self.create(request, *args, **kwargs)


class UpdateAPIView(UpdateModelMixin, GenericAPIView):
    """Concrete view for updating a model instance."""

    def put(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle PUT request to fully update an instance."""
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle PATCH request to partially update an instance."""
        return self.partial_update(request, *args, **kwargs)


class ListAPIView(ListModelMixin, GenericAPIView):
    """Concrete view for listing a queryset."""

    def get(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle GET request to list instances."""
        return self.list(request, *args, **kwargs)


class RetrieveAPIView(RetrieveModelMixin, GenericAPIView):
    """Concrete view for retrieving a model instance."""

    def get(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle GET request to retrieve an instance."""
        return self.retrieve(request, *args, **kwargs)


class ListCreateAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Concrete view for listing a queryset or creating a model instance."""

    def get(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle GET request to list instances."""
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle POST request to create a new instance."""
        return self.create(request, *args, **kwargs)


class RetrieveDestroyAPIView(RetrieveModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    """Concrete view for retrieving or deleting a model instance."""

    def get(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle GET request to retrieve an instance."""
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle DELETE request to destroy an instance."""
        return self.destroy(request, *args, **kwargs)  # type: ignore[attr-defined]


class RetrieveUpdateAPIView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    """Concrete view for retrieving or updating a model instance."""

    def get(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle GET request to retrieve an instance."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle PUT request to fully update an instance."""
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle PATCH request to partially update an instance."""
        return self.partial_update(request, *args, **kwargs)  # type: ignore[attr-defined]


class RetrieveUpdateDestroyAPIView(RetrieveModelMixin, UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    """Concrete view for retrieving, updating, or deleting a model instance."""

    def get(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle GET request to retrieve an instance."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle PUT request to fully update an instance."""
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle PATCH request to partially update an instance."""
        return self.partial_update(request, *args, **kwargs)  # type: ignore[attr-defined]

    def delete(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle DELETE request to destroy an instance."""
        return self.destroy(request, *args, **kwargs)  # type: ignore[attr-defined]


class DestroyAPIView(mixins.DestroyModelMixin, GenericAPIView):
    """Concrete view for deleting a model instance."""

    def delete(self, request: Request, *args: str, **kwargs: bool | str) -> Response:
        """Handle DELETE request to destroy an instance."""
        return self.destroy(request, *args, **kwargs)
