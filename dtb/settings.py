import logging
import os
import sys
import random
import string
from decouple import config

import dj_database_url

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load env variables from file
dotenv_file = BASE_DIR / ".env"


# SECURITY WARNING: keep the secret key used in production secret!
def generate_secret():
    default_secret_key_alphabet_list = list((string.ascii_letters + string.digits) * 2)
    random.shuffle(default_secret_key_alphabet_list)
    return "".join(default_secret_key_alphabet_list)[:64]


SECRET_KEY = config("DJANGO_SECRET_KEY", default=generate_secret())

DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    "*",
]  # since Telegram uses a lot of IPs for webhooks

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps
    "django_celery_beat",
    "debug_toolbar",
    "dbsettings",
    # local apps
    "users.apps.UsersConfig",
    "shop.apps.ShopConfig",
    "cloudpayments_django_app.apps.CloudpaymentsDjangoAppConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.common.CommonMiddleware",
]

MAIN_URL = config("URL", default="http://localhost:8000")
PAYMENT_URL = config("PAYMENT_URL")
ROOT_ADMIN_ID = config("ROOT_ADMIN_ID")

CSRF_TRUSTED_ORIGINS = [MAIN_URL]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "dtb.urls"

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

WSGI_APPLICATION = "dtb.wsgi.application"
ASGI_APPLICATION = "dtb.asgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(conn_max_age=600, default="sqlite:///db.sqlite3"),
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

# -----> CELERY
REDIS_URL = config("REDIS_URL", default="redis://redis:6379")
BROKER_URL = REDIS_URL
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_DEFAULT_QUEUE = "default"

# -----> TELEGRAM
TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
TELEGRAPH_INSTRUCTION_LINK = config("TELEGRAPH_INSTRUCTION_LINK")

if TELEGRAM_TOKEN is None:
    logging.error(
        "Please provide TELEGRAM_TOKEN in .env file.\n"
        "Example of .env file: https://github.com/ohld/django-telegram-bot/blob/main/.env_example"
    )
    sys.exit(1)

TELEGRAM_LOGS_CHAT_ID = config("TELEGRAM_LOGS_CHAT_ID", default=None)
BOT_LINK = config("BOT_LINK")
CLOUDPAYMENTS_PUBLIC_ID = config("CLOUDPAYMENTS_PUBLIC_ID")
CLOUDPAYMENTS_SECRET_KEY = config("CLOUDPAYMENTS_SECRET_KEY")
GARPIX_PAYMENT_STATUS_CHANGED_CALLBACK = (
    "cloudpayments_django_app.views.payment_status_changed_callback"
)
SUBSCRIPTION_PRICE = 300
TRIAL_PERIOD_DAYS = 3
MAXIMUM_PROFILES = config("MAXIMUM_PROFILES", cast=int, default=5)
