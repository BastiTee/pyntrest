"""Test suite for module views"""
from os import path, makedirs
from shutil import rmtree, copyfile
from tempfile import mkdtemp
import unittest

from django.http import HttpRequest
from django.http.response import HttpResponseRedirect, HttpResponse

from pyntrest.pyntrest_core import PyntrestHandler
from pyntrest.views import ViewHandler

class ViewsTestSuite(unittest.TestCase):

    mip = path.join(path.abspath(path.dirname(__file__)), 'testdata')
    sip = path.abspath(path.dirname(__file__))

    def generate_test_dirs (self):
        base_static = path.join(
                    path.dirname(path.dirname(__file__)),
                    'pyntrest', 'static','pyntrest')
        static_images_dir = mkdtemp()
        #print 'Temp dir created at {}'.format(static_images_dir)
        for subdir in [ 'res', 'css', 'fonts', 'js']:
            makedirs(path.join(static_images_dir, subdir ))
        for resfile in [
                        path.join('res', 'favicon.png.default'),
                        path.join('res', 'favicon-apple.png.default'),
                        path.join('css', 'pyntrest-main.css.default'),
                        'index.html.default',
                        'bookify.html.default',
                        ]:
            copyfile(path.join(base_static, resfile),
                 path.join(static_images_dir, resfile))
        self.addCleanup(rmtree, static_images_dir, True)
        return  static_images_dir

    def test_get (self):

        views_h = ViewHandler ()
        static_images_dir = self.generate_test_dirs()
        pyntrest_handler = PyntrestHandler(self.mip, static_images_dir)
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

        request = HttpRequest()
        request.path = '/'
        response = type(views_h.get(request))
        self.assertIs(HttpResponse, response)
        self.assertEquals(200, response.status_code)

if __name__ == '__main__':
    unittest.main()
