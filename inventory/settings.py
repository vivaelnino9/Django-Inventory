"""
Django settings for inventory project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ioa^_7xj(og*ng)r8jz@#ca&#u3r@dluelm6r-a+4g==7f9wue'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
HOST = ''

# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inv_app.apps.InvAppConfig',
    'bootstrap3',
    'sortedm2m',
    'storages',
    'boto',
]
SITE_ID = 1

# LOGGING CONFIGURATION
# A logging configuration that writes log messages to the console.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    # Formatting of messages.
    'formatters': {
        # Don't need to show the time when logging to console.
        'console': {
            'format': '%(levelname)s %(name)s.%(funcName)s (%(lineno)d) %(message)s'
        }
    },
    # The handlers decide what we should do with a logging message - do we email
    # it, ditch it, or write it to a file?
    'handlers': {
        # Writing to console. Use only in dev.
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        # Send logs to /dev/null.
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    # Loggers decide what is logged.
    'loggers': {
        '': {
            # Default (suitable for dev) is to log to console.
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'photologue': {
            # Default (suitable for dev) is to log to console.
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # logging of SQL statements. Default is to ditch them (send them to
        # null). Note that this logger only works if DEBUG = True.
        'django.db.backends': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventory.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'inventory.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inventory',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# AWS_REGION = os.environ.get('AWS_REGION', 'US Standard')


# STATIC_URL = 'https://s3-%s.amazonaws.com/%s/static/' % (AWS_REGION, AWS_STORAGE_BUCKET_NAME)
# MEDIA_URL = 'https://s3-%s.amazonaws.com/%s/media/' % (AWS_REGION, AWS_STORAGE_BUCKET_NAME)
# STATICFILES_STORAGE = 'inventory.customstorages.StaticStorage'
# DEFAULT_FILE_STORAGE = 'inventory.customstorages.MediaStorage'
# STATICFILES_LOCATION = 'img'  # name of folder within bucket
# MEDIAFILES_LOCATION = 'media' # name of folder within bucket


def get_static_memcache():
    # For python 2.7, just 'import urlparse'
    from urllib.parse import urlparse

    if os.environ.get('REDIS_URL', ''):
        redis_url = urlparse(os.environ.get('REDIS_URL'))
        return {
            "BACKEND": "redis_cache.RedisCache",
            'TIMEOUT': None,
            "LOCATION": "{0}:{1}".format(redis_url.hostname, redis_url.port),
            "OPTIONS": {
                "PASSWORD": redis_url.password,
                "DB": 0,
            }
        }
    return {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': None,
        'OPTIONS': {
            'MAX_ENTRIES': 5000
        }
    }

CACHES = {
    # Replace the default cache with your existing one (if you have any)
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    },
    'collectfast': get_static_memcache(),
}

COLLECTFAST_CACHE = 'collectfast'



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static/')

MEDIA_URL = 'inventory/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')
