"""Django Unfold settings contribution.

Django Unfold is a powerful admin interface for Django applications.
Link: https://unfoldadmin.com/docs/installation/quickstart/
"""

# Got familiar with Unfold through: https://youtu.be/kkxAVubUOj8?si=EhVjpjIT36KCawyA

from src.settings.environment import env


BASE_APP_URL = "https://ishflow.uz" if env("ISHFLOW_ENVIRONMENT") == "prod" else "http://localhost:8000"

UNFOLD = {
    "SITE_TITLE": "Ishflow Admin",
    "SITE_HEADER": "Ishflow Administration",
    "SITE_SUBHEADER": "Recruitment & Talent Management Platform",
    "SITE_DROPDOWN": [
        {
            "icon": "dashboard",
            "title": "Dashboard",
            "link": f"{BASE_APP_URL}/admin/",
        },
        {
            "icon": "api",
            "title": "API Documentation",
            "link": f"{BASE_APP_URL}/api/v1/docs/",
        },
        {
            "icon": "public",
            "title": "Visit Site",
            "link": BASE_APP_URL,
        },
    ],
    "SITE_URL": "/",
    "SITE_SYMBOL": "work",  # Material icon for job/recruitment theme
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": "https://cdn-icons-png.freepik.com/256/14993/14993311.png?semt=ais_white_label",
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "BORDER_RADIUS": "8px",
    "COLORS": {
        "base": {
            "50": "248 250 252",
            "100": "241 245 249",
            "200": "226 232 240",
            "300": "203 213 225",
            "400": "148 163 184",
            "500": "100 116 139",
            "600": "71 85 105",
            "700": "51 65 85",
            "800": "30 41 59",
            "900": "15 23 42",
            "950": "3 7 18",
        },
        "primary": {
            "50": "240 249 255",
            "100": "224 242 254",
            "200": "186 230 253",
            "300": "125 211 252",
            "400": "56 189 248",
            "500": "14 165 233",
            "600": "2 132 199",
            "700": "3 105 161",
            "800": "7 89 133",
            "900": "12 74 110",
            "950": "8 47 73",
        },
        "font": {
            "subtle-light": "148 163 184",
            "subtle-dark": "148 163 184",
            "default-light": "71 85 105",
            "default-dark": "203 213 225",
            "important-light": "15 23 42",
            "important-dark": "241 245 249",
        },
    },
    "EXTENSIONS": {},
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "User Management",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "people",
                        "link": lambda request: f"{BASE_APP_URL}/admin/accounts/userorm/",  # noqa: ARG005
                    },
                    {
                        "title": "Groups",
                        "icon": "group",
                        "link": lambda request: f"{BASE_APP_URL}/admin/auth/group/",  # noqa: ARG005
                    },
                    {
                        "title": "Permissions",
                        "icon": "lock",
                        "link": lambda request: f"{BASE_APP_URL}/admin/auth/permission/",  # noqa: ARG005
                    },
                ],
            },
            {
                "title": "Companies & Jobs",
                "separator": True,
                "items": [
                    {
                        "title": "Companies",
                        "icon": "business",
                        "link": lambda request: f"{BASE_APP_URL}/admin/companies/companyorm/",  # noqa: ARG005
                    },
                    {
                        "title": "Job Posts",
                        "icon": "work",
                        "link": lambda request: f"{BASE_APP_URL}/admin/jobs/jobpostorm/",  # noqa: ARG005
                    },
                ],
            },
            {
                "title": "Recruitment",
                "separator": True,
                "items": [
                    {
                        "title": "Candidates",
                        "icon": "badge",
                        "link": lambda request: f"{BASE_APP_URL}/admin/candidates/candidateorm/",  # noqa: ARG005
                    },
                    {
                        "title": "Applications",
                        "icon": "assignment",
                        "link": lambda request: f"{BASE_APP_URL}/admin/applications/applicationorm/",  # noqa: ARG005
                    },
                    {
                        "title": "Interviews",
                        "icon": "event",
                        "link": lambda request: f"{BASE_APP_URL}/admin/interviews/intervieworm/",  # noqa: ARG005
                    },
                ],
            },
        ],
    },
    "TABS": [],
}
