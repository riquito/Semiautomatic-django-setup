#!/usr/bin/env python

import os,imp
from os.path import join,dirname,abspath

conf_target = os.environ.get('TARGET','develop')
conf_path = abspath(join(dirname(__file__),'configs',conf_target))

try:
    fp,path,desc = imp.find_module('settings',[conf_path])
    try: 
      settings = imp.load_module('settings',fp,path,desc)
    finally: 
      fp.close()
    
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory configs/%s. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % conf_target)
    sys.exit(1)


if __name__ == "__main__":
    from django.core.management import execute_manager
    execute_manager(settings)
