"""WSGI-hook for Pyntrest to combine Django with a WSGI-compatible web
server like Apache HTTP or Unicorn."""

from os import environ
from django.core.wsgi import get_wsgi_application
from pyntrest.pyntrest_processor import on_startup

environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyntrest_project.settings')

# run Pyntrest's system initialization procedure
on_startup()
application = get_wsgi_application()
