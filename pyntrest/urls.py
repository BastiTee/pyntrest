"""Django default module for url pattern definition"""

from django.conf.urls import patterns, url
from pyntrest.views import ViewHandler
from pyntrest.pyntrest_core import PyntrestHandler

# Generate a new view handler with a default Pyntrest handler 
view_handler = ViewHandler ( PyntrestHandler() )

urlpatterns = patterns('',
    url(r'^', view_handler.get, name='get'),
)
