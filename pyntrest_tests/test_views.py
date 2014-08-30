"""Test suite for module views"""

from os import environ, path
environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyntrest_project.settings')

from django.http.response import HttpResponseRedirect, HttpResponse, Http404
from pyntrest.pyntrest_core import PyntrestHandler
from pyntrest.views import ViewHandler
from django.http import HttpRequest
import unittest

class ViewsTestSuite(unittest.TestCase):
    
    def test_get (self):
        
        pyntrest_h = PyntrestHandler ()
        mip = path.join(path.abspath(path.dirname(__file__)), 'testdata')
        pyntrest_h.set_main_images_path(mip)
        views_h = ViewHandler ( pyntrest_h )
        
        self.assertRaises(TypeError, views_h.get)
        
        request = HttpRequest()
        request.path = '///'
        self.assertIs(HttpResponseRedirect, type(views_h.get(request)))
        
        request = HttpRequest()
        request.path = '/index.html'
        self.assertIs(HttpResponseRedirect, type(views_h.get(request)))
        
        request = HttpRequest()
        request.path = ''
        redirect = views_h.get(request)
        self.assertIs(HttpResponseRedirect, type(redirect))
        self.assertEquals('/', redirect.url)
        
        request = HttpRequest()
        request.path = '/notexistingalbum'
        try:
            views_h.get(request)
            self.fail()
        except Http404:
            pass
        
        request = HttpRequest()
        request.path = '/'
        response = type(views_h.get(request))
        self.assertIs(HttpResponse, response)
        self.assertEquals(200, response.status_code)        
        
if __name__ == '__main__':
    unittest.main()