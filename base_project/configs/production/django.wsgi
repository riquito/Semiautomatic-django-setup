# -*- coding: utf-8 -*-

import os,sys,glob
import site
from os.path import abspath,dirname,join

os.environ['DJANGO_SETTINGS_MODULE'] = 'configs.production.settings'

PROJECT_PATH = abspath(join(dirname(__file__), "../../"))

VIRTUALENV_LIB_PATH = join(PROJECT_PATH,'.env/lib')

os.environ['PYTHON_EGG_CACHE'] = join(PROJECT_PATH,'var/tmp/egg-cache')
if not os.path.exists(os.environ['PYTHON_EGG_CACHE']):
    os.mkdir(os.environ['PYTHON_EGG_CACHE'])

if os.path.exists(VIRTUALENV_LIB_PATH):
    # "lib" has always at least a "python2.x" directory inside
    py_dirs = sorted(glob.glob(VIRTUALENV_LIB_PATH + '/py*'))
    site.addsitedir(join(VIRTUALENV_LIB_PATH,py_dirs[-1],'site-packages'))

sys.path.insert(0, PROJECT_PATH)
sys.path.insert(1, join(PROJECT_PATH,'apps'))

import logging
import django.core.handlers.wsgi
import django.core.signals
import django.dispatch.dispatcher

def log_exception(*args, **kwds):
    logging.exception('Exception in request:',*args,**kwds)

# Log errors.
django.dispatch.dispatcher.connect(
    log_exception, django.core.signals.got_request_exception
)

application = django.core.handlers.wsgi.WSGIHandler()
