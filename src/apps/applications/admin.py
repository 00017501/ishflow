"""Admin configuration for the applications app."""

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from src.apps.applications.models.applications import ApplicationORM, ApplicationStatus


@admin.register(ApplicationORM)
class ApplicationAdmin(ModelAdmin):
    """Admin interface for Application model."""

    # List view configuration
    list_display = (
        "id",
        "applicant_name",
        "applicant_email",
        "job_title",
        "company_name",
        "status_badge",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "status",
        "created_at",
        "updated_at",
        ("post__company", admin.RelatedOnlyFieldListFilter),
    )
    search_fields = (
        "applicant__user__email",
        "applicant__user__first_name",
        "applicant__user__last_name",
        "post__title",
        "post__company__name",
        "cover_letter",
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
                "fields": ("applicant", "post", "status"),
            },
        ),
        (
            _("Application Details"),
            {
                "fields": ("cover_letter",),
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
    autocomplete_fields = ("applicant", "post")

    # Actions
    actions = ["mark_as_under_review", "mark_as_interview_scheduled", "mark_as_offered", "mark_as_rejected"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[ApplicationORM]:
        """Optimize queryset with select_related for related objects."""
        return (
            super()
            .get_queryset(request)
            .select_related(
                "applicant__user",
                "post",
                "post__company",
            )
        )

    def applicant_name(self, obj: ApplicationORM) -> str:
        """Get applicant's full name."""
        return obj.applicant.user.full_name

    applicant_name.short_description = _("Applicant")
    applicant_name.admin_order_field = "applicant__user__first_name"

    def applicant_email(self, obj: ApplicationORM) -> str:
        """Get applicant's email."""
        return obj.applicant.user.email

    applicant_email.short_description = _("Email")
    applicant_email.admin_order_field = "applicant__user__email"

    def job_title(self, obj: ApplicationORM) -> str:
        """Get job post title."""
        return obj.post.title

    job_title.short_description = _("Job Title")
    job_title.admin_order_field = "post__title"

    def company_name(self, obj: ApplicationORM) -> str:
        """Get company name."""
        return obj.post.company.name

    company_name.short_description = _("Company")
    company_name.admin_order_field = "post__company__name"

    def status_badge(self, obj: ApplicationORM) -> str:
        """Display status with color coding."""
        color_map = {
            ApplicationStatus.APPLIED: "#17a2b8",  # Info blue
            ApplicationStatus.UNDER_REVIEW: "#ffc107",  # Warning yellow
            ApplicationStatus.INTERVIEW_SCHEDULED: "#007bff",  # Primary blue
            ApplicationStatus.OFFERED: "#28a745",  # Success green
            ApplicationStatus.REJECTED: "#dc3545",  # Danger red
        }
        color = color_map.get(obj.status, "#6c757d")
        return format_html(
            (
                '<span style="background-color: {}; color: white; padding:'
                ' 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>'
            ),
            color,
            obj.get_status_display(),  # type: ignore
        )

    status_badge.short_description = _("Status")
    status_badge.admin_order_field = "status"

    # Admin actions
    @admin.action(description=_("Mark selected applications as Under Review"))
    def mark_as_under_review(self, request: HttpRequest, queryset: QuerySet[ApplicationORM]) -> None:
        """Mark applications as under review."""
        updated = queryset.update(status=ApplicationStatus.UNDER_REVIEW)
        self.message_user(request, f"{updated} application(s) marked as Under Review.")

    @admin.action(description=_("Mark selected applications as Interview Scheduled"))
    def mark_as_interview_scheduled(self, request: HttpRequest, queryset: QuerySet[ApplicationORM]) -> None:
        """Mark applications as interview scheduled."""
        updated = queryset.update(status=ApplicationStatus.INTERVIEW_SCHEDULED)
        self.message_user(request, f"{updated} application(s) marked as Interview Scheduled.")

    @admin.action(description=_("Mark selected applications as Offered"))
    def mark_as_offered(self, request: HttpRequest, queryset: QuerySet[ApplicationORM]) -> None:
        """Mark applications as offered."""
        updated = queryset.update(status=ApplicationStatus.OFFERED)
        self.message_user(request, f"{updated} application(s) marked as Offered.")

    @admin.action(description=_("Mark selected applications as Rejected"))
    def mark_as_rejected(self, request: HttpRequest, queryset: QuerySet[ApplicationORM]) -> None:
        """Mark applications as rejected."""
        updated = queryset.update(status=ApplicationStatus.REJECTED)
        self.message_user(request, f"{updated} application(s) marked as Rejected.")
