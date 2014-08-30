"""Pyntrest wrapper for operations using Python image library (PIL)""" 

from PIL import Image
from os import path
from re import compile 
from pyntrest_config import IMAGE_THUMB_WIDTH, IMAGE_THUMB_HEIGHT

UPSCALE_FACTOR = 1.75
"""If set to 1.0, image thumbs will be rescaled to the exact size as used
in the web photo album. Depending on the source images this might not look
that neat. Increase the upscale factor to make sure images are left a bit
bigger. An upscale factor of 1.5 would mean that if you want your album
thumbnail to be 400x100px the full image will be rescaled to 600x200"""
GIF_PATTERN = compile('^.*\\.gif$')
"""Pattern for GIF files"""

def upscale_value (base_value):
    """Wrapper for recurring value casting for upscaling"""
    
    return int(float(base_value) * UPSCALE_FACTOR)

def resize_and_crop_image (source_file, target_file):
    """If the target file does not exist, reads the source file and resizes 
    and crops it with the given width and height"""
    
    if not path.exists(target_file):
        
        template_width = upscale_value(IMAGE_THUMB_WIDTH)
        template_height = upscale_value(IMAGE_THUMB_HEIGHT)
        
        im = Image.open(source_file)
         
        width, height = im.size
        height = int(height * (template_width / float(width)))
        width = template_width
        im = im.resize((width, height), Image.ANTIALIAS)
        left = (width - template_width) / 2
        upper = (height - template_height) / 2
        right = width - left
        lower = height - upper
        im = im.crop((left, upper, right, lower))
        if GIF_PATTERN.match(target_file.lower()):
            im.save(target_file, 'GIF')
        else:
            im.save(target_file, 'JPEG')

def rescale_image_dimensions_to_desired_width (width, height, des_width,
                                                upscale_factor):
    """Calculates new image dimensions based on the given image's width 
    and height and the provided desired image width multiplied by the
    upscale factor"""
    
    new_width = des_width
    new_height = int(height * (float(des_width) / float(width)))
    new_width = int(float(new_width) * upscale_factor)
    new_height = int(float(new_height) * upscale_factor)
    return new_width, new_height
    
def resize_image (source_file, target_file):
    """Reads the image width and height from the given image and, if it does 
    not exist, resizes the file to the given target file keeping the original 
    aspect ratio"""
    
    if not source_file:
        raise TypeError ('source_file not set')
    if not target_file:
        raise TypeError ('target_file not set')
    if not path.exists(source_file):
        raise TypeError ('source_file does not exist')
    if not path.exists(path.dirname(target_file)):
        raise TypeError ('Folder for target_file does not exist')
    
    image = Image.open(source_file)
    width, height = image.size
    width, height = rescale_image_dimensions_to_desired_width(
                                    width, height, IMAGE_THUMB_WIDTH, UPSCALE_FACTOR )
    
    if not path.exists(target_file):
        im = image.resize((width, height), Image.ANTIALIAS) 
        if GIF_PATTERN.match(target_file.lower()):
            im.save(target_file, 'GIF')
        else:
            im.save (target_file, 'JPEG')
        
    return width, height
