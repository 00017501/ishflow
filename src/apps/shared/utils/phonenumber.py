"""Phone number validation utilities using the phonenumbers library."""

import phonenumbers

from phonenumbers.phonenumberutil import NumberParseException


class PhoneNumberValidator:
    """Utility class for validating and formatting phone numbers."""

    @staticmethod
    def is_valid(number: str) -> bool:
        """Check if the phone number is valid (expects international format)."""
        try:
            parsed = phonenumbers.parse(number, None)
            return phonenumbers.is_valid_number(parsed)
        except NumberParseException:
            return False

    @staticmethod
    def format_e164(number: str) -> str | None:
        """Format the phone number in E.164 format if valid.

        Example:
            +1234567890 -> +1234567890
            123-456-7890 -> +11234567890 (if valid in default region)
        """
        try:
            parsed = phonenumbers.parse(number, None)
            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except NumberParseException:
            pass
        return None

    @staticmethod
    def get_region_code(number: str) -> str | None:
        """Get the region code for a valid phone number."""
        try:
            parsed = phonenumbers.parse(number, None)
            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.region_code_for_number(parsed)
        except NumberParseException:
            pass
        return None
