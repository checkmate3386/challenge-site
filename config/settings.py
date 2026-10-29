"""Configuration simple du site et de sa génération statique."""
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content"


def lire_configuration_site():
    try:
        with (CONTENT_DIR / "site.json").open(encoding="utf-8") as fichier:
            configuration = json.load(fichier)
        if isinstance(configuration, dict):
            return configuration
    except (OSError, json.JSONDecodeError):
        pass
    return {}


SITE_CONFIG = lire_configuration_site()
SITE_BASE_PATH = SITE_CONFIG.get("SITE_BASE_PATH", "").strip("/")
SITE_URL = SITE_CONFIG.get(
    "SITE_URL", "https://challengetrailsudtoulousain.com"
).rstrip("/")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "site-statique-challenge-trail")
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver", ".onrender.com","challengetrailsudtoulousain.com","www.challengetrailsudtoulousain.com"]
CSRF_TRUSTED_ORIGINS = ["https://www.challengetrailsudtoulousain.com","https://challengetrailsudtoulousain.com"]
ROOT_URLCONF = "config.urls"
INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django_distill",
    "site_app",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "site_app" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.static",
                "django.template.context_processors.request",
                "site_app.context_processors.site_context",
            ],
        },
    },
]
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {}
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True
STATIC_URL = f"/{SITE_BASE_PATH + '/' if SITE_BASE_PATH else ''}static/"
STATIC_ROOT = BASE_DIR / ".static-build"
STATICFILES_DIRS = [CONTENT_DIR]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
