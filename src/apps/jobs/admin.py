"""Admin configuration for the jobs app."""

from django.contrib import admin
from django.db.models import Count, QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import AutocompleteSelectMultipleFilter

from src.apps.applications.models.applications import ApplicationORM
from src.apps.jobs.models.jobs import EmploymentType, JobPostORM


class ApplicationInline(TabularInline):
    """Inline for displaying applications within job post admin."""

    model = ApplicationORM
    extra = 0
    can_delete = False
    fields = ("applicant", "status", "created_at")
    readonly_fields = ("applicant", "created_at")
    ordering = ("-created_at",)

    def has_add_permission(self, request: HttpRequest, obj: JobPostORM | None = None) -> bool:  # noqa: ARG002
        """Disable adding applications through inline."""
        return False


@admin.register(JobPostORM)
class JobPostAdmin(ModelAdmin):
    """Admin interface for Job Post model."""

    inlines = [ApplicationInline]
    list_filter_submit = True

    # List view configuration
    list_display = (
        "title",
        "company_name",
        "location",
        "employment_type_badge",
        "salary_range",
        "applications_count",
        "is_active",
        "created_at",
    )
    list_filter = (
        ("company", AutocompleteSelectMultipleFilter),
        "type",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "company__name",
        "location",
        "description",
    )
    ordering = ("-created_at",)
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")

    # Detail view configuration
    fieldsets = (
        (
            None,
            {
                "fields": ("company", "title", "type"),
            },
        ),
        (
            _("Job Details"),
            {
                "fields": ("description", "location"),
            },
        ),
        (
            _("Compensation"),
            {
                "fields": ("salary_min", "salary_max"),
            },
        ),
        (
            _("Metadata"),
            {
                "fields": ("created_at", "updated_at", "is_active"),
                "classes": ("collapse",),
            },
        ),
    )

    # Form configuration
    autocomplete_fields = ("company",)

    # Actions
    actions = ["mark_as_active", "mark_as_inactive"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[JobPostORM]:
        """Optimize queryset with select_related and annotate application count."""
        return (
            super().get_queryset(request).select_related("company").annotate(_applications_count=Count("applications"))
        )

    def company_name(self, obj: JobPostORM) -> str:
        """Get company name."""
        return obj.company.name

    company_name.short_description = _("Company")
    company_name.admin_order_field = "company__name"

    def employment_type_badge(self, obj: JobPostORM) -> str:
        """Display employment type with color coding."""
        color_map = {
            EmploymentType.FULL_TIME: "#28a745",  # Green
            EmploymentType.PART_TIME: "#17a2b8",  # Cyan
            EmploymentType.CONTRACT: "#ffc107",  # Yellow
            EmploymentType.INTERN: "#007bff",  # Blue
            EmploymentType.FREELANCE: "#6f42c1",  # Purple
        }
        color = color_map.get(obj.type, "#6c757d")
        return format_html(
            (
                '<span style="background-color: {}; color: white; padding: 3px 10px; '
                'border-radius: 3px; font-weight: bold;">{}</span>'
            ),
            color,
            obj.get_type_display(),  # type: ignore
        )

    employment_type_badge.short_description = _("Type")
    employment_type_badge.admin_order_field = "type"

    def salary_range(self, obj: JobPostORM) -> str:
        """Display salary range."""
        if obj.salary_min and obj.salary_max:
            return f"${obj.salary_min:,.0f} - ${obj.salary_max:,.0f}"
        elif obj.salary_min:  # noqa
            return f"${obj.salary_min:,.0f}+"
        elif obj.salary_max:
            return f"Up to ${obj.salary_max:,.0f}"
        return "Not specified"

    salary_range.short_description = _("Salary Range")

    def applications_count(self, obj: JobPostORM) -> int:
        """Get number of applications for this job post."""
        return getattr(obj, "_applications_count", obj.applications.count())  # type: ignore[attr-defined]

    applications_count.short_description = _("Applications")
    applications_count.admin_order_field = "_applications_count"  # type: ignore[attr-defined]

    # Admin actions
    @admin.action(description=_("Mark selected job posts as active"))
    def mark_as_active(self, request: HttpRequest, queryset: QuerySet[JobPostORM]) -> None:
        """Mark job posts as active."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} job post(s) marked as active.")

    @admin.action(description=_("Mark selected job posts as inactive"))
    def mark_as_inactive(self, request: HttpRequest, queryset: QuerySet[JobPostORM]) -> None:
        """Mark job posts as inactive."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} job post(s) marked as inactive.")
