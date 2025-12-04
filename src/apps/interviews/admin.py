"""Admin configuration for the interviews app."""

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline

from src.apps.interviews.models.interviews import InterviewORM, InterviewSlotORM, InterviewStatusOptions, SlotStatus


class InterviewSlotInline(TabularInline):
    """Inline for interview slots within interview admin."""

    model = InterviewSlotORM
    extra = 0
    fields = ("start_time", "end_time", "status", "proposed_by", "location", "meeting_link", "notes")
    readonly_fields = ("proposed_by", "created_at")
    ordering = ("-created_at",)

    def has_add_permission(self, request: HttpRequest, obj: InterviewORM | None = None) -> bool:  # noqa: ARG002
        """Disable adding slots through inline."""
        return False


@admin.register(InterviewORM)
class InterviewAdmin(ModelAdmin):
    """Admin interface for Interview model."""

    # List view configuration
    list_display = (
        "id",
        "candidate_name",
        "job_title",
        "company_name",
        "accepted_slot_time",
        "status_badge",
        "created_at",
    )
    list_filter = (
        "status",
        "created_at",
        ("company", admin.RelatedOnlyFieldListFilter),
    )
    search_fields = (
        "application__applicant__user__email",
        "application__applicant__user__first_name",
        "application__applicant__user__last_name",
        "application__post__title",
        "company__name",
        "notes",
    )
    ordering = ("-created_at",)
    list_per_page = 25
    readonly_fields = ("created_at", "updated_at")

    # Inlines
    inlines = [InterviewSlotInline]

    # Detail view configuration
    fieldsets = (
        (
            None,
            {
                "fields": ("company", "application", "status"),
            },
        ),
        (
            _("Notes"),
            {
                "fields": ("notes",),
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
    autocomplete_fields = ("company", "application")

    # Actions
    actions = ["mark_as_completed", "mark_as_canceled"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[InterviewORM]:
        """Optimize queryset with select_related for related objects."""
        return (
            super()
            .get_queryset(request)
            .select_related(
                "company",
                "application__applicant__user",
                "application__post",
            )
            .prefetch_related("slots")
        )

    def candidate_name(self, obj: InterviewORM) -> str:
        """Get candidate's full name."""
        return obj.application.applicant.user.full_name

    candidate_name.short_description = _("Candidate")
    candidate_name.admin_order_field = "application__applicant__user__first_name"

    def job_title(self, obj: InterviewORM) -> str:
        """Get job post title."""
        return obj.application.post.title

    job_title.short_description = _("Job Title")
    job_title.admin_order_field = "application__post__title"

    def company_name(self, obj: InterviewORM) -> str:
        """Get company name."""
        return obj.company.name

    company_name.short_description = _("Company")
    company_name.admin_order_field = "company__name"

    def status_badge(self, obj: InterviewORM) -> str:
        """Display status with color coding."""
        color_map = {
            InterviewStatusOptions.PENDING: "#ffc107",  # Yellow
            InterviewStatusOptions.SCHEDULED: "#007bff",  # Blue
            InterviewStatusOptions.COMPLETED: "#28a745",  # Green
            InterviewStatusOptions.CANCELED: "#6c757d",  # Gray
        }
        color = color_map.get(obj.status, "#6c757d")
        return format_html(
            (
                '<span style="background-color: {}; color: white; padding: 3px 10px; '
                'border-radius: 3px; font-weight: bold;">{}</span>'
            ),
            color,
            obj.get_status_display(),  # type: ignore[attr-defined]
        )

    status_badge.short_description = _("Status")
    status_badge.admin_order_field = "status"

    def accepted_slot_time(self, obj: InterviewORM) -> str:
        """Display accepted slot time if available."""
        accepted_slot = obj.slots.filter(status=SlotStatus.ACCEPTED).first()
        if accepted_slot:
            return format_html(
                "{}<br><small>{} - {}</small>",
                accepted_slot.start_time.strftime("%b %d, %Y"),
                accepted_slot.start_time.strftime("%I:%M %p"),
                accepted_slot.end_time.strftime("%I:%M %p"),
            )
        return format_html('<span style="color: #6c757d;">Not scheduled</span>')

    accepted_slot_time.short_description = _("Scheduled Time")

    # Admin actions
    @admin.action(description=_("Mark selected interviews as completed"))
    def mark_as_completed(self, request: HttpRequest, queryset: QuerySet[InterviewORM]) -> None:
        """Mark interviews as completed."""
        updated = queryset.update(status=InterviewStatusOptions.COMPLETED)
        self.message_user(request, f"{updated} interview(s) marked as completed.")

    @admin.action(description=_("Mark selected interviews as canceled"))
    def mark_as_canceled(self, request: HttpRequest, queryset: QuerySet[InterviewORM]) -> None:
        """Mark interviews as canceled."""
        updated = queryset.update(status=InterviewStatusOptions.CANCELED)
        self.message_user(request, f"{updated} interview(s) marked as canceled.")


@admin.register(InterviewSlotORM)
class InterviewSlotAdmin(ModelAdmin):
    """Admin interface for Interview Slot model."""

    # List view configuration
    list_display = (
        "id",
        "candidate_name",
        "job_title",
        "time_range",
        "status_badge",
        "proposed_by",
        "slot_type",
        "created_at",
    )
    list_filter = (
        "status",
        "start_time",
        "created_at",
    )
    search_fields = (
        "interview__application__applicant__user__email",
        "interview__application__applicant__user__first_name",
        "interview__application__applicant__user__last_name",
        "interview__application__post__title",
        "proposed_by__email",
        "notes",
    )
    ordering = ("-created_at",)
    list_per_page = 25
    date_hierarchy = "start_time"
    readonly_fields = ("created_at", "updated_at")

    # Detail view configuration
    fieldsets = (
        (
            None,
            {
                "fields": ("interview", "proposed_by", "status"),
            },
        ),
        (
            _("Time Slot"),
            {
                "fields": ("start_time", "end_time"),
            },
        ),
        (
            _("Location Details"),
            {
                "fields": ("location", "meeting_link"),
            },
        ),
        (
            _("Notes"),
            {
                "fields": ("notes",),
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
    autocomplete_fields = ("interview", "proposed_by")

    # Actions
    actions = ["mark_as_accepted", "mark_as_rejected"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[InterviewSlotORM]:
        """Optimize queryset with select_related for related objects."""
        return (
            super()
            .get_queryset(request)
            .select_related(
                "interview__application__applicant__user",
                "interview__application__post",
                "interview__application__post__company",
                "proposed_by",
            )
        )

    def candidate_name(self, obj: InterviewSlotORM) -> str:
        """Get candidate's full name."""
        return obj.interview.application.applicant.user.full_name

    candidate_name.short_description = _("Candidate")
    candidate_name.admin_order_field = "interview__application__applicant__user__first_name"

    def job_title(self, obj: InterviewSlotORM) -> str:
        """Get job post title."""
        return obj.interview.application.post.title

    job_title.short_description = _("Job Title")
    job_title.admin_order_field = "interview__application__post__title"

    def time_range(self, obj: InterviewSlotORM) -> str:
        """Display time range."""
        return format_html(
            "{}<br><small>{} - {}</small>",
            obj.start_time.strftime("%b %d, %Y"),
            obj.start_time.strftime("%I:%M %p"),
            obj.end_time.strftime("%I:%M %p"),
        )

    time_range.short_description = _("Time")

    def status_badge(self, obj: InterviewSlotORM) -> str:
        """Display status with color coding."""
        color_map = {
            SlotStatus.PROPOSED: "#007bff",  # Blue
            SlotStatus.COUNTER_PROPOSED: "#ffc107",  # Yellow
            SlotStatus.ACCEPTED: "#28a745",  # Green
            SlotStatus.REJECTED: "#6c757d",  # Gray
        }
        color = color_map.get(obj.status, "#6c757d")
        return format_html(
            (
                '<span style="background-color: {}; color: white; padding: 3px 10px; '
                'border-radius: 3px; font-weight: bold;">{}</span>'
            ),
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = _("Status")
    status_badge.admin_order_field = "status"

    def slot_type(self, obj: InterviewSlotORM) -> str:
        """Determine if slot is online or in-person."""
        if obj.meeting_link:
            return format_html('<span style="color: #007bff;">🎥 Online</span>')
        if obj.location:
            return format_html('<span style="color: #28a745;">📍 In-Person</span>')
        return "-"

    slot_type.short_description = _("Type")

    # Admin actions
    @admin.action(description=_("Mark selected slots as accepted"))
    def mark_as_accepted(self, request: HttpRequest, queryset: QuerySet[InterviewSlotORM]) -> None:
        """Mark slots as accepted."""
        updated = queryset.update(status=SlotStatus.ACCEPTED)
        self.message_user(request, f"{updated} slot(s) marked as accepted.")

    @admin.action(description=_("Mark selected slots as rejected"))
    def mark_as_rejected(self, request: HttpRequest, queryset: QuerySet[InterviewSlotORM]) -> None:
        """Mark slots as rejected."""
        updated = queryset.update(status=SlotStatus.REJECTED)
        self.message_user(request, f"{updated} slot(s) marked as rejected.")
