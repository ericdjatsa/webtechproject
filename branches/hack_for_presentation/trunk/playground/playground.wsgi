import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'playground.settings'
sys.path.append('/xampplite/Django-1.1.1')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
