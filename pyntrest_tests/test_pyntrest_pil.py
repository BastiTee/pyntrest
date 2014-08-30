"""Test suite for module pyntrest_pil"""

from pyntrest import pyntrest_pil
from PIL import Image        
from os import path, remove
import unittest

class PilTestSuite(unittest.TestCase):

    base_path = path.abspath(path.dirname(__file__))
    
    def test_rescale_image_dimensions_to_desired_width (self):
        self.assertRaises(TypeError, pyntrest_pil.rescale_image_dimensions_to_desired_width)
        self.assertRaises(TypeError, pyntrest_pil.rescale_image_dimensions_to_desired_width, None)
        self.assertRaises(TypeError, pyntrest_pil.rescale_image_dimensions_to_desired_width, None, None)
        self.assertRaises(TypeError, pyntrest_pil.rescale_image_dimensions_to_desired_width, None, None, None)
        self.assertRaises(TypeError, pyntrest_pil.rescale_image_dimensions_to_desired_width, None, None, None, None)
        a, b, c, d = pyntrest_pil.rescale_image_dimensions_to_desired_width(500, 400, 200, 1)
        self.assertEqual(200, a)
        self.assertEqual(160, b)
        self.assertEqual(200, c)
        self.assertEqual(160, d)  
        a, b, c, d = pyntrest_pil.rescale_image_dimensions_to_desired_width(500, 400, 200, 2)
        self.assertEqual(200, a)
        self.assertEqual(160, b)
        self.assertEqual(400, c)
        self.assertEqual(320, d)  
    
    def test_create_image_thumbnail_if_not_present ( self ):

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
        
    def test_create_album_thumbnail_if_not_present ( self ):

        self.assertRaises(TypeError, pyntrest_pil.create_album_thumbnail_if_not_present)
        self.assertRaises(TypeError, pyntrest_pil.create_album_thumbnail_if_not_present, None)
        self.assertRaises(TypeError, pyntrest_pil.create_album_thumbnail_if_not_present, None, None)
        self.assertRaises(TypeError, pyntrest_pil.create_album_thumbnail_if_not_present, 
                          '/somewhere/foo.jpg', '/somewhere/foo2.jpg')
        source_file = path.join ( self.base_path, 'testdata', 'image.jpg')
        target_file = path.join ( self.base_path, 'testdata', 'album-trg.jpg')
        self.addCleanup(remove, target_file)
        width, height = pyntrest_pil.create_album_thumbnail_if_not_present(source_file, target_file)
        self.assertTrue(path.exists(target_file))
        self.assertEqual(300, width)
        self.assertEqual(150, height)
        im = Image.open(target_file)
        self.assertEqual((525, 262), im.size)
