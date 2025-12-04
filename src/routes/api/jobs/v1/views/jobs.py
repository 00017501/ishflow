"""Job post views."""

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.jobs.models.jobs import JobPostORM
from src.apps.jobs.services.job_crud import JobService
from src.apps.shared.views.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from src.routes.api.accounts.v1.permissions import IsCompanyOwnerUser
from src.routes.api.jobs.v1.filters import JobFilter
from src.routes.api.jobs.v1.permissions import CanManageJob, IsEmployerWithCompany
from src.routes.api.jobs.v1.serializers import (
    CreateJobSerializer,
    JobListSerializer,
    ReadJobSerializer,
    UpdateJobSerializer,
)


class JobListView(ListAPIView):
    """View for listing all published job posts."""

    queryset = JobPostORM.objects.select_related("company").all()
    serializer_class = JobListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = JobFilter
    search_fields = ["title", "description", "company__name"]

    @extend_schema(
        summary="List Job Posts",
        description="Retrieve a list of all published job posts with optional search and filters.",
        tags=["Jobs"],
    )
    def get(self, request: Request) -> Response:
        """Handle requests to list job posts.

        Returns:
            Response: List of job posts
        """
        return super().get(request)


class JobDetailView(RetrieveAPIView):
    """View for retrieving a single job post."""

    serializer_class = ReadJobSerializer
    permission_classes = [AllowAny]
    queryset = JobPostORM.objects.select_related("company").all()

    @extend_schema(
        summary="Retrieve Job Post",
        description="Retrieve detailed information about a specific job post.",
        tags=["Jobs"],
    )
    def get(self, request: Request, pk: int) -> Response:
        """Handle requests to retrieve a job post.

        Args:
            request: The HTTP request object
            pk: Job post ID

        Returns:
            Response: Job post data
        """
        return super().get(request, pk=pk)  # type: ignore


class MyJobsView(ListAPIView):
    """View for listing jobs posted by the employer's company."""

    serializer_class = ReadJobSerializer
    permission_classes = [IsEmployerWithCompany]
    filterset_class = JobFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]
    queryset = JobPostORM.objects.none()  # Placeholder, overridden in get_queryset (so drf-spectacular picks it up)
    search_fields = ["title", "description", "company__name"]

    def get_queryset(self) -> QuerySet[JobPostORM]:
        """Get jobs for the current user's company."""
        return (
            JobPostORM.objects.filter(company=self.request.user.company)  # type: ignore
            .select_related("company")
            .order_by("-created_at")
        )

    @extend_schema(
        summary="List My Company's Jobs",
        description="Retrieve a list of all job posts created by your company.",
        tags=["Jobs"],
    )
    def get(self, request: Request) -> Response:
        """Handle requests to list company's job posts.

        Returns:
            Response: List of company's job posts
        """
        return super().get(request)


@extend_schema(
    summary="Create Job Post",
    description="Create a new job post. Only authenticated employers with a company can create job posts.",
    tags=["Jobs"],
    responses={201: ReadJobSerializer},
)
class JobCreateView(CreateAPIView):
    """View for creating a new job post."""

    serializer_class = CreateJobSerializer
    write_serializer_class = CreateJobSerializer
    read_serializer_class = ReadJobSerializer

    permission_classes = [IsEmployerWithCompany]

    def perform_create(self, serializer: CreateJobSerializer) -> None:
        """Create a new job post associated with the user's company."""
        # Create job using service layer
        self.instance = JobService.create_job(
            company=self.request.user.company,  # type: ignore
            **serializer.validated_data,
        )


class JobUpdateView(UpdateAPIView):
    """View for updating an existing job post."""

    serializer_class = UpdateJobSerializer
    write_serializer_class = UpdateJobSerializer
    read_serializer_class = ReadJobSerializer
    permission_classes = [IsEmployerWithCompany, CanManageJob]
    queryset = JobPostORM.objects.none()  # Placeholder, overridden in get_queryset

    def get_queryset(self) -> QuerySet[JobPostORM]:
        """Get jobs for the current user's company."""
        return JobPostORM.objects.filter(company=self.request.user.company).select_related("company")  # type: ignore

    @extend_schema(
        summary="Update Job Post",
        description="Update an existing job post. Only the company that created the job can update it.",
        tags=["Jobs"],
        responses={200: ReadJobSerializer},
    )
    def put(self, request: Request, pk: int) -> Response:
        """Handle requests to update a job post.

        Args:
            request: The HTTP request object
            pk: Job post ID

        Returns:
            Response: Updated job post data
        """
        return super().put(request, pk=pk)  # type: ignore

    @extend_schema(
        summary="Partially Update Job Post",
        description="Partially update an existing job post. Only the company that created the job can update it.",
        tags=["Jobs"],
        responses={200: ReadJobSerializer},
    )
    def patch(self, request: Request, pk: int) -> Response:
        """Handle requests to partially update a job post.

        Args:
            request: The HTTP request object
            pk: Job post ID

        Returns:
            Response: Updated job post data
        """
        return super().patch(request, pk=pk)  # type: ignore


class JobDeleteView(DestroyAPIView):
    """View for deleting a job post."""

    serializer_class = ReadJobSerializer
    permission_classes = [IsEmployerWithCompany, CanManageJob, IsCompanyOwnerUser]
    queryset = JobPostORM.objects.none()  # Placeholder, overridden in get_queryset

    def get_queryset(self) -> QuerySet[JobPostORM]:
        """Get jobs for the current user's company."""
        return JobPostORM.objects.filter(company=self.request.user.company).select_related("company")  # type: ignore

    @extend_schema(
        summary="Delete Job Post",
        description="Delete a job post. Only the company that created the job can delete it.",
        tags=["Jobs"],
        responses={204: None},
    )
    def delete(self, request: Request, pk: int) -> Response:
        """Handle requests to delete a job post.

        Args:
            request: The HTTP request object
            pk: Job post ID

        Returns:
            Response: No content
        """
        return super().delete(request, pk=pk)  # type: ignore
