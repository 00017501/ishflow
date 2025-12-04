"""Custom viewsets with read/write serializer separation.

This module provides enhanced DRF viewsets that support separate
serializers for read and write operations.
"""

from rest_framework import mixins, viewsets

from .generics import GenericAPIView
from .mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin


class GenericViewSet(GenericAPIView, viewsets.GenericViewSet):
    """Base viewset that combines GenericAPIView with ViewSet functionality.

    Provides all the standard viewset features with support for
    separate read and write serializers.
    """


class ModelViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    mixins.DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """A viewset that provides default `create`, `retrieve`, `update`, `partial_update`, `destroy`, and `list` actions.

    Uses separate serializers for read and write operations.
    """


class ReadOnlyModelViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """A viewset that provides default `list` and `retrieve` actions.

    Uses read_serializer for all operations.
    """
