"""Interview scheduling URL patterns."""

from django.urls import path

from src.routes.web.interviews import views


urlpatterns = [
    path("application/<int:application_pk>/propose/", views.propose_interview_slot_view, name="propose_slot"),
    path("application/<int:application_pk>/view-slots/", views.view_interview_slots_view, name="view_slots"),
    path("application/<int:application_pk>/counter-propose/", views.counter_propose_slot_view, name="counter_propose"),
    path("slot/<int:slot_pk>/accept/", views.accept_interview_slot_view, name="accept_slot"),
    path("slot/<int:slot_pk>/accept-counter/", views.accept_counter_proposal_view, name="accept_counter_proposal"),
    path("slot/<int:slot_pk>/reject/", views.reject_interview_slot_view, name="reject_slot"),
]
