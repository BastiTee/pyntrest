"""Django default module for url pattern definition"""

from django.conf.urls import *
from pyntrest.views import ViewHandler

urlpatterns = [
    url(r'^', ViewHandler().get, name='get'),
]
