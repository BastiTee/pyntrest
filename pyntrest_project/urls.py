"""URL definition for Pytnrest's Django project. Basically this is only used
to redirect to straight to the only app involved."""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from pyntrest.pyntrest_rss import RSSFeed

admin.autodiscover()

rss_feed = RSSFeed()
urlpatterns = patterns('',
    url(r'^feed.xml$',rss_feed),
    url(r'^', include('pyntrest.urls', namespace='pyntrest')),
)
