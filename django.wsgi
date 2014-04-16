import os
import sys
sys.path.append( '/var/www/' )
sys.path.append( '/var/www/bbsparse/' )

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bbsparse.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

