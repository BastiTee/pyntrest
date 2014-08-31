"""Test suite for module pyntrest_core"""

from os import environ, path
environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyntrest_project.settings')

from shutil import rmtree
from tempfile import mkdtemp
from pyntrest.pyntrest_core import PyntrestHandler
import unittest

class CoreTestSuite(unittest.TestCase):
    
    def generate_test_dirs (self):
        static_images_dir = mkdtemp()
        self.addCleanup(rmtree, static_images_dir, True)
        test_images_dir = path.join(path.abspath(path.dirname(__file__)), 'testdata')
        return test_images_dir, static_images_dir
    
    def test_init (self):
        self.assertRaises(TypeError, PyntrestHandler)
        self.assertRaises(TypeError, PyntrestHandler, '')
        test_images_dir, static_images_dir = self.generate_test_dirs()
        pyh = PyntrestHandler( test_images_dir, static_images_dir)
        self.assertIsNotNone(pyh)
    
    """TODO More testing"""
        
if __name__ == '__main__':
    unittest.main()