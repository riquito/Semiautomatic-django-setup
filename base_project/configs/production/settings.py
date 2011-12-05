# -*- coding: utf-8 -*-

from configs.develop.settings import *

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

try:
    from local_settings import *
except ImportError:
    pass

