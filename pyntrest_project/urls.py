"""URL definition for Pytnrest's Django project. Basically this is only used
to redirect to straight to the only app involved."""

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('pyntrest.urls', namespace='pyntrest')),
)
