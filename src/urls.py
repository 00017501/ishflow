"""URL configuration for src project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from src.routes.web.accounts import urls as accounts_urls
from src.routes.web.errors import urls as errors_urls
from src.routes.web.home import urls as home_urls
from src.routes.web.interviews import urls as interviews_urls
from src.routes.web.jobs import urls as jobs_urls


API_PREFIX = "api"
SWAGGER_PREFIX = "swagger"
REDOC_PREFIX = "docs"

web_urlpatterns = [
    path("", include((home_urls, "home"), namespace="home")),
    path("accounts/", include((accounts_urls, "accounts"), namespace="accounts")),
    path("jobs/", include((jobs_urls, "jobs"), namespace="jobs")),
    path("interviews/", include((interviews_urls, "interviews"), namespace="interviews")),
    path("errors/", include((errors_urls, "errors"), namespace="errors")),
]

api_v1_urlpatterns = [
    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        f"{REDOC_PREFIX}/",
        SpectacularRedocView.as_view(url_name="v1:schema"),
        name="v1-schema-redoc",
    ),
    path(
        "accounts/",
        include(("src.routes.api.accounts.v1.urls", "accounts"), namespace="accounts"),
    ),
    path(
        "jobs/",
        include(("src.routes.api.jobs.v1.urls", "jobs"), namespace="jobs"),
    ),
]

# Add Swagger UI only in non-production environments
if settings.ENVIRONMENT != "production":
    api_v1_urlpatterns += [
        path(
            f"{SWAGGER_PREFIX}/",
            SpectacularSwaggerView.as_view(url_name="v1:schema"),
            name="v1-schema-swagger-ui",
        ),
    ]


security_txt_urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="shared/robots.txt",
            content_type="text/plain",
        ),
    ),
    path(
        "humans.txt",
        TemplateView.as_view(
            template_name="shared/humans.txt",
            content_type="text/plain",
        ),
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{API_PREFIX}/v1/", include((api_v1_urlpatterns, "api"), namespace="v1")),
    *web_urlpatterns,
    *security_txt_urlpatterns,
]

# Custom error handlers
handler403 = "src.routes.web.errors.views.forbidden_view"
handler404 = "src.routes.web.errors.views.page_not_found_view"
handler429 = "src.routes.web.errors.views.too_many_requests_view"
handler500 = "src.routes.web.errors.views.server_error_view"

# Serve static and media files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files in non-production environments
if settings.MEDIA_URL and settings.ENVIRONMENT != "production":
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug toolbar URLs
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
