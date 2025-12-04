"""Django Cachalot settings.

Cachalot is a caching framework for Django ORM queries that helps improve
the performance of database operations by caching the results of queries.

Link: https://django-cachalot.readthedocs.io/en/latest/
"""

# I got familiar with this package through this video: https://youtu.be/mH2XWYBvG_0?si=yo60PDS5QQYQv8gG

CACHALOT_ENABLED = True

# Number of seconds for cachalot to invalidate cached queries
CACHALOT_TIMEOUT = 60 * 60 * 24 * 3  # 3 days
