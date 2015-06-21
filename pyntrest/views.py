"""Django default module for view generation"""

from django.shortcuts import redirect, render
from pyntrest_io import cleanup_url_path
from pyntrest.pyntrest_core import PyntrestHandler
from pyntrest.pyntrest_config import YOUR_IMAGE_FOLDER, STATIC_PATH

class ViewHandler ():
    """Instances of this class handle incoming GET requests and serve
    the appropriate HTTP responses"""

    pyntrest_handler = None
    """Handler to create the webpage context for incoming GET requests"""

    def __init__(self):
        """Constructor"""
        self.pyntrest_handler = PyntrestHandler(YOUR_IMAGE_FOLDER, STATIC_PATH)
        
    def set_pyntrest_handler(self, pyntrest_handler):    
        self.pyntrest_handler = pyntrest_handler

    def get(self, request):
        """This method serves the GET requests to the web photo albums"""
       
        if not request:
            raise TypeError
       
        # Check whether to redirect on dirty request paths
        clean_path = cleanup_url_path(request.path)
        if not request.path == clean_path:
            return redirect(clean_path)
    
        if not request.path.endswith('/'):
            request.path = request.path + '/'
    
        if not self.pyntrest_handler.check_if_album_exists(request.path):
            # If path does not exist, redirect to root album 
            return redirect(request.build_absolute_uri('/'))
        else:
            if self.pyntrest_handler:
                view_context = self.pyntrest_handler.generate_view_context(request.path)
            return render(request, 'pyntrest/index.html', view_context)
