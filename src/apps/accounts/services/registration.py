"""Services for user registration and email notifications."""

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from src.apps.accounts.models.users import InvitationStatusOptions, UserORM, UserTypeOptions
from src.apps.accounts.schemas.registration import EmployeeInvitationDataSchema, UserValidatedDataSchema
from src.apps.accounts.services.tokens import account_activation_token
from src.apps.companies.models.companies import CompanyORM


def send_confirmation_email(request: HttpRequest, user: UserORM) -> None:
    """Send email confirmation to user."""
    current_site = get_current_site(request)
    subject = "Activate Your Ishflow Account"

    # Generate confirmation token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    # Build confirmation URL
    confirmation_url = request.build_absolute_uri(
        reverse("accounts:confirm_email", kwargs={"uidb64": uid, "token": token})
    )

    # Render email template
    message = render_to_string(
        "emails/account_confirmation.html",
        {
            "user": user,
            "domain": current_site.domain,
            "confirmation_url": confirmation_url,
        },
    )

    # Send email
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = "html"
    email.send()


def send_invitation_email(request: HttpRequest, user: UserORM, company: CompanyORM) -> None:
    """Send invitation email to new employee."""
    current_site = get_current_site(request)
    subject = f"Invitation to Join {company.name} on Ishflow"

    # Generate invitation token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    # Build set password URL
    set_password_url = request.build_absolute_uri(
        reverse("accounts:set_password", kwargs={"uidb64": uid, "token": token})
    )

    # Render email template
    message = render_to_string(
        "emails/employee_invitation.html",
        {
            "user": user,
            "company": company,
            "domain": current_site.domain,
            "set_password_url": set_password_url,
        },
    )

    # Send email
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = "html"
    email.send()


def create_user_flow(data: UserValidatedDataSchema) -> UserORM:
    """Create user and associated company if employer."""
    user_type = data.user_type

    with transaction.atomic():
        # Create user
        user = UserORM.objects.create_user(
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            phone_number=data.phone_number,  # type: ignore
            type=user_type,
            is_active=True,
            # Will be set to True after email confirmation
            has_confirmed_email=False,
        )

        # If employer, create company
        if user_type == UserTypeOptions.EMPLOYER:
            company = CompanyORM.objects.create(
                owner=user,
                name=data.company_name,
                description=data.company_description or None,
                website=data.company_website or None,
                logo=data.company_logo or None,
            )

            # Link user to company
            user.company = company
            user.save(update_fields=["company"])

        return user


def create_employee_user_flow(data: EmployeeInvitationDataSchema, request: HttpRequest, company: CompanyORM) -> UserORM:
    """Create employee user associated with a company."""
    with transaction.atomic():
        user = UserORM.objects.create(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            type=UserTypeOptions.EMPLOYER,
            company=company,
            # Will be activated upon invitation acceptance
            invitation_status=InvitationStatusOptions.INVITED,
            is_active=False,
            has_confirmed_email=False,
        )

        send_invitation_email(request, user, company)

        return user
