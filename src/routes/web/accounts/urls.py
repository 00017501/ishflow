"""Account URL patterns."""

from django.urls import path

from src.routes.web.accounts import views
from src.routes.web.accounts.views import profile as profile_views


urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Employee invitation and email confirmation
    path("confirm-email/<str:uidb64>/<str:token>/", views.confirm_email_view, name="confirm_email"),
    path("employees/", views.employees_list_view, name="employees_list"),
    path("employees/invite/", views.invite_employee_view, name="invite_employee"),
    path("set-password/<str:uidb64>/<str:token>/", views.set_password_view, name="set_password"),
    # Profile management
    path("profile/", profile_views.profile_view, name="profile"),
    path("profile/candidate/", profile_views.candidate_profile_view, name="candidate_profile"),
    path("profile/company/", profile_views.company_profile_view, name="company_profile"),
]
