"""Job CRUD service layer."""

from typing import Any

from django.db.models import QuerySet

from src.apps.companies.models.companies import CompanyORM
from src.apps.jobs.models.jobs import JobPostORM


class JobService:
    """Service for job post operations."""

    @staticmethod
    def create_job(company: CompanyORM, **job_data: Any) -> JobPostORM:  # noqa: ANN401
        """Create a new job post for a company.

        Args:
            company: The company creating the job post
            **job_data: Job post data

        Returns:
            JobPostORM: The created job post
        """
        return JobPostORM.objects.create(
            company=company,
            **job_data,
        )

    @staticmethod
    def update_job(job: JobPostORM, **job_data: Any) -> JobPostORM:  # noqa: ANN401
        """Update an existing job post.

        Args:
            job: The job post to update
            **job_data: Updated job post data

        Returns:
            JobPostORM: The updated job post
        """
        for field, value in job_data.items():
            setattr(job, field, value)
        job.save()
        return job

    @staticmethod
    def delete_job(job: JobPostORM) -> None:
        """Delete a job post.

        Args:
            job: The job post to delete
        """
        job.delete()

    @staticmethod
    def get_company_jobs(company: CompanyORM) -> QuerySet[JobPostORM]:
        """Get all jobs for a specific company.

        Args:
            company: The company to get jobs for

        Returns:
            QuerySet[JobPostORM]: Job posts for the company
        """
        return JobPostORM.objects.filter(company=company).select_related("company").order_by("-created_at")

    @staticmethod
    def get_job_by_id(job_id: int, company: CompanyORM | None = None) -> JobPostORM | None:
        """Get a job post by ID, optionally filtered by company.

        Args:
            job_id: The ID of the job post
            company: Optional company to filter by

        Returns:
            JobPostORM | None: The job post or None if not found
        """
        queryset = JobPostORM.objects.select_related("company")
        if company:
            queryset = queryset.filter(company=company)

        try:
            return queryset.get(id=job_id)
        except JobPostORM.DoesNotExist:
            return None
