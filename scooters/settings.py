"""
Django settings for scooters project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'viddb+p+j9&b(5+-v2f&q2d^8^25mgs5_8qxfkznxfml3r#+=1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    ## Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    ## Django extensions
    'django_extensions',

    ## GeoDjango support
    'django.contrib.gis',

    ## GraphQL & PostGIS
    'graphene_django',
    'graphene_gis_extension', # this is our own extension

    ## Serious Django
    'serious_django_services',
    'serious_django_permissions',
    'serious_django_graphene',

    ## Your helpers app
    'helpers',
    'django_admin_json_editor',  # for the crawler settings
    'leaflet',

    ## Your own apps
    'vehicles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    # Only add the toolbar when DEBUG=True
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

ROOT_URLCONF = 'scooters.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'scooters.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    # overwrite this in local_settings.py, see the README
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


# Session management via cache (=> via Redis)
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# Graphene settings
GRAPHENE = {
    'SCHEMA': 'scooters.schema.schema'
}


# Authentication settings (do NOT put app keys etc. here, these are local / stored in deployment)
AUTHENTICATION_BACKENDS = (
    'serious_django_permissions.permissions.PermissionModelBackend',
)


# Serious Django configuration
DEFAULT_GROUPS_MODULE = 'users.default_groups'


# shell_plus config (useful for development)
SHELL_PLUS_PRE_IMPORTS = [
    ('django.contrib.gis.geos', '*'),
    ('helpers', '*'),
]

# Setting to have debug-toolbar show up on local development
INTERNAL_IPS = ['127.0.0.1', '127.0.0.3']


INSTALLED_CRAWLERS = {
    "circ": 'vehicles.crawlers.circ.CircCrawler',
    "emmy": 'vehicles.crawlers.emmy.EmmyCrawler',
    "hive": 'vehicles.crawlers.hive.HiveCrawler',
    "lime": 'vehicles.crawlers.lime.LimeCrawler',
    "tier": 'vehicles.crawlers.tier.TierCrawler',
    "ufo": 'vehicles.crawlers.ufo.UfoCrawler',
    "voi": 'vehicles.crawlers.voi.VoiCrawler',
    "zero": 'vehicles.crawlers.tier.ZeroCrawler',
}

# Use the file local_settings.py to overwrite the defaults with your own
# settings
try:
    from .local_settings import *
except ImportError:
    pass

# If (and only if) we're using docker (implied by the IS_DOCKER env variable),
# import the relevant settings
from os import environ
if environ.get('IS_DOCKER') is not None:
    from .docker_settings import *
