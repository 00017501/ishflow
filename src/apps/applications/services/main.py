"""Application service layer."""

import logging

from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse

from src.apps.applications.models.applications import ApplicationORM, ApplicationStatus
from src.apps.candidates.models import CandidateORM
from src.apps.jobs.models.jobs import JobPostORM


logger = logging.getLogger(__name__)


def create_application(job: JobPostORM, candidate: CandidateORM, cover_letter: str = "") -> ApplicationORM:
    """Create a new job application."""
    return ApplicationORM.objects.create(
        post=job,
        applicant=candidate,
        cover_letter=cover_letter,
    )


def check_already_applied(job: JobPostORM, candidate: CandidateORM) -> bool:
    """Check if candidate has already applied to the job."""
    return ApplicationORM.objects.filter(post=job, applicant=candidate).exists()


def update_application_status(application: ApplicationORM, new_status: ApplicationStatus) -> bool:
    """Update application status and return True if valid."""
    application.status = new_status
    application.save()
    return True


def send_status_update_email(application: ApplicationORM, request: HttpRequest, old_status: ApplicationStatus) -> None:
    """Send email notification for important status changes."""
    important_statuses = [ApplicationStatus.OFFERED, ApplicationStatus.REJECTED]
    new_status = application.status

    if new_status not in important_statuses or new_status == old_status:
        return

    try:
        # Build application URL
        application_url = request.build_absolute_uri(reverse("jobs:my_applications"))

        # Render email template
        html_message = render_to_string(
            "emails/application_status_update.html",
            {
                "candidate_name": application.applicant.user.full_name,
                "job_title": application.post.title,
                "company_name": application.post.company.name,
                "status": new_status,
                "status_display": application.get_status_display(),  # type: ignore
                "application_url": application_url,
            },
        )

        # Send email
        send_mail(
            subject=f"Application Status Update - {application.post.title}",
            message=f"Your application status has been updated to: {application.get_status_display()}",  # type: ignore
            from_email=None,  # Uses DEFAULT_FROM_EMAIL
            recipient_list=[application.applicant.user.email],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Failed to send application status update email: {e}")
        pass


def filter_applications(  # noqa: PLR0913
    applications: QuerySet[ApplicationORM],
    status: str = "",
    job_id: str = "",
    skill: str = "",
    title: str = "",
    min_experience: str = "",
    has_resume: str = "",
) -> QuerySet[ApplicationORM]:
    """Apply filters to applications queryset."""
    if status:
        applications = applications.filter(status=status)

    if job_id:
        try:
            job_pk = int(job_id)
            applications = applications.filter(post_id=job_pk)
        except ValueError:
            pass

    if skill:
        applications = applications.filter(applicant__skills__icontains=skill)

    if title:
        applications = applications.filter(applicant__current_title__icontains=title)

    if min_experience:
        try:
            min_exp_int = int(min_experience)
            applications = applications.filter(applicant__years_of_experience__gte=min_exp_int)
        except ValueError:
            pass

    if has_resume == "yes":
        applications = applications.exclude(applicant__resume__isnull=True).exclude(applicant__resume="")

    return applications
