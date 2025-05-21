"""
WSGI config for gutendex project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
print("PYTHONPATH:", sys.path)
print("Current directory:", os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gutendex.settings')

application = get_wsgi_application()
