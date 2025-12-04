"""Admin configuration for the candidates app."""

from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from src.apps.candidates.models.candidates import CandidateORM


class CandidateAdminForm(forms.ModelForm):
    """Custom form for Candidate admin with proper skills handling."""

    skills_display = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"rows": 3, "placeholder": "Enter skills separated by commas (e.g., Python, Django, React)"}
        ),
        label="Skills",
        help_text="Enter skills separated by commas",
    )

    class Meta:
        """Meta options for CandidateAdminForm."""

        model = CandidateORM
        fields = "__all__"

    def __init__(self, *args, **kwargs):  # noqa
        """Initialize the form and populate skills_display from skills field."""
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.skills:
            # Convert list back to comma-separated string for display
            if isinstance(self.instance.skills, list):
                self.initial["skills_display"] = ", ".join(self.instance.skills)
            else:
                self.initial["skills_display"] = self.instance.skills

        # Hide the original skills field
        if "skills" in self.fields:
            self.fields["skills"].widget = forms.HiddenInput()

    def clean_skills_display(self) -> list[str]:
        """Clean and validate the skills_display field."""
        skills_text = self.cleaned_data.get("skills_display", "")
        if not skills_text:
            return []
        # Split by comma, strip whitespace, and filter out empty strings
        return [skill.strip() for skill in skills_text.split(",") if skill.strip()]

    def save(self, commit: bool = True) -> CandidateORM:
        """Save the form and update skills from skills_display."""
        instance = super().save(commit=False)
        instance.skills = self.cleaned_data.get("skills_display", [])
        if commit:
            instance.save()
        return instance


@admin.register(CandidateORM)
class CandidateAdmin(ModelAdmin):
    """Admin interface for Candidate model."""

    form = CandidateAdminForm

    # List view configuration
    list_display = (
        "user_email",
        "full_name",
        "skills_preview",
        "is_open_to_work",
        "profile_completion",
        "created_at",
    )
    list_filter = (
        "is_open_to_work",
        "is_searching_actively",
        "salary_currency",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "current_title",
        "location",
        "skills",
    )
    ordering = ("-created_at",)
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at", "profile_completion_badge")

    # Detail view configuration
    fieldsets = (
        (
            None,
            {
                "fields": ("user",),
            },
        ),
        (
            _("Core Profile"),
            {
                "fields": ("resume", "cover_letter", "bio", "location"),
            },
        ),
        (
            _("Professional Information"),
            {
                "fields": (
                    "current_title",
                    "years_of_experience",
                    "skills_display",
                    "linkedin_url",
                    "github_url",
                    "portfolio_url",
                ),
            },
        ),
        (
            _("Job Preferences"),
            {
                "fields": (
                    "is_open_to_work",
                    "is_searching_actively",
                    "desired_salary_min",
                    "desired_salary_max",
                    "salary_currency",
                    "available_from",
                ),
            },
        ),
        (
            _("Metadata"),
            {
                "fields": ("created_at", "updated_at", "is_active", "profile_completion_badge"),
                "classes": ("collapse",),
            },
        ),
    )

    # Form configuration
    autocomplete_fields = ("user",)

    def user_email(self, obj: CandidateORM) -> str:
        """Get user's email."""
        return obj.user.email

    user_email.short_description = _("Email")
    user_email.admin_order_field = "user__email"

    def full_name(self, obj: CandidateORM) -> str:
        """Get user's full name."""
        return obj.user.full_name

    full_name.short_description = _("Full Name")
    full_name.admin_order_field = "user__first_name"

    def has_resume(self, obj: CandidateORM) -> bool:
        """Check if candidate has uploaded a resume."""
        return bool(obj.resume)

    has_resume.boolean = True
    has_resume.short_description = _("Has Resume")

    def skills_preview(self, obj: CandidateORM) -> str:
        """Display first 3 skills as a preview."""
        if not obj.skills:
            return "-"
        skills_list = obj.skills if isinstance(obj.skills, list) else []
        if not skills_list:
            return "-"
        preview = skills_list[:3]
        result = ", ".join(preview)
        if (more := len(skills_list) - 3) > 0:
            result += f" (+{more} more)"
        return result

    skills_preview.short_description = _("Skills")

    def profile_completion(self, obj: CandidateORM) -> str:
        """Show profile completion status."""
        return "✅ Complete" if obj.has_completed_profile else "⚠️ Incomplete"

    profile_completion.short_description = _("Profile")

    def profile_completion_badge(self, obj: CandidateORM) -> str:
        """Show colored profile completion badge."""
        if obj.has_completed_profile:
            return format_html('<span style="color: #28a745; font-weight: bold;">✅ Profile Complete</span>')
        return format_html(
            '<span style="color: #ffc107; font-weight: bold;">⚠️ Profile Incomplete (Resume and Skills required)</span>'
        )

    profile_completion_badge.short_description = _("Profile Status")
