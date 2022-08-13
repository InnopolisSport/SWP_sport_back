"""
Django settings for adminpage project.

Generated by 'django-admin startproject' using Django 2.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from datetime import timedelta

SENTRY_DSN = os.getenv("SENTRY_DSN", None)

if SENTRY_DSN is not None:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


def compose_base_url(schema, hostname, port) -> str:
    base_url = f"{schema}://{hostname}"
    if port is not None and int(port) != 80:
        base_url += f":{port}"
    return base_url


DATE_FORMAT = "%Y-%m-%d"

# People with passed checkup are able to upload self-sport
SELFSPORT_MINIMUM_MEDICAL_GROUP_ID = -1

JS_VERSION = "Sum22.17.4"

SPORT_DEPARTMENT_EMAIL = "sport@innopolis.university"
STUDENT_AUTH_GROUP_VERBOSE_NAME = "Students"
STUDENT_AUTH_GROUP_NAME = "S-1-5-21-721043115-644155662-3522934251-2285"

TRAINER_AUTH_GROUP_VERBOSE_NAME = "School Physical Activity for Health"
TRAINER_AUTH_GROUP_NAME = "S-1-5-21-2948122937-1530199265-1034249961-9635"

SC_TRAINERS_GROUP_NAME_FREE = "SC trainers (free)"
SC_TRAINERS_GROUP_NAME_PAID = "SC trainers (paid)"
SELF_TRAINING_GROUP_NAME = "Self training"
EXTRA_EVENTS_GROUP_NAME = "Extra sport events"
MEDICAL_LEAVE_GROUP_NAME = "Medical leave"
OTHER_SPORT_NAME = "Other"

TRAINING_EDITABLE_INTERVAL = timedelta(
    days=3
)

BACHELOR_STUDY_PERIOD_YEARS = 4
BACHELOR_GROUPS_PREFIX = "B"
# When changing STUDENT_MAXIMUM_GROUP_COUNT
# make sure to change the corresponding constraint in the DB
STUDENT_MAXIMUM_GROUP_COUNT = 5

SCHEMA = os.getenv("SCHEMA", "http")
HOSTNAME = os.getenv("HOSTNAME", "localhost")
PORT = os.getenv("PORT", 80)

BASE_URL = compose_base_url(SCHEMA, HOSTNAME, PORT)

PREFIX = ""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv_boolean("DEBUG")
PROJECT_ROOT = "/src/"
ALLOWED_HOSTS = [HOSTNAME, 'adminpanel', '*']

if DEBUG:
    ALLOWED_HOSTS.append('localhost')

if os.getenv('SCHEMA') == 'https':
    # make django think it is using https
    # WARNING: make sure, only trusted connections are possible
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = [
    'adminpage.apps.SportAdminConfig',
    'django.contrib.auth',
    'accounts',
    'revproxy',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_sendfile',
    'smartfields',
    'import_export',
    'rangefilter',
    'image_optimizer',
    'django_auth_adfs',
    'admin_auto_filters',
    'rest_framework',
    'django_prometheus',
    'drf_yasg',
    'sport.apps.SportConfig',
    'api',
    'media',
    'hijack',
    'hijack.contrib.admin',
    'tinymce',
    'django_telegram_login',
    'bot'
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
    'hijack.middleware.HijackUserMiddleware',
]

ROOT_URLCONF = 'adminpage.urls'

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, "templates/"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sport.context_processors.js_version',
            ],
        },
    },
]

WSGI_APPLICATION = 'adminpage.wsgi.application'

AUTH_USER_MODEL = 'accounts.User'

# Authentication
OAUTH_CLIENT_ID = os.getenv('oauth_appID')
OAUTH_CLIENT_SECRET = os.getenv("oauth_shared_secret")
OAUTH_AUTHORIZATION_BASEURL = os.getenv("oauth_authorization_baseURL")
OAUTH_GET_INFO_URL = os.getenv("oauth_get_infoURL")
OAUTH_TOKEN_URL = os.getenv("oauth_tokenURL")
OAUTH_END_SESSION_URL = os.getenv("oauth_end_session_endpoint")

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_adfs.backend.AdfsAuthCodeBackend',
)

AUTH_ADFS = {
    "SERVER": "sso.university.innopolis.ru",
    "CLIENT_ID": OAUTH_CLIENT_ID,
    "CLIENT_SECRET": OAUTH_CLIENT_SECRET,
    "RELYING_PARTY_ID": OAUTH_CLIENT_ID,
    # Make sure to read the documentation about the AUDIENCE setting
    # when you configured the identifier as a URL!
    "AUDIENCE": f"microsoft:identityserver:{OAUTH_CLIENT_ID}",
    "CA_BUNDLE": True,
    "USERNAME_CLAIM": "upn",
    # use group ids instead of name, because names are written in different languages
    "GROUPS_CLAIM": "groupsid",
    "GROUPS_CLAIM_REGEX": r"S-\d*-\d*-\d*-\d*-\d*-\d*-\d*",
    "MIRROR_GROUPS": True,
    "CLAIM_MAPPING": {
        "first_name": "given_name",
        "last_name": "family_name",
        "role": "role",
    },
}

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "profile"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {
    'default': {
        "ENGINE": 'django_prometheus.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_SERVER"),
        "PORT": "",  # default 5432 will be set
    }
}

PROMETHEUS_EXPORT_MIGRATIONS = False

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = '/static/'

if DEBUG:
    STATIC_URL = f'/{PREFIX}static/'
else:
    STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/uploaded_media'

# Sendfile settings
SENDFILE_BACKEND = "django_sendfile.backends.nginx"
SENDFILE_ROOT = MEDIA_ROOT
SENDFILE_URL = "/files/"

MEDICAL_REFERENCE_FOLDER = "medical_references"
SELF_SPORT_FOLDER = "self_sport_reports"
MEDICAL_GROUP_REFERENCE_FOLDER = "medical_group_references"

OPTIMIZED_IMAGE_METHOD = 'pillow'

MAX_IMAGE_SIZE = 10_000_000  # 10MB
MIN_IMAGE_DIMENSION = 400
MAX_IMAGE_DIMENSION = 4500

EMAIL_HOST = os.getenv("EMAIL_HOST", None)
EMAIL_PORT = os.getenv("EMAIL_PORT", None)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", None)
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", None)
EMAIL_USE_TLS = True

EMAIL_TEMPLATES = {
    'medical_leave_success': (
        '[IU Sport] Reference Accepted',
        'Your reference from {date} was accepted.\n'
        'You received {hours} hour(-s) for it.\n\n'
        'Your submission:\n{submission}'
    ),
    'medical_leave_reject': (
        '[IU Sport] Reference Rejected',
        'Your reference from {date} was rejected.\n'
        'Comment: {comment}\n\n'
        'Your submission:\n{submission}'
    ),
    'medical_group_success': (
        '[IU Sport] Medical Group Reference Processed',
        'Your medical group reference for semester {semester} was processed.\n'
        'You were assigned a medical group "{medical_group}".\n\n'
        'Your submission:\n{submission}'
    ),
    'medical_group_reject': (
        '[IU Sport] Medical Group Reference Rejected',
        'Your medical group reference for semester {semester} was rejected.\n'
        'Please, submit a new reference or contact the course support.\n'
        'Comment: {comment}\n\n'
        'Your submission:\n{submission}'
    ),
    'self_sport_success': (
        '[IU Sport] Self-training Proof Accepted',
        'Your self-training proof for {training_type} '
        'from {date} was accepted.\n'
        'You received {hours} hour(-s) for it.\n\n'
        'Your submission:\n{submission}'
    ),
    'self_sport_reject': (
        '[IU Sport] Self-training Report Rejected',
        'Your self-training proof for {training_type} '
        ' from {date} was rejected.\n'
        'Comment: {comment}\n\n'
        'Your submission:\n{submission}'
    ),
}

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", None)

TELEGRAM_BOT_TOKEN = '5210388390:AAHGSbn4NPLxtlK5nqDDSZUr3pTOpyUjzqo'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'bot.authentication.TelegramAuthentication',
    ]
}
