"""
Django settings for config project.
Deployment-ready version (PythonAnywhere + SQLite by default)
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------
# SECURITY
# --------------------------------------------------------------------
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-replace-this-key-in-production"
)
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# PythonAnywhere domain and localhost for local testing
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    os.getenv("PYTHONANYWHERE_HOST", "mangi.pythonanywhere.com"),
]

# --------------------------------------------------------------------
# APPLICATIONS
# --------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "countries",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "currency.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "currency.wsgi.application"

# --------------------------------------------------------------------
# DATABASE CONFIG
# --------------------------------------------------------------------
USE_SQLITE = os.getenv("USE_SQLITE", "True").lower() == "true"

if USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "3306"),
        }
    }

# --------------------------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "Africa/Lagos")
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------
# STATIC FILES
# --------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# --------------------------------------------------------------------
# MEDIA FILES (if needed later)
# --------------------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# --------------------------------------------------------------------
# MISC SETTINGS
# --------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APPEND_SLASH = False

# --------------------------------------------------------------------
# DRF CONFIG (optional)
# --------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ]
}