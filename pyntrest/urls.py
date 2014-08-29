"""Django default module for url pattern definition"""

from django.conf.urls import patterns, url
from pyntrest import views

urlpatterns = patterns('',
    url(r'^', views.get, name='get'),
)
