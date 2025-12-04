"""Job service layer."""

from typing import Any

from django.db.models import Q, QuerySet

from src.apps.companies.models.companies import CompanyORM
from src.apps.jobs.models.jobs import JobPostORM


def search_and_filter_jobs(
    search_query: str = "",
    job_type: str = "",
    location: str = "",
) -> QuerySet[JobPostORM]:
    """Search and filter job posts."""
    jobs = JobPostORM.objects.select_related("company")

    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(company__name__icontains=search_query)
        )

    if job_type:
        jobs = jobs.filter(type=job_type)

    if location:
        jobs = jobs.filter(location__icontains=location)

    return jobs


def create_job_post(company: CompanyORM, **job_data: Any) -> JobPostORM:  # noqa: ANN401
    """Create a new job post for a company."""
    return JobPostORM.objects.create(
        company=company,
        **job_data,
    )
