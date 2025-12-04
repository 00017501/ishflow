"""Set password form."""

from django import forms
from django.core.exceptions import ValidationError


class SetPasswordForm(forms.Form):
    """Form for setting password after invitation."""

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}),
        label="Password",
        min_length=8,
        help_text="Password must be at least 8 characters long",
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"}),
        label="Confirm Password",
    )

    def clean_password_confirm(self) -> str | None:
        """Validate that the two password entries match."""
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("The two password fields didn't match.")

        return password_confirm
