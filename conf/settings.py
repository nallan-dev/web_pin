from pathlib import Path

from cron_descriptor import Options

# ==========================================================================

DEBUG = True
ALLOWED_HOSTS = ["*"]  # "*" Only for private network!
WEB_APP_PORT = 8080  # Port of this Django-app
FAKE_GPIO = True  # On raspberry set to False here to use real GPIO
USE_BOT = True  # Don't show in interfaces and don't launch in background

# Telegram bot conf in web admin panel (if change token - app restart required)

# Internationalization
LANGUAGE_CODE = "ru-ru"  # supports only 'ru-ru' and 'en-us'
# On Raspberry requires installed locales ru_RU.UTF-8 and/or en_US.UTF-8
# (you can install them in raspi-config)
TIME_ZONE = "Europe/Moscow"  # 'UTC' etc.
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

# GPIO BOARD nums available for use. (https://pinout.xyz/)
# Works for Pi1 Model B+, Pi 2B, Pi Zero, Pi 3B, and Pi 4B.
# Remove some if you want to exclude them from list of available (app restart)
# Make sure that deleted pin doesn't already in use in database!
# In that case - delete pin-config in admin panel first, then remove here
# and restart app.
BOARD_NUMS = [
    3,
    5,
    7,
    8,
    10,
    11,
    12,
    13,
    15,
    16,
    18,
    19,
    21,
    22,
    23,
    24,
    26,
    29,
    31,
    32,
    33,
    35,
    36,
    37,
    38,
    40,
]

# ==========================================================================


CRON_OPTIONS = Options()
if "ru" in LANGUAGE_CODE:
    CRON_OPTIONS.locale_code = "ru_RU"
    CRON_OPTIONS.use_24hour_time_format = True
else:
    CRON_OPTIONS.locale_code = "en_US"
    CRON_OPTIONS.use_24hour_time_format = False


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "for-local-network-so-no-big-secret"

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Application definition

INSTALLED_APPS = [
    "relay_app.apps.RelayAppConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "conf.middlewares.AutoAuthAdminMiddleware",
]

ROOT_URLCONF = "conf.urls"

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


WSGI_APPLICATION = "conf.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
