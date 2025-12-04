"""Job views."""

from src.routes.api.jobs.v1.views.jobs import (
    JobCreateView,
    JobDeleteView,
    JobDetailView,
    JobListView,
    JobUpdateView,
    MyJobsView,
)


__all__ = [  # noqa: RUF022
    "JobListView",
    "JobDetailView",
    "JobCreateView",
    "JobUpdateView",
    "JobDeleteView",
    "MyJobsView",
]
