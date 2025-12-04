"""Job post and application views."""

from src.routes.web.jobs.views.applications import (
    application_status_update_view,
    job_applicants_view,
    job_apply_view,
    my_applications_view,
    received_applications_view,
)
from src.routes.web.jobs.views.jobs import (
    job_create_view,
    job_delete_view,
    job_detail_view,
    job_edit_view,
    job_list_view,
    my_jobs_view,
)


__all__ = [  # noqa: RUF022
    # Application views
    "application_status_update_view",
    "job_applicants_view",
    "job_apply_view",
    "my_applications_view",
    "received_applications_view",
    # Job views
    "job_create_view",
    "job_delete_view",
    "job_detail_view",
    "job_edit_view",
    "job_list_view",
    "my_jobs_view",
]
