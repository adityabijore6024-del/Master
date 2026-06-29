"""
Django settings for course project.
"""

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


# ======================================================
# SECURITY
# ======================================================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-dev-key"
)

DEBUG = os.environ.get(
    "DEBUG",
    "True"
) == "True"

ALLOWED_HOSTS = [
    "*"
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
    "https://*.up.railway.app",
]

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


# ======================================================
# APPS
# ======================================================

INSTALLED_APPS = [

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",

    "whitenoise.runserver_nostatic",

    "django.contrib.staticfiles",

    "frontend",
]


# ======================================================
# MIDDLEWARE
# ======================================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]


ROOT_URLCONF = "course.urls"


# ======================================================
# TEMPLATE
# ======================================================

TEMPLATES = [

    {

        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates"
        ],

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


WSGI_APPLICATION = "course.wsgi.application"


# ======================================================
# DATABASE
# ======================================================

DATABASES = {

    "default": dj_database_url.config(

        default=f"sqlite:///{BASE_DIR/'db.sqlite3'}",

        conn_max_age=600,

        conn_health_checks=True,

    )

}


# ======================================================
# PASSWORD
# ======================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },

]


# ======================================================
# LANGUAGE
# ======================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ======================================================
# STATIC FILES
# ======================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedStaticFilesStorage"
)


# ======================================================
# MEDIA
# ======================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ======================================================
# LOGIN
# ======================================================

LOGIN_URL = "login"


# ======================================================
# DEFAULT PK
# ======================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



# ==============================================================================
# API KEYS (Local + Railway)
# ==============================================================================

# Gemini API
GEMINI_API_KEY = os.environ.get(
    "GEMINI_API_KEY",
    "AQ.Ab8RN6JZxY8akIw3pMcdk7nz9oKZcFQ_rcIhcyQvmSOq0abR8A"
)

# Razorpay
RAZORPAY_KEY_ID = os.environ.get(
    "RAZORPAY_KEY_ID",
    "rzp_test_T7WAoq5vjPbjGS"
)

RAZORPAY_KEY_SECRET = os.environ.get(
    "RAZORPAY_KEY_SECRET",
    "Bh40t2GEFmzYX7uYX9XdmXH9"
)
