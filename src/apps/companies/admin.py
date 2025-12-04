"""Admin configuration for the companies app."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from src.apps.companies.models.companies import CompanyORM


@admin.register(CompanyORM)
class CompanyAdmin(ModelAdmin):
    """Admin interface for Company model."""

    # List view configuration
    list_display = (
        "name",
        "owner",
        "website",
        "has_logo",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "owner__email", "owner__first_name", "owner__last_name", "description")
    ordering = ("-created_at",)
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")

    # Detail view configuration
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "owner"),
            },
        ),
        (
            _("Details"),
            {
                "fields": ("description", "website", "logo"),
            },
        ),
        (
            _("Metadata"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    # Form configuration
    autocomplete_fields = ("owner",)

    def has_logo(self, obj: CompanyORM) -> bool:
        """Check if company has a logo."""
        return bool(obj.logo)

    has_logo.boolean = True
    has_logo.short_description = _("Has Logo")
