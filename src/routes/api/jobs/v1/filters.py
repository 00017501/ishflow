"""Job post filters."""

from django_filters import rest_framework as filters

from src.apps.jobs.models.jobs import EmploymentType, JobPostORM


class JobFilter(filters.FilterSet):
    """Filter set for job posts."""

    # Filter by employment type
    type = filters.ChoiceFilter(
        field_name="type",
        choices=EmploymentType.choices,
        label="Employment Type",
    )

    # Filter by location (case-insensitive contains)
    location = filters.CharFilter(
        field_name="location",
        lookup_expr="icontains",
        label="Location",
    )

    # Salary range filters
    salary_min_gte = filters.NumberFilter(
        field_name="salary_min",
        lookup_expr="gte",
        label="Minimum Salary (>=)",
    )

    salary_max_lte = filters.NumberFilter(
        field_name="salary_max",
        lookup_expr="lte",
        label="Maximum Salary (<=)",
    )

    # Company filter
    company = filters.NumberFilter(
        field_name="company__id",
        label="Company ID",
    )

    class Meta:
        """Meta class for JobFilter."""

        model = JobPostORM
        fields = ["type", "location", "company"]
