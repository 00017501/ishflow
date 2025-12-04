"""Account views."""

from src.routes.web.accounts.views.confirmation import confirm_email_view
from src.routes.web.accounts.views.employees import employees_list_view, invite_employee_view
from src.routes.web.accounts.views.login import login_view
from src.routes.web.accounts.views.logout import logout_view
from src.routes.web.accounts.views.registration import register_view
from src.routes.web.accounts.views.set_password import set_password_view


__all__ = [
    "confirm_email_view",
    "employees_list_view",
    "invite_employee_view",
    "login_view",
    "logout_view",
    "register_view",
    "set_password_view",
]
