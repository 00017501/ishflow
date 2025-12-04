"""Forms for employee invitation."""

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()


class InviteEmployeeForm(forms.Form):
    """Form for inviting employees to a company."""

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "John"}),
        label="First Name",
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Doe"}),
        label="Last Name",
    )

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "employee@example.com"}),
        label="Email Address",
    )

    def clean_email(self) -> str | None:
        """Validate that the email is not already in use."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email
