"""URL configuration for the jobs app."""

from django.urls import path

from src.routes.api.jobs.v1.views import (
    JobCreateView,
    JobDeleteView,
    JobDetailView,
    JobListView,
    JobUpdateView,
    MyJobsView,
)


urlpatterns = [
    # Public endpoints
    path("", JobListView.as_view(), name="job-list"),
    path("<int:pk>/", JobDetailView.as_view(), name="job-detail"),
    # Employer endpoints
    path("my-jobs/", MyJobsView.as_view(), name="my-jobs"),
    path("create/", JobCreateView.as_view(), name="job-create"),
    path("<int:pk>/update/", JobUpdateView.as_view(), name="job-update"),
    path("<int:pk>/delete/", JobDeleteView.as_view(), name="job-delete"),
]
