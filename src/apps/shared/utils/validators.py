"""Custom validators for Django models and forms."""

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible


@deconstructible
class FileSizeValidator:
    """Validator that checks file size.

    Example:
        class MyModel(models.Model):
            document = models.FileField(
                validators=[FileSizeValidator(max_size_mb=10)]
            )
    """

    def __init__(self, max_size_mb: int = 5) -> None:
        """Initialize validator with max file size in megabytes.

        Args:
            max_size_mb: Maximum file size in megabytes (default: 5MB)
        """
        self.max_size_mb = max_size_mb
        self.max_size_bytes = max_size_mb * 1024 * 1024

    def __call__(self, file: UploadedFile) -> None:
        """Validate the file size.

        Args:
            file: The uploaded file to validate

        Raises:
            ValidationError: If file size exceeds the maximum
        """
        if file.size and file.size > self.max_size_bytes:
            raise ValidationError(
                f"File size must not exceed {self.max_size_mb}MB. "
                f"Current file size is {filesizeformat(file.size)}.",
                code="file_too_large",
                params={"max_size": self.max_size_mb, "current_size": filesizeformat(file.size)},
            )

    def __eq__(self, other: object) -> bool:
        """Check equality based on max_size_mb."""
        if not isinstance(other, FileSizeValidator):
            return NotImplemented
        return self.max_size_mb == other.max_size_mb

    def __hash__(self) -> int:
        """Return hash based on max_size_mb."""
        return hash(self.max_size_mb)
