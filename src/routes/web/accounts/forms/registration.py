"""Forms for account registration and authentication."""

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from src.apps.accounts.models.users import UserORM, UserTypeOptions
from src.apps.accounts.schemas.registration import UserValidatedDataSchema
from src.apps.accounts.services import registration as services
from src.apps.shared.utils.phonenumber import PhoneNumberValidator


class RegistrationForm(forms.Form):
    """Base registration form for all users."""

    # User type selection
    user_type = forms.ChoiceField(
        choices=UserTypeOptions.choices,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        initial=UserTypeOptions.CANDIDATE,
        label="I am a",
    )

    # User fields
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "your@email.com"}),
        label="Email Address",
    )

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

    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "+998901234567"}),
        label="Phone Number",
        help_text="Optional: Format +998901234567",
    )

    # Company fields (for employers only)
    company_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Company Name",
                "data-employer-field": "true",
            }
        ),
        label="Company Name",
    )

    company_description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Brief description of your company",
                "data-employer-field": "true",
            }
        ),
        label="Company Description",
    )

    company_website = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": "https://www.example.com",
                "data-employer-field": "true",
            }
        ),
        label="Company Website",
    )

    company_logo = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": "image/*",
                "data-employer-field": "true",
            }
        ),
        label="Company Logo",
        help_text="Optional: Upload company logo (max 5MB)",
    )

    # Terms acceptance
    accept_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="I agree to the Terms and Conditions",
    )

    def clean_email(self) -> str | None:
        """Validate that the email is not already in use."""
        email = self.cleaned_data.get("email")
        if email and UserORM.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_phone_number(self) -> str | None:
        """Validate phone number format using PhoneNumberValidator."""
        phone_number = self.cleaned_data.get("phone_number")

        if phone_number:
            # Validate phone number format
            if not PhoneNumberValidator.is_valid(phone_number):
                raise ValidationError(
                    f"'{phone_number}' is not a valid phone number. "
                    "Please use international format (e.g., +998901234567)."
                )

            # Format to E.164 before saving
            formatted = PhoneNumberValidator.format_e164(phone_number)
            if formatted:
                return formatted

            raise ValidationError("Unable to format phone number. Please check the format.")

        return phone_number

    def clean_company_website(self) -> str | None:
        """Validate company website URL format."""
        website = self.cleaned_data.get("company_website")

        # Ensure URL has a scheme
        if website and not website.startswith(("http://", "https://")):
            raise ValidationError("Website URL must start with http:// or https://")

        return website

    def clean_company_logo(self) -> None:
        """Validate company logo file size and type."""
        logo = self.cleaned_data.get("company_logo")

        if logo and logo.size > 5 * 1024 * 1024:
            raise ValidationError("Logo file size must not exceed 5MB.")

        return logo

    def clean_password(self) -> str | None:
        """Validate password using Django's password validators."""
        password = self.cleaned_data.get("password")

        if password:
            validate_password(password, user=None)

        return password

    def clean_password_confirm(self) -> str | None:
        """Validate that the two password entries match."""
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("The two password fields didn't match.")

        return password_confirm

    def clean(self) -> dict:
        """Additional validation for employer-specific fields."""
        cleaned_data: dict = super().clean()  # type: ignore
        user_type = cleaned_data.get("user_type")

        # If employer, company name is required
        if user_type == UserTypeOptions.EMPLOYER:
            company_name = cleaned_data.get("company_name")
            if not company_name:
                self.add_error("company_name", "Company name is required for employers.")

        return cleaned_data

    def save(self) -> UserORM:
        """Create user and optionally company."""
        return services.create_user_flow(data=UserValidatedDataSchema(**self.cleaned_data))  # type: ignore


class LoginForm(forms.Form):
    """Login form for users."""

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "your@email.com",
                "autofocus": True,
            }
        ),
        label="Email Address",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}),
        label="Password",
    )

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Remember me",
    )
