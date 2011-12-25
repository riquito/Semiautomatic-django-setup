#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
from fabric.api import local, settings, abort,env,require,prefix,sudo
from fabric.contrib.console import confirm

import os

def std_env(func):
    '''std_env(func)
    
    Decorator to apply to each function that needs to customize "env" dictionary-like object.
    Decorated functions MUST define env.confname with a custom label for the configuration, and provide
    the other settings either inside a <confname>_settings.py file or inside the same function (using an
    external file will let you put under your repository of choice this file and ignore the other).
    Whatever method is choosen, env.base_path MUST be defined as the root directory where the django
    project resides at.
    
    After running this decorator your env object will contain the following additional keys

    env_path    - path to the virtualenv environment
    media_path  - path to the directory where media files are collected
    static_path - path to the directory where static files are collected
    tmp_path    - path to the directory where tmp files are generated
    log_path    - path to the directory where log files are generated
    apps_path   - path to the directory where django apps are stored 
    activate    - a shortcut to run commands inside virtualenv 
    manage      - a shortcut to run manage.py
    '''

    def foo(*args,**xargs):
        res = func(*args,**xargs)

        if not env.has_key('confname'):
            raise Exception('Functions with std_env decorator must add to env dictionary a custom name under key "confname"')
        
        try:
           settingsModule = __import__('fabfile.%s_settings' % env.confname,fromlist='%s_settings' % env.confname)
           env.update(settingsModule.env)
        except ImportError,e:
           pass

        if not env.get('deploy_user'):
            env.deploy_user = env.user
        
        if not env.has_key('base_path'):
            raise Exception("Configuration named <%s> didn\'t declare key <base_path> inside variable <env>" % env.confname)
        
        while env.base_path.endswith('/'):
            env.base_path = env.base_path[0:-1]
         
        env.env_path = os.path.join(env.base_path,'.env')
        env.media_path = os.path.join(env.base_path,'var/media')
        env.static_path = os.path.join(env.base_path,'var/static')
        env.tmp_path = os.path.join(env.base_path,'var/tmp')
        env.log_path = os.path.join(env.base_path,'var/log')
        env.apps_path = os.path.join(env.base_path,'apps')

        env.manage = 'python %s/manage.py' % env.base_path
        env.activate = 'source %s/bin/activate' % env.env_path

        return res

    return foo

@std_env
def develop():
    env.confname = 'develop'
    env.base_path = os.path.abspath(os.getcwd())
    env.hosts = ['localhost']

@std_env
def production():
    env.confname = 'production'
    # note: read/rename the example external configuration file production_settings.py.example

def collectstatic():
    require('confname', provided_by=[local,production])
    
    with prefix(env.activate):
        sudo('''
            export TARGET="%(confname)s";
            %(manage)s collectstatic --noinput''' % env,
            user = env.deploy_user
        )

def clear_cache():
    require('confname', provided_by=[local,production])

    sudo('rm -fr %(base_path)s/var/tmp/*' % env,user=env.deploy_user)

def compress():
    require('confname', provided_by=[local,production])
    
    with prefix(env.activate):
        sudo('''
            export TARGET="%(confname)s";
            %(manage)s compress --force''' % env,
            user = env.deploy_user
        )

def compilemessages():
    require('confname', provided_by=[local,production])
    
    with prefix(env.activate):
        sudo('''
            export TARGET="%(confname)s";
            %(manage)s compilemessages''' % env,
            user = env.deploy_user
        )


def deploy():
    require('confname', provided_by=[local,production])
    
    compilemessages()
    collectstatic()
    compress()
    clear_cache()
