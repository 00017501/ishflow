"""Forms for interview scheduling."""

from django import forms
from django.utils import timezone

from src.apps.interviews.models.interviews import InterviewSlotORM


class InterviewSlotForm(forms.ModelForm):
    """Form for proposing interview time slots."""

    class Meta:
        """Meta options."""

        model = InterviewSlotORM
        fields = ["start_time", "end_time", "location", "meeting_link", "notes"]
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
            "end_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Office - Room 301 or Leave blank for online",
                }
            ),
            "meeting_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., https://meet.google.com/xxx-yyyy-zzz",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Additional notes for the candidate...",
                }
            ),
        }
        labels = {
            "start_time": "Start Time",
            "end_time": "End Time",
            "location": "Location (Optional)",
            "meeting_link": "Meeting Link (Optional)",
            "notes": "Notes (Optional)",
        }

    def clean(self) -> dict:
        """Validate time slots."""
        cleaned_data = super().clean()
        if not cleaned_data:
            return {}

        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time:
            # Check that end time is after start time
            if end_time <= start_time:
                raise forms.ValidationError("End time must be after start time.")

            # Check that start time is in the future
            if start_time <= timezone.now():
                raise forms.ValidationError("Interview time must be in the future.")

            # Check duration (should be at least 15 minutes and max 4 hours)
            duration = (end_time - start_time).total_seconds() / 60  # in minutes
            if duration < 15:  # noqa: PLR2004
                raise forms.ValidationError("Interview must be at least 15 minutes long.")
            if duration > 240:  # 4 hours  # noqa: PLR2004
                raise forms.ValidationError("Interview cannot be longer than 4 hours.")

        return cleaned_data
