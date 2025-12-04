"""Job post forms."""

from django import forms

from src.apps.applications.models.applications import ApplicationORM
from src.apps.jobs.models.jobs import JobPostORM


class JobPostForm(forms.ModelForm):
    """Form for creating and editing job posts."""

    class Meta:
        """Meta options for JobPostForm."""

        model = JobPostORM
        fields = [
            "title",
            "description",
            "location",
            "type",
            "salary_min",
            "salary_max",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Senior Software Engineer",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 8,
                    "placeholder": "Describe the role, responsibilities, and requirements...",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., New York, NY or Remote",
                }
            ),
            "type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "salary_min": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Min salary",
                    "step": "0.01",
                }
            ),
            "salary_max": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Max salary",
                    "step": "0.01",
                }
            ),
        }
        labels = {
            "title": "Job Title",
            "description": "Job Description",
            "location": "Location",
            "type": "Employment Type",
            "salary_min": "Minimum Salary",
            "salary_max": "Maximum Salary",
        }
        help_texts = {
            "salary_min": "Optional: Minimum salary range",
            "salary_max": "Optional: Maximum salary range",
        }

    def clean(self) -> dict:
        """Validate salary range."""
        cleaned_data = super().clean()
        if not cleaned_data:
            return {}

        salary_min = cleaned_data.get("salary_min")
        salary_max = cleaned_data.get("salary_max")

        if salary_min and salary_max and salary_min > salary_max:
            raise forms.ValidationError("Minimum salary cannot be greater than maximum salary.")

        return cleaned_data


class JobApplicationForm(forms.ModelForm):
    """Form for applying to a job."""

    class Meta:
        """Meta options for JobApplicationForm."""

        model = ApplicationORM
        fields = ["cover_letter"]
        widgets = {
            "cover_letter": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 8,
                    "placeholder": "Write a cover letter to introduce yourself and explain why you're a great fit for this position...",  # noqa: E501
                }
            ),
        }
        labels = {
            "cover_letter": "Cover Letter",
        }
        help_texts = {
            "cover_letter": "Optional: Add a personalized cover letter for this application",
        }
