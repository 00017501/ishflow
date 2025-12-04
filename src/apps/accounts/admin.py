"""Admin configuration for the accounts app."""

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin, UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from src.apps.accounts.models.users import UserORM


@admin.register(UserORM)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """Admin interface for User model."""

    # List view configuration
    list_display = (
        "email",
        "first_name",
        "last_name",
        "type",
        "company",
        "invitation_status",
        "has_confirmed_email",
        "is_active",
        "is_staff",
        "created_at",
    )
    list_filter = (
        "type",
        "invitation_status",
        "has_confirmed_email",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
    )
    search_fields = ("email", "first_name", "last_name", "phone_number")
    ordering = ("-created_at",)
    list_per_page = 25
    date_hierarchy = "created_at"

    # Detail view configuration
    fieldsets = (
        (
            None,
            {
                "fields": ("email", "password"),
            },
        ),
        (
            _("Personal Info"),
            {
                "fields": ("first_name", "last_name", "phone_number"),
            },
        ),
        (
            _("Company & Type"),
            {
                "fields": ("company", "type"),
            },
        ),
        (
            _("Status"),
            {
                "fields": ("invitation_status", "has_confirmed_email", "is_active"),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important Dates"),
            {
                "fields": ("last_login", "created_at", "updated_at"),
            },
        ),
    )

    # Add user form configuration
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "type",
                    "company",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at", "last_login")
    filter_horizontal = ("groups", "user_permissions")

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Optimize queryset with select_related for foreign keys."""
        qs = super().get_queryset(request)
        return qs.select_related("company")


# Unregister the default Group admin
admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """Admin interface for Group model with Unfold styling."""

    list_display = ("name", "get_permissions_count")
    search_fields = ("name",)
    filter_horizontal = ("permissions",)
    ordering = ("name",)

    def get_permissions_count(self, obj: Group) -> int:
        """Return the count of permissions in this group."""
        return obj.permissions.count()

    get_permissions_count.short_description = "Perms Count"


@admin.register(Permission)
class PermissionAdmin(ModelAdmin):
    """Admin interface for Permission model."""

    list_display = ("name", "content_type", "codename")
    list_filter = ("content_type",)
    search_fields = ("name", "codename")
    ordering = ("content_type", "codename")
    list_per_page = 50

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Optimize queryset with select_related for content_type."""
        qs = super().get_queryset(request)
        return qs.select_related("content_type")
