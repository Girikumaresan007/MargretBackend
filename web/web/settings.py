"""
Django settings for web project.
"""

from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
from corsheaders.defaults import default_headers

# --------------------------------------------------
# BASE DIR & ENV
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------
# CORE SETTINGS
# --------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    raise Exception("DJANGO_SECRET_KEY is not set in .env file")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    # Django default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "corsheaders",
    "rest_framework",
    "drf_yasg",

    # Local apps
    "login",
    "margret",
    "new_form",
]

# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------
# CORS & CSRF (React frontend)
# --------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers)

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CSRF_COOKIE_HTTPONLY = False

# --------------------------------------------------
# REST FRAMEWORK & JWT
# --------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# --------------------------------------------------
# URLS & TEMPLATES
# --------------------------------------------------
ROOT_URLCONF = "web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "web.wsgi.application"

# --------------------------------------------------
# DATABASE (MySQL)
# --------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "combined_db"),
        "USER": os.getenv("DB_USER", "root"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {
            "auth_plugin": "mysql_native_password",
        },
    }
}

# --------------------------------------------------
# EMAIL (Gmail SMTP)
# --------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------
STATIC_URL = "static/"

# --------------------------------------------------
# DEFAULT PRIMARY KEY
# --------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
