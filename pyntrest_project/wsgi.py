"""WSGI-hook for Pyntrest to combine Django with a WSGI-compatible web
server like Apache HTTP or Unicorn."""

# The following two lines MUST stick to the top in that order 
# right on top. Otherwise WSGI-usage will not work. 
from os import environ
environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyntrest_project.settings')

from django.core.wsgi import get_wsgi_application
from pyntrest.pyntrest_core import on_startup

# run Pyntrest's system initialization procedure
on_startup()
application = get_wsgi_application()
