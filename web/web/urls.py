"""
URL configuration for the project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView

# --------------------------------------------------
# SWAGGER CONFIG (ONE SINGLE SCHEMA)
# --------------------------------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="Combined Project API",
        default_version="v1",
        description="Margret + New Form + Admin Authentication APIs",
        contact=openapi.Contact(email="admin@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# --------------------------------------------------
# URL PATTERNS
# --------------------------------------------------
urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # App URLs
    path("margret/", include("margret.urls")),
    path("new_form/", include("new_form.urls")),

    # Auth / API URLs
    path("api/", include("login.urls")),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Swagger Docs
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
]
