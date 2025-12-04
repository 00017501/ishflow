"""Django management command to create test users for development."""

from django.core.management import BaseCommand
from pydantic import BaseModel

from src.apps.accounts.models import UserORM


class UserData(BaseModel):
    """Type definition for user data dictionary."""

    email: str
    password: str


class Command(BaseCommand):
    """Management command to create test superuser accounts.

    This command creates predefined test users for development and testing purposes.
    Each user is created as an active superuser with staff privileges.
    """

    help = "Create test superuser accounts for development"

    def handle(self, *_args: str, **_options: bool | str) -> None:
        """Execute the command to create test users.

        Args:
            _args: Positional arguments (unused, prefixed with underscore).
            _options: Command options (unused, prefixed with underscore).

        Returns:
            None
        """
        self.stdout.write(self.style.NOTICE("Creating test users..."))

        users = self._get_test_users_data()
        created_count = 0

        for user_data in users:
            if UserORM.objects.filter(email=user_data.email).exists():
                self.stdout.write(self.style.WARNING(f"User {user_data.email} already exists, skipping"))
                continue

            self._create_user(user_data)
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Created user: {user_data.email}"))

        if created_count > 0:
            self.stdout.write(self.style.SUCCESS(f"Successfully created {created_count} test user(s)"))
        else:
            self.stdout.write(self.style.NOTICE("No new users created (all already exist)"))

    def _create_user(self, user_data: UserData) -> UserORM:
        """Create and save a superuser with the provided data.

        Args:
            user_data: Dictionary containing email and password for the user.

        Returns:
            The created user instance.
        """
        user = UserORM(
            email=user_data.email,
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(user_data.password)
        user.save()
        return user

    def _get_test_users_data(self) -> list[UserData]:
        """Get the list of test users to create.

        Returns:
            List of dictionaries containing email and password for each test user.
        """
        return [
            UserData(
                **{
                    "email": "admin@test.com",
                    "password": "admin",
                }
            ),
            UserData(
                **{
                    "email": "admin1@test.com",
                    "password": "183376e22238164f",
                }
            ),
            UserData(
                **{
                    "email": "admin2@test.com",
                    "password": "bxeilqi5Kkc=",
                }
            ),
        ]
