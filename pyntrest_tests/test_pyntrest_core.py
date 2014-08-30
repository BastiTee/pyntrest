"""Test suite for module pyntrest_core"""

from os import environ, path
environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyntrest_project.settings')

from pyntrest.pyntrest_core import PyntrestHandler
import unittest

class CoreTestSuite(unittest.TestCase):
    
    def test_init (self):
        pyntrest_h = PyntrestHandler ()
        mip = path.join(path.abspath(path.dirname(__file__)), 'testdata')
        pyntrest_h.set_main_images_path(mip)
        self.assertFalse(pyntrest_h is None)
    
    """TODO More testing"""
        
if __name__ == '__main__':
    unittest.main()