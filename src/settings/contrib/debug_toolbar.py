"""Django Debug Toolbar settings.

Django Debug Toolbar is a configurable set of panels that display various
debugging information about the current request/response.

Link: https://django-debug-toolbar.readthedocs.io/en/latest/
"""

# I used it to find and optimize slow database queries and view rendering times.
import socket

from django.http import HttpRequest

from src.settings.environment import env


# Configuration is inspired from: https://github.com/wemake-services/wemake-django-template
if env.bool("ISHFLOW_DEBUG", default=False):  # type: ignore
    # https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
    try:  # This might fail on some OS
        INTERNAL_IPS = ["{}.1".format(ip[: ip.rfind(".")]) for ip in socket.gethostbyname_ex(socket.gethostname())[2]]
    except OSError:  # pragma: no cover
        INTERNAL_IPS = []
    INTERNAL_IPS += ["127.0.0.1", "10.0.2.2"]

    def _custom_show_toolbar(request: HttpRequest) -> bool:  # noqa
        """Only show the debug toolbar in non-production environments."""
        return env("ISHFLOW_DEBUG") is True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": ("src.settings.contrib.debug_toolbar._custom_show_toolbar"),
    }
