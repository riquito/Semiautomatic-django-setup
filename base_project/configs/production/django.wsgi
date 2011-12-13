# -*- coding: utf-8 -*-

import os,sys

sys.stdout = sys.stderr

import glob,site
from os.path import abspath,dirname,join

os.environ['DJANGO_SETTINGS_MODULE'] = 'configs.production.settings'

PROJECT_PATH = abspath(join(dirname(__file__), "../../"))

VIRTUALENV_LIB_PATH = join(PROJECT_PATH,'.env/lib')

os.environ['PYTHON_EGG_CACHE'] = join(PROJECT_PATH,'var/tmp/egg-cache')
if not os.path.exists(os.environ['PYTHON_EGG_CACHE']):
    os.mkdir(os.environ['PYTHON_EGG_CACHE'])


if os.path.exists(VIRTUALENV_LIB_PATH):
    # "lib" has always at least a "python2.x" directory inside
    py_dirs = sorted(x for x in os.listdir(VIRTUALENV_LIB_PATH) if x.startswith('python'))
    site_packages_path = join(VIRTUALENV_LIB_PATH,py_dirs[-1],'site-packages')
     
    #site.addsitedir(site_packages_path)
    #sys.path = [sys.path[-1]]+sys.path[0:-1]
    
    ALLDIRS = [site_packages_path]

    # Remember original sys.path.
    prev_sys_path = list(sys.path) 

    # Add each new site-packages directory.
    for directory in ALLDIRS:
       site.addsitedir(directory)

    # Reorder sys.path so new directories at the front.
    new_sys_path = [] 
    for item in list(sys.path): 
        if item not in prev_sys_path: 
            new_sys_path.append(item) 
            sys.path.remove(item) 
    sys.path[:0] = new_sys_path  
    

sys.path.insert(0, PROJECT_PATH)
sys.path.insert(1, join(PROJECT_PATH,'apps'))

import logging
import django.core.handlers.wsgi
import django.core.signals
import django.dispatch.dispatcher

my_signal = django.dispatch.dispatcher.Signal()

def log_exception(*args, **kwds):
    logging.exception('Exception in request:',*args,**kwds)

# Log errors.
my_signal.connect(
    log_exception, django.core.signals.got_request_exception
)

application = django.core.handlers.wsgi.WSGIHandler()
