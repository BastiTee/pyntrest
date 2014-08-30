"""Django default module for view generation"""

from django.shortcuts import redirect, render
from django.http import Http404 
from os import path
from pyntrest.pyntrest_core import generate_view_context
from pyntrest_io import (cleanup_url_path,
    convert_url_path_to_local_filesystem_path)
from pyntrest_constants import MAIN_IMAGES_PATH

def get(request):
    """This method serves the GET requests to the web photo albums"""
   
    if not request:
        raise TypeError
   
    # Check whether to redirect on dirty request paths
    clean_path = cleanup_url_path(request.path)
    if not request.path == clean_path:
        return redirect(clean_path)
       
    local_albumpath_abs = convert_url_path_to_local_filesystem_path(
                  MAIN_IMAGES_PATH, clean_path)
    
    if not request.path.endswith('/'):
        request.path = request.path + '/'
        
    if not path.exists(local_albumpath_abs):
        raise Http404
    if path.isdir(local_albumpath_abs):
        view_context = generate_view_context(local_albumpath_abs, request.path)
        return render(request, 'pyntrest/index.html', view_context)
