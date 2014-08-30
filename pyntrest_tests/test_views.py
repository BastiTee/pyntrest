"""Test suite for module views"""

from os import environ
from django.http.response import HttpResponseRedirect
environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyntrest_project.settings')
from django.http import HttpRequest
from pyntrest import views
import unittest

class ViewsTestSuite(unittest.TestCase):
    
    def test_get (self):
        self.assertRaises(TypeError, views.get)
        request = HttpRequest()
        request.path = '///'
        self.assertIs(HttpResponseRedirect, type(views.get(request)))
        request.path = '/index.html'
        self.assertIs(HttpResponseRedirect, type(views.get(request)))
        request.path = ''
        redirect = views.get(request)
        self.assertIs(HttpResponseRedirect, type(redirect))
        self.assertEquals('/', redirect.url)
        request.path = redirect.url
        # TODO 
        
if __name__ == '__main__':
    unittest.main()