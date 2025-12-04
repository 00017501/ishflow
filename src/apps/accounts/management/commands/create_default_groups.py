"""Django management command to create default groups with permissions."""

import json

from typing import Any

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from pydantic import BaseModel, Field, ValidationError


class GroupSchema(BaseModel):
    """Pydantic schema for group data validation."""

    name: str = Field(..., min_length=1, description="Name of the group")
    permissions: list[str] = Field(
        default_factory=list, description="List of permissions in 'app_label.codename' format"
    )


class GroupsFixture(BaseModel):
    """Pydantic schema for the entire groups fixture."""

    groups: list[GroupSchema] = Field(default_factory=list, description="List of groups")


class Command(BaseCommand):
    """Management command to create default groups from JSON fixture."""

    help = "Create default groups with permissions from groups.json fixture"
    _FIXTURE_PATH = settings.BASE_DIR / "apps" / "accounts" / "fixtures" / "groups.json"

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: ANN401, ARG002
        """Execute the command."""
        if not self._FIXTURE_PATH.exists():
            raise CommandError(f"Fixture file not found: {self._FIXTURE_PATH}")

        # Load and validate JSON using Pydantic
        try:

            with self._FIXTURE_PATH.open("r") as f:
                raw_data = json.load(f)
                data = GroupsFixture(**raw_data)

                groups_created = 0
                groups_updated = 0
                permissions_assigned = 0

                for group_schema in data.groups:
                    group_name = group_schema.name
                    permission_strings = group_schema.permissions

                    # Get or create the group
                    group, created = Group.objects.get_or_create(name=group_name)

                    if created:
                        groups_created += 1
                        self.stdout.write(self.style.SUCCESS(f"✓ Created group: {group_name}"))
                    else:
                        groups_updated += 1
                        self.stdout.write(self.style.WARNING(f"○ Group already exists: {group_name}"))

                    # Clear existing permissions to ensure clean state
                    group.permissions.clear()

                    # Process permissions
                    for perm_string in permission_strings:
                        permission = self._get_permission(perm_string)

                        if permission:
                            group.permissions.add(permission)
                            permissions_assigned += 1
                            self.stdout.write(f"  + Added permission: {perm_string}")
                        else:
                            self.stdout.write(self.style.WARNING(f"  ! Permission not found: {perm_string}"))

                # Summary
                self.stdout.write("\n" + "=" * 50)
                self.stdout.write(self.style.SUCCESS(f"Groups created: {groups_created}"))
                self.stdout.write(self.style.WARNING(f"Groups updated: {groups_updated}"))
                self.stdout.write(self.style.SUCCESS(f"Permissions assigned: {permissions_assigned}"))
                self.stdout.write("=" * 50)

        except ValidationError as e:
            raise CommandError(f"Invalid fixture data: {e}") from e
        except json.JSONDecodeError as e:
            raise CommandError(f"Invalid JSON in fixture file: {e}") from e
        except Exception as e:
            raise CommandError(f"Error loading fixture file: {e}") from e

    def _get_permission(self, perm_string: str) -> Permission | None:
        """Get a permission object from a string like 'app_label.codename'.

        Args:
            perm_string: Permission string in format 'app_label.codename'

        Returns:
            Permission object or None if not found
        """
        try:
            app_label, codename = perm_string.split(".", 1)
        except ValueError:
            self.stdout.write(
                self.style.ERROR(f"Invalid permission format '{perm_string}'. Expected 'app_label.codename'")
            )
            return None

        try:
            # Try to find permission by app_label and codename
            content_type = ContentType.objects.filter(app_label=app_label).first()

            if not content_type:
                return None

            return Permission.objects.filter(content_type__app_label=app_label, codename=codename).first()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error finding permission '{perm_string}': {e}"))
            return None
