"""Management command to create a new Django application with a flexible folder structure."""

from argparse import ArgumentParser
from pathlib import Path

from django.apps import apps
from django.core.management import CommandError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Create a new Django app with a structured folder layout."""

    help: str = "Create a new Django application with a flexible folder structure"

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add command-line arguments."""
        parser.add_argument(
            "app_name",
            type=str,
            help="The name of the new application",
        )

    @staticmethod
    def _touch_file(file_path: str) -> None:
        """Create an empty file at the given path."""
        Path(file_path).touch()

    @staticmethod
    def _create_folder(folder_path: str) -> None:
        """Create a folder and an empty __init__.py inside it."""
        path = Path(folder_path)
        path.mkdir(parents=True, exist_ok=True)
        Command._touch_file(str(path / "__init__.py"))

    @staticmethod
    def _create_app_package(app_name: str) -> None:
        """Create the main app package under src/apps/<app_name>."""
        app_path = Path("src") / "apps" / app_name
        app_path.mkdir(parents=True, exist_ok=True)

        # Core app files
        Command._touch_file(str(app_path / "__init__.py"))
        Command._touch_file(str(app_path / "admin.py"))

        with (app_path / "admin.py").open("w") as f:
            f.write(
                f'"""Admin configuration for the {app_name} app."""\n'
                "\n"
                "from django.contrib import admin  # noqa: F401\n\n"
                "# Register your models here.\n"
            )

        # apps.py with AppConfig
        apps_py_path = app_path / "apps.py"
        with apps_py_path.open("w") as f:
            f.write(
                f"from django.apps import AppConfig\n\n\n"
                f"class {app_name.capitalize()}Config(AppConfig):\n"
                f'    default_auto_field = "django.db.models.BigAutoField"\n'
                f"    name = 'src.apps.{app_name}'\n"
            )

        # Standard subdirectories
        standard_folders = [
            "models",
            "migrations",
            "schemas",
        ]
        interface_folders = [
            "services",
        ]

        for folder in standard_folders:
            Command._create_folder(str(app_path / folder))

        for folder in interface_folders:
            folder_path = app_path / folder
            Command._create_folder(str(folder_path))

    @staticmethod
    def _create_routes_package(app_name: str) -> None:
        """Create the API package under src/routes/api/<app_name>/v1."""
        route_paths = [
            ("api", Path("src") / "routes" / "api" / app_name),
            ("web", Path("src") / "routes" / "web" / app_name),
        ]
        for key, route_path in route_paths:
            Command._create_folder(str(route_path))

            if key == "api":
                # v1 package
                v1_path = route_path / "v1"
                Command._create_folder(str(v1_path))

                # v1 submodules
                Command._create_folder(str(v1_path / "serializers"))
                Command._create_folder(str(v1_path / "views"))
                Command._touch_file(str(v1_path / "urls.py"))

            else:
                # web submodules
                Command._create_folder(str(route_path / "views"))
                Command._touch_file(str(route_path / "urls.py"))

    @staticmethod
    def create_app(app_name: str) -> None:
        """Create the full app structure including API package."""
        Command._create_app_package(app_name)
        Command._create_routes_package(app_name)

    def handle(self, *_args: str, **options: str) -> None:
        """Execute the command."""
        app_name: str = options["app_name"]

        if not app_name:
            raise CommandError("Please provide an app name using the 'app_name' argument.")

        # Validate app name format
        if not app_name.islower() or not app_name.replace("_", "").isalnum():
            raise CommandError("App name must be lowercase alphanumeric with underscores only.")

        # Check if app already exists
        try:
            apps.get_app_config(app_name)
            raise CommandError(f"App with the name '{app_name}' already exists.")
        except LookupError:
            pass  # App does not exist — safe to create

        try:
            self.create_app(app_name)
            self.stdout.write(self.style.SUCCESS(f"Successfully created app '{app_name}' with full structure."))
        except OSError as e:
            raise CommandError(f"Failed to create app structure: {e}") from e
