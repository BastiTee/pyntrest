"""Pyntrest wrapper for operations using Python image library (PIL)""" 

from PIL import Image
from os import path
from pyntrest_config import IMAGE_THUMB_WIDTH, IMAGE_THUMB_HEIGHT, UPSCALE_FACTOR
from pyntrest_constants import GIF_PATTERN

def rescale_image_dimensions_to_desired_width (width, height, des_width,
                                                upscale_factor):
    """Calculates new image dimensions based on the given image's width 
    and height and the provided desired image width multiplied by the
    upscale factor"""
    
    if not width or not height or not des_width or not upscale_factor:
        raise TypeError
    
    new_width = des_width
    new_height = int(height * (float(des_width) / float(width)))
    rescaled_width = int(float(new_width) * upscale_factor)
    rescaled_height = int(float(new_height) * upscale_factor)
    return new_width, new_height, rescaled_width, rescaled_height

def create_album_thumbnail_if_not_present (source_image, thumb_image):
    """If the target file does not exist, reads the source file and resizes 
    and crops it with the given width and height"""
    
    if not source_image:
        raise TypeError ('source_image not set')
    if not thumb_image:
        raise TypeError ('thumb_image not set')
    if not path.exists(source_image):
        raise TypeError ('source_image does not exist')
    if not path.exists(path.dirname(thumb_image)):
        raise TypeError ('Folder for thumb_image does not exist')
    
    if not path.exists(thumb_image):
        
        image = Image.open(source_image)
        width, height = image.size
        _, _, res_w, res_h = rescale_image_dimensions_to_desired_width(
                            width, height, IMAGE_THUMB_WIDTH, UPSCALE_FACTOR)
        image = image.resize((res_w, res_h), Image.ANTIALIAS)  
        template_height = int(float(IMAGE_THUMB_HEIGHT) * UPSCALE_FACTOR)
        
        left = 0
        upper = (res_h - template_height) / 2
        right = res_w
        lower = res_h - upper
        image = image.crop((left, upper, right, lower))
        if GIF_PATTERN.match(thumb_image.lower()):
            image.save(thumb_image, 'GIF')
        else:
            image.save(thumb_image, 'JPEG')
    
    return IMAGE_THUMB_WIDTH, IMAGE_THUMB_HEIGHT
    

def create_image_thumbnail_if_not_present (source_image, thumb_image):
    """Reads the image width and height from the given image and, if it does 
    not exist, resizes the file to the given target file keeping the original 
    aspect ratio"""
    
    if not source_image:
        raise TypeError ('source_image not set')
    if not thumb_image:
        raise TypeError ('thumb_image not set')
    if not path.exists(source_image):
        raise TypeError ('source_image does not exist')
    if not path.exists(path.dirname(thumb_image)):
        raise TypeError ('Folder for thumb_image does not exist')
    
    image = Image.open(source_image)
    width, height = image.size
    new_w, new_h, res_w, res_h = rescale_image_dimensions_to_desired_width(
                            width, height, IMAGE_THUMB_WIDTH, UPSCALE_FACTOR)
    
    if not path.exists(thumb_image):
        im = image.resize((res_w, res_h), Image.ANTIALIAS) 
        if GIF_PATTERN.match(thumb_image.lower()):
            im.save(thumb_image, 'GIF')
        else:
            im.save (thumb_image, 'JPEG')
        
    return new_w, new_h
