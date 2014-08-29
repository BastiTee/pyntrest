"""Contains variables that are used Pyntrest-wide"""

from os import path
import re
import pyntrest_config

IMAGE_FILE_PATTERN = re.compile(pyntrest_config.ALLOWED_IMAGE_PATTERN)
"""Regex pattern to test whether local files are images""" 
YOUTUBE_INI_FILE_PATTERN = re.compile('^.*\\.youtube\\.ini$')
"""Regex pattern to test if a local file is a Youtube hook"""
MAIN_IMAGES_PATH = path.abspath(pyntrest_config.YOUR_IMAGE_FOLDER)
"""Path of the user's image folder"""
STATIC_IMAGES_PATH = path.abspath(
                            path.join(pyntrest_config.STATIC_PATH, 'images'))
"""Path from where static images are served"""
STATIC_FULLSIZE_IMAGES_PATH = path.join (STATIC_IMAGES_PATH, 'full_size')
"""Path from where static full size images are served"""
STATIC_ALBUM_THUMBS_PATH = path.join (STATIC_IMAGES_PATH, 'album_thumbs')
"""Path from where static album thumbnails are served"""
STATIC_IMAGE_THUMBS_PATH = path.join (STATIC_IMAGES_PATH, 'image_thumbs')
"""Path from where static image thumbnails are served"""
