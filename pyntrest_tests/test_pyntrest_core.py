"""Test suite for module pyntrest_core"""

from os import path
from shutil import rmtree
from tempfile import mkdtemp
from pyntrest.pyntrest_core import PyntrestHandler
import unittest
from pyntrest import pyntrest_config

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
    
    def test (self):
        test_images_dir, static_images_dir = self.generate_test_dirs()
        pyh = PyntrestHandler( test_images_dir, static_images_dir)
        context = pyh.generate_view_context('/')
        
        self.assertEquals(pyntrest_config.IMAGE_THUMB_WIDTH, context['col_width'])
        self.assertEquals(pyntrest_config.IMAGE_THUMB_HEIGHT, context['col_height'])
        self.assertEquals(pyntrest_config.WORDING_ALBUM, context['lang_albums'])
        self.assertEquals(pyntrest_config.WORDING_IMAGES, context['lang_images'])
    
        self.assertEquals('title', context['page_title'])
        self.assertEquals('desc', context['album_description'])
        
        breadcrumbs = context['breadcrumbs']
        images = context['images']
        subalbums = context['subalbums']
        
        self.assertEqual(1, len(breadcrumbs))
        self.assertEqual(3, len(images))
        self.assertEqual(1, len(subalbums))
        
