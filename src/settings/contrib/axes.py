"""Django Axes settings for the project.

Django Axes is a security application that helps protect Django applications
from brute-force login attempts by tracking failed login attempts and locking
out users after a specified number of failures.

Link: https://django-axes.readthedocs.io/en/latest/index.html
"""

# How many failed login attempts are allowed before a user is locked out.
AXES_FAILURE_LIMIT = 5

# The duration (in hours) for which a user is locked out after exceeding the failure limit.
AXES_COOLOFF_TIME = 0.5

# Use custom lockout response (429 error page)
AXES_LOCKOUT_TEMPLATE = "errors/429.html"
AXES_LOCKOUT_URL = "/errors/429/"
