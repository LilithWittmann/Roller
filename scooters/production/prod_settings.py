from os import environ
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# PostGIS db
# - You have to set this up locally yourself (TODO)
# - When setting up, make sure to create the postgis extension for the DB
# - Remove to use SQLite/SpatiaLite
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': environ.get('RDS_DB_HOST'),
        'NAME': environ.get('RDS_DB_NAME'),
        'USER': environ.get('RDS_DB_USER'),
        'PASSWORD': environ.get('RDS_DB_PASSWORD'),
    },
}


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

AWS_EB_DEFAULT_REGION = "eu-central-1"
# your aws access key id
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# your aws access key
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# queue name to use - queues that don't exist will be created automatically
AWS_EB_DEFAULT_QUEUE_NAME = "roller_queue"

STATIC_ROOT = "/static/"
ALLOWED_HOSTS = ['*']
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_REGION_NAME = 'eu-central-1'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
