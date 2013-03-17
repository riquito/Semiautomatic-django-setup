# -*- coding: utf-8 -*-

from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

### DJANGO-COMPRESSOR ###
COMPRESS_ENABLED = True

# if set to True you must run "python manage.py compress" after 
# collecting new static files
COMPRESS_OFFLINE = True
#########################

### CACHE ###
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PROJECT_PATH,'var/tmp/django_cache'),
    }
}

CACHE_MIDDLEWARE_SECONDS = 60*5
#############

### LOGGING ###
LOGGING['handlers']['file']['level'] = 'ERROR'
###############

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY') 

ADMINS = (
   ('Riccardo Galli', 'riccardo@sideralis.org'),
)

MANAGERS = ADMINS

"""
DATABASES = {
    'default': {
        'ENGINE': get_env_variable('DJANGO_DB_ENGINE'), # Add django.db.backends. 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
	'NAME': get_env_variable('DJANGO_DB_NAME'),                      # Or path to database file if using sqlite3.
        'USER': get_env_variable('DJANGO_DB_USER'),                      # Not used with sqlite3.
        'PASSWORD': get_env_variable('DJANGO_DB_PASSWORD'),                  # Not used with sqlite3.
        'HOST': get_env_variable('DJANGO_DB_HOST'),                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': get_env_variable('DJANGO_DB_PORT'),                      # Set to empty string for default. Not used with sqlite3.
    }
}
"""
#INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = ['*']
