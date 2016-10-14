"""Django default module for view generation"""

from django.shortcuts import redirect, render
from pyntrest.pyntrest_io import cleanup_url_path
from pyntrest.pyntrest_core import PyntrestHandler
from pyntrest.pyntrest_config import YOUR_IMAGE_FOLDER, STATIC_PATH,\
    EXTERNAL_BASE_URL,BOOKIFY_PATH

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

        if BOOKIFY_PATH:
            clean_bookify_path = cleanup_url_path('/' + BOOKIFY_PATH + '/')
            #print 'Testing path \'{}\' against bookify root path \'{}\''.format(request.path, clean_bookify_path)
            if request.path == clean_bookify_path:
                view_context = self.pyntrest_handler.generate_view_context_bookify()
                return render(request, 'pyntrest/bookify.html', view_context)

        if not self.pyntrest_handler.check_if_album_exists(request.path):
            # If path does not exist, redirect to root album
            if EXTERNAL_BASE_URL is not None:
                return redirect(EXTERNAL_BASE_URL)
            else:
                return redirect('/')
        else:
            if not self.pyntrest_handler:
                return render(request, 'pyntrest/index.html', None)
            # check if static files like css have been updated
            self.pyntrest_handler.upgrade_static_files()
            view_context = self.pyntrest_handler.generate_view_context(
                request.path)
            return render(request, 'pyntrest/index.html', view_context)
