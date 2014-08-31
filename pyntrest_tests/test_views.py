"""Test suite for module views"""

from os import path
from pyntrest.pyntrest_core import PyntrestHandler
from django.http.response import HttpResponseRedirect, HttpResponse, Http404
from pyntrest.views import ViewHandler
from django.http import HttpRequest
from shutil import rmtree
import unittest

class ViewsTestSuite(unittest.TestCase):
    
    mip = path.join(path.abspath(path.dirname(__file__)), 'testdata')
    sip = path.abspath(path.dirname(__file__))
    
    def test_get (self):
        
        views_h = ViewHandler ()
        pyntrest_handler = PyntrestHandler(self.mip, self.sip)
        self.addCleanup(rmtree, path.join(self.sip, 'images'), True)
        views_h.set_pyntrest_handler(pyntrest_handler)
        
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