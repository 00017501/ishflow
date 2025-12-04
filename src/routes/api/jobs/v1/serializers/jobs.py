"""Job post serializers."""

from rest_framework import serializers

from src.apps.companies.models.companies import CompanyORM
from src.apps.jobs.models.jobs import JobPostORM


class _CompanyInJobSerializer(serializers.ModelSerializer):
    """Serializer for company details in job response."""

    class Meta:
        """Meta class for _CompanyInJobSerializer."""

        model = CompanyORM
        fields = ["id", "name", "logo"]


class ReadJobSerializer(serializers.ModelSerializer):
    """Serializer for reading job post information."""

    company = _CompanyInJobSerializer(read_only=True)

    class Meta:
        """Meta class for ReadJobSerializer."""

        model = JobPostORM
        fields = [
            "id",
            "title",
            "description",
            "location",
            "type",
            "salary_min",
            "salary_max",
            "company",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class CreateJobSerializer(serializers.ModelSerializer):
    """Serializer for creating job posts."""

    class Meta:
        """Meta class for CreateJobSerializer."""

        model = JobPostORM
        fields = [
            "title",
            "description",
            "location",
            "type",
            "salary_min",
            "salary_max",
        ]

    def validate(self, attrs: dict) -> dict:
        """Validate salary range."""
        salary_min = attrs.get("salary_min")
        salary_max = attrs.get("salary_max")

        if salary_min and salary_max and salary_min > salary_max:
            raise serializers.ValidationError({"salary_min": "Minimum salary cannot be greater than maximum salary."})

        return attrs


class UpdateJobSerializer(serializers.ModelSerializer):
    """Serializer for updating job posts."""

    class Meta:
        """Meta class for UpdateJobSerializer."""

        model = JobPostORM
        fields = [
            "title",
            "description",
            "location",
            "type",
            "salary_min",
            "salary_max",
        ]

    def validate(self, attrs: dict) -> dict:
        """Validate salary range."""
        salary_min = attrs.get("salary_min", self.instance.salary_min if self.instance else None)
        salary_max = attrs.get("salary_max", self.instance.salary_max if self.instance else None)

        if salary_min and salary_max and salary_min > salary_max:
            raise serializers.ValidationError({"salary_min": "Minimum salary cannot be greater than maximum salary."})

        return attrs


class JobListSerializer(serializers.ModelSerializer):
    """Serializer for listing job posts (summary view)."""

    company = _CompanyInJobSerializer(read_only=True)

    class Meta:
        """Meta class for JobListSerializer."""

        model = JobPostORM
        fields = [
            "id",
            "title",
            "location",
            "type",
            "salary_min",
            "salary_max",
            "company",
            "created_at",
        ]
        read_only_fields = fields
