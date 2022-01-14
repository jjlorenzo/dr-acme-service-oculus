import os
import pathlib

ALLOWED_HOSTS = os.environ.get("OCULUS_ALLOWED_HOSTS", "*").split(",")

AUTH_PASSWORD_VALIDATORS = []

BASE_DIR = pathlib.Path(__file__).resolve().parent

CSRF_COOKIE_SECURE = os.environ.get("OCULUS_CSRF_COOKIE_SECURE", "no") == "yes"

DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.environ.get("OCULUS_DATABASE_NAME", "acme-service-oculus"),
    "USER": os.environ.get("OCULUS_DATABASE_USER"),
    "PASSWORD": os.environ.get("OCULUS_DATABASE_PASSWORD"),
    "HOST": os.environ.get("OCULUS_DATABASE_HOST", "localhost"),
  }
}

DEBUG = os.environ.get("OCULUS_DEBUG", "yes") != "no"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
  "acme.service.oculus",
]

MIDDLEWARE = [
  "django.middleware.security.SecurityMiddleware",
  "django.middleware.csrf.CsrfViewMiddleware",
  "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "acme.service.oculus.urls"

SECRET_KEY = "f6dvs8*3==y@^pmgd)5f^+r$h0*#9&)2@9)=7qnm)6r3ahl3bx"

SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("OCULUS_SECURE_HSTS_INCLUDE_SUBDOMAINS", "no") != "yes"
SECURE_HSTS_PRELOAD = os.environ.get("OCULUS_SECURE_HSTS_PRELOAD", "no") != "yes"
SECURE_HSTS_SECONDS = int(os.environ.get("OCULUS_SECURE_HSTS_SECONDS", "0"))

SECURE_SSL_REDIRECT = os.environ.get("OCULUS_SECURE_SSL_REDIRECT", "no") != "yes"

TEMPLATES = []

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True

WSGI_APPLICATION = "acme.service.oculus.wsgi.application"
