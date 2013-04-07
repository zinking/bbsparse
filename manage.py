#!/usr/bin/env python

# Add "common-apps" folder to sys.path if it exists
import os, sys
common_dir = os.path.join(os.path.dirname(__file__), 'common-apps')
if os.path.exists(common_dir):
    sys.path.append(common_dir)

# Initialize App Engine SDK if djangoappengine backend is installed
DIR_PATH = "d:\\Program Files\\Google\\appengine\\"
print "DIRPATH",DIR_PATH
SCRIPT_DIR = os.path.join(DIR_PATH, 'google', 'appengine', 'tools')



EXTRA_PATHS = [
  DIR_PATH,
  os.path.join(DIR_PATH, 'lib', 'antlr3'),
  os.path.join(DIR_PATH, 'lib', 'django_0_96'),
  os.path.join(DIR_PATH, 'lib', 'fancy_urllib'),
  os.path.join(DIR_PATH, 'lib', 'ipaddr'),
  os.path.join(DIR_PATH, 'lib', 'protorpc'),
  os.path.join(DIR_PATH, 'lib', 'webob'),
  os.path.join(DIR_PATH, 'lib', 'whoosh'),
  os.path.join(DIR_PATH, 'lib', 'yaml', 'lib'),
  os.path.join(DIR_PATH, 'lib', 'simplejson'),
  os.path.join(DIR_PATH, 'lib', 'graphy'),
]

sys.path = EXTRA_PATHS + sys.path

  
  
  
try:
    from djangoappengine.boot import setup_env
except ImportError:
    pass
else:
    setup_env()

from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
