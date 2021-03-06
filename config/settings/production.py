# -*- coding: utf-8 -*-
'''
Production Configurations
'''
import logging
import re

from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['colegend.org'])

# DATABASES
# ------------------------------------------------------------------------------
DATABASES['default'] = env.db('DATABASE_URL')  # noqa F405
# DATABASES['default']['ATOMIC_REQUESTS'] = True  # noqa F405
# DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)  # noqa F405


# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'{env("REDIS_URL", default="redis://")}/{0}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            'IGNORE_EXCEPTIONS': True,
        }
    }
}


# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
# TODO: Check if this works -- I had False before
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
# TODO: Check!
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool('DJANGO_SECURE_HSTS_PRELOAD', default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = 'DENY'

# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ['storages']  # noqa F405
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_AUTO_CREATE_BUCKET = True
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_QUERYSTRING_AUTH = False
# DO NOT change these unless you know what you're doing.
_AWS_EXPIRY = 60 * 60 * 24 * 7
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': f'max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate',
}

# STATIC
# ------------------------
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA
# ------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/'

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa F405
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL', default='colegend <connect@colegend.org>')
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default='[colegend] ')

# Anymail (Mailgun)
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
INSTALLED_APPS += ['anymail']  # noqa F405
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
ANYMAIL = {
    'MAILGUN_API_KEY': env('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': env('MAILGUN_DOMAIN')
}

# Gunicorn
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['gunicorn']  # noqa F405

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#enable-whitenoise
MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE  # noqa F405

# raven
# ------------------------------------------------------------------------------
# https://docs.sentry.io/clients/python/integrations/django/
INSTALLED_APPS += ['raven.contrib.django.raven_compat']  # noqa F405
RAVEN_MIDDLEWARE = [
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
]
MIDDLEWARE = RAVEN_MIDDLEWARE + MIDDLEWARE

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = env('SENTRY_DSN')
SENTRY_CLIENT = env('DJANGO_SENTRY_CLIENT', default='raven.contrib.django.raven_compat.DjangoClient')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
    },
}

SENTRY_CELERY_LOGLEVEL = env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)
RAVEN_CONFIG = {
    'dsn': SENTRY_DSN
}
IGNORABLE_404_URLS = (
    re.compile(r'\.(php|cgi|aspx)$'),
    re.compile(r'^/wp-content'),
    re.compile(r'^/op69okl'),
)

# opbeat integration
# ------------------------------------------------------------------------------
# See https://opbeat.com/languages/django/
# INSTALLED_APPS += ['opbeat.contrib.django']
# OPBEAT = {
#     'ORGANIZATION_ID': env('DJANGO_OPBEAT_ORGANIZATION_ID'),
#     'APP_ID': env('DJANGO_OPBEAT_APP_ID'),
#     'SECRET_TOKEN': env('DJANGO_OPBEAT_SECRET_TOKEN')
# }
# MIDDLEWARE = ['opbeat.contrib.django.middleware.OpbeatAPMMiddleware'] + MIDDLEWARE


# SECURITY
# ------------------------------------------------------------------------------
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS

# Your production stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------


# ALLAUTH
# ------------------------------------------------------------------------------
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# EASY THUMBNAILS
# ------------------------------------------------------------------------------
# THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE


# CRONTAB
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_crontab']
CRON_TIMESTAMP = '`date +\%Y-\%m-\%dT\%H\%M`'
CRON_LOGS_PATH = '~/colegend/logs/'
CRONJOBS = [
    ('0 0 4 * *', 'django.core.management.call_command', ['process_contributions']),
    ('0 2 * * *', 'django.core.management.call_command', ['update_habit_streaks'], {}, f'>> {CRON_LOGS_PATH}update_habit_streaks_{CRON_TIMESTAMP}.txt'),
    ('0 14 * * *', 'django.core.management.call_command', ['generate_focus_reports', 'day'], {}, f'>> {CRON_LOGS_PATH}generate_focus_day_reports_{CRON_TIMESTAMP}.txt'),
    ('0 2 * * Mon', 'django.core.management.call_command', ['generate_focus_reports', 'week'], {}, f'>> {CRON_LOGS_PATH}generate_focus_week_reports_{CRON_TIMESTAMP}.txt'),
    ('0 2 8 * *', 'django.core.management.call_command', ['generate_focus_reports', 'month'], {}, f'>> {CRON_LOGS_PATH}generate_focus_month_reports_{CRON_TIMESTAMP}.txt'),
    ('0 2 4 1 *', 'django.core.management.call_command', ['generate_focus_reports', 'year'], {}, f'>> {CRON_LOGS_PATH}generate_focus_year_reports_{CRON_TIMESTAMP}.txt'),
]
CRONTAB_DJANGO_PROJECT_NAME = 'colegend'
CRONTAB_DJANGO_SETTINGS_MODULE = 'config.settings.production'
