"""Custom model fields for the shared app."""

from collections.abc import Sequence
from typing import Any

from django.core.exceptions import ValidationError
from django.db import models

from src.apps.shared.utils.phonenumber import PhoneNumberValidator


class PhoneNumberField(models.CharField):
    """Custom CharField that validates and formats phone numbers in E.164 format.

    This field automatically:
    - Validates phone numbers using the phonenumbers library
    - Formats valid numbers to E.164 format before saving
    - Stores numbers as strings with a default max length of 20 characters

    Example:
    ```python
        class User(models.Model):
            phone = PhoneNumberField()

        user = User(phone='+1 (234) 567-8900')
        user.save()  # Stores as '+12345678900'
    ```
    """

    default_max_length = 20
    description = "Phone number field that validates and formats to E.164"

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        # Set default max_length for phone numbers if not specified
        kwargs.setdefault("max_length", self.default_max_length)
        super().__init__(*args, **kwargs)

    def deconstruct(self) -> tuple[str, str, Sequence[Any], dict[str, Any]]:
        """Return enough information to recreate the field for migrations."""
        name, path, args, kwargs = super().deconstruct()
        # Remove max_length from kwargs if it's the default value
        if kwargs.get("max_length") == self.default_max_length:
            del kwargs["max_length"]
        return name, path, args, kwargs

    def validate(self, value: str, model_instance: models.Model) -> None:
        """Validate that the phone number is valid."""
        super().validate(value, model_instance)

        if value and not PhoneNumberValidator.is_valid(value):
            raise ValidationError(
                f"'{value}' is not a valid phone number. " "Please use international format (e.g., +1234567890).",
                code="invalid_phone_number",
                params={"value": value},
            )

    def pre_save(self, model_instance: models.Model, add: bool) -> str | None:  # noqa: ARG002
        """Format the phone number to E.164 before saving."""
        value = getattr(model_instance, self.attname, None)

        if value:
            # Format to E.164
            formatted = PhoneNumberValidator.format_e164(value)
            if formatted:
                setattr(model_instance, self.attname, formatted)
                return formatted

        return value

    def formfield(self, **kwargs: Any) -> models.Field | None:  # noqa: ANN401
        """Return a form field for this model field."""
        defaults: dict = {"max_length": self.max_length}
        defaults.update(kwargs)
        return super().formfield(**defaults)  # type: ignore


class CommaSeparatedCharField(models.CharField):
    """Custom CharField that stores a list of strings as comma-separated values.

    This field automatically:
    - Converts Python lists to comma-separated strings for database storage
    - Converts comma-separated strings back to Python lists when retrieved
    - Strips whitespace from each item
    - Filters out empty strings

    Example:
    ```python
        class Product(models.Model):
            tags = CommaSeparatedCharField(max_length=200)

        product = Product(tags=['python', 'django', 'web'])
        product.save()  # Stores as 'python,django,web'
        print(product.tags)  # ['python', 'django', 'web']
    ```
    """

    description = "Comma-separated list stored as CharField"

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        self.separator = kwargs.pop("separator", ",")
        super().__init__(*args, **kwargs)

    def deconstruct(self) -> tuple[str, str, Sequence[Any], dict[str, Any]]:
        """Return enough information to recreate the field for migrations."""
        name, path, args, kwargs = super().deconstruct()
        if self.separator != ",":
            kwargs["separator"] = self.separator
        return name, path, args, kwargs

    def from_db_value(
        self, value: str | None, expression: Any, connection: Any  # noqa: ANN401, ARG002
    ) -> list[str] | None:
        """Convert database value to Python list."""
        if value is None:
            return None
        if value == "":
            return []
        return [item.strip() for item in value.split(self.separator) if item.strip()]

    def to_python(self, value: Any) -> list[str] | None:  # noqa: ANN401
        """Convert value to Python list."""
        if value is None:
            return None
        if isinstance(value, list):
            return value
        if value == "":
            return []
        return [item.strip() for item in value.split(self.separator) if item.strip()]

    def get_prep_value(self, value: list[str] | str | None) -> str | None:
        """Convert Python list to database string."""
        if value is None:
            return None
        if isinstance(value, str):
            # Already a string, just return it
            return value
        if isinstance(value, list):
            # Filter out empty strings and join
            filtered = [str(item).strip() for item in value if str(item).strip()]
            return self.separator.join(filtered)
        return str(value)

    def value_to_string(self, obj: models.Model) -> str:
        """Serialize the field value for serialization."""
        value = self.value_from_object(obj)
        return self.get_prep_value(value) or ""
