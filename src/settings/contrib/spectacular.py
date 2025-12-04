"""DRF Spectacular settings for the project.

DRF Spectacular is a library that generates OpenAPI 3.0 documentation
for Django REST Framework APIs. It provides a way to create and maintain
up-to-date API documentation that is compliant with the OpenAPI specification.

Link: https://drf-spectacular.readthedocs.io/en/latest/
"""

SPECTACULAR_SETTINGS = {
    "TITLE": "API DOCS | ISHFLOW",
    "DESCRIPTION": "API documentation for ISHFLOW API service.",
    "VERSION": "0.1.0",
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_DIST": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "DISABLE_ERRORS_AND_WARNINGS": True,
    "SWAGGER_UI_FAVICON_HREF": "https://cdn-icons-png.flaticon.com/512/2164/2164832.png",
}
