"""Test suite for module pyntrest_pil"""

from pyntrest import pyntrest_pil
from PIL import Image        
from os import path, remove
import unittest

class PilTestSuite(unittest.TestCase):

    base_path = path.abspath(path.dirname(__file__))
    
    def test_resize_image ( self ):

        self.assertRaises(TypeError, pyntrest_pil.create_image_thumbnail_if_not_present)
        self.assertRaises(TypeError, pyntrest_pil.create_image_thumbnail_if_not_present, None)
        self.assertRaises(TypeError, pyntrest_pil.create_image_thumbnail_if_not_present, None, None)
        self.assertRaises(TypeError, pyntrest_pil.create_image_thumbnail_if_not_present, 
                          '/somewhere/foo.jpg', '/somewhere/foo2.jpg')
        source_file = path.join ( self.base_path, 'testdata', 'image.jpg')
        target_file = path.join ( self.base_path, 'testdata', 'image-trg.jpg')
        self.addCleanup(remove, target_file)
        width, height = pyntrest_pil.create_image_thumbnail_if_not_present(source_file, target_file)
        self.assertTrue(path.exists(target_file))
        self.assertEqual(300, width)
        self.assertEqual(199, height)
        im = Image.open(target_file)
        self.assertEqual((525, 348), im.size)
         
if __name__ == '__main__':
    unittest.main()