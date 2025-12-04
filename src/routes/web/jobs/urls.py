"""Job URL patterns."""

from django.urls import path

from src.routes.web.jobs import views


urlpatterns = [
    path("", views.job_list_view, name="list"),
    path("<int:pk>/", views.job_detail_view, name="detail"),
    path("my-jobs/", views.my_jobs_view, name="my_jobs"),
    path("create/", views.job_create_view, name="create"),
    path("<int:pk>/edit/", views.job_edit_view, name="edit"),
    path("<int:pk>/delete/", views.job_delete_view, name="delete"),
    # Application URLs
    path("<int:pk>/apply/", views.job_apply_view, name="apply"),
    path("my-applications/", views.my_applications_view, name="my_applications"),
    path("received-applications/", views.received_applications_view, name="received_applications"),
    path("<int:pk>/applicants/", views.job_applicants_view, name="applicants"),
    path(
        "applications/<int:pk>/update-status/", views.application_status_update_view, name="application_status_update"
    ),
]
