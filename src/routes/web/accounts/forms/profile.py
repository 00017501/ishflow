"""Forms for user profile editing."""

from django import forms

from src.apps.accounts.models import UserORM
from src.apps.candidates.models.candidates import CandidateORM
from src.apps.companies.models.companies import CompanyORM


class UserProfileForm(forms.ModelForm):
    """Form for editing basic user information."""

    class Meta:
        """Meta options for UserProfileForm."""

        model = UserORM
        fields = ["first_name", "last_name", "phone_number"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First Name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last Name",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+1234567890",
                }
            ),
        }


class CandidateProfileForm(forms.ModelForm):
    """Form for editing candidate profile information."""

    class Meta:
        """Meta options for CandidateProfileForm."""

        model = CandidateORM
        fields = [
            "bio",
            "location",
            "skills",
            "years_of_experience",
            "current_title",
            "desired_salary_min",
            "desired_salary_max",
            "salary_currency",
            "resume",
            "cover_letter",
        ]
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Tell us about yourself...",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "City, Country",
                }
            ),
            "skills": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Python, Django, JavaScript, React...",
                }
            ),
            "years_of_experience": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "placeholder": "Years of experience",
                }
            ),
            "current_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Senior Software Engineer",
                }
            ),
            "desired_salary_min": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "1000",
                    "placeholder": "Minimum expected salary",
                }
            ),
            "desired_salary_max": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "1000",
                    "placeholder": "Maximum expected salary",
                }
            ),
            "salary_currency": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "resume": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.doc,.docx",
                }
            ),
            "cover_letter": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Your default cover letter...",
                }
            ),
        }
        help_texts = {
            "skills": "Separate multiple skills with commas",
            "resume": "PDF, DOC, or DOCX file (max 5MB)",
            "desired_salary_min": "Optional: Your minimum expected salary",
            "desired_salary_max": "Optional: Your maximum expected salary",
        }

    def clean(self) -> dict:
        """Validate salary range."""
        cleaned_data = super().clean()
        if not cleaned_data:
            return {}

        salary_min = cleaned_data.get("desired_salary_min")
        salary_max = cleaned_data.get("desired_salary_max")

        if salary_min and salary_max and salary_min > salary_max:
            raise forms.ValidationError("Minimum salary cannot be greater than maximum salary.")

        return cleaned_data


class CompanyProfileForm(forms.ModelForm):
    """Form for editing company information."""

    class Meta:
        """Meta options for CompanyProfileForm."""

        model = CompanyORM
        fields = ["name", "description", "website", "logo"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Company Name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe your company...",
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://www.example.com",
                }
            ),
            "logo": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
        }
        help_texts = {
            "logo": "Company logo image (max 5MB)",
            "website": "Your company's website URL",
        }
