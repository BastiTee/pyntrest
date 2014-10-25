"""Core Pyntrest handler to generate AlbumImage and Album models from 
a local folder or file"""

from os import listdir, path, walk
from shutil import copyfile
from re import sub, compile
import pyntrest_config
from pyntrest_io import (read_optional_album_metadata, mkdirs, read_youtube_ini_file,
    get_immediate_subdirectories, convert_url_path_to_local_filesystem_path,
    get_absolute_breadcrumb_filesystem_paths, read_optional_image_metadata)
from pyntrest_pil import PILHandler
from models import AlbumImage, Album, WebPath

IMAGE_FILE_PATTERN = compile('^.*\\.(png|jpg|gif)$')
"""Regex pattern to test whether local files are images""" 
META_INI_FILE_PATTERN = 'info.ini'
"""Name of the optional album information files"""
YOUTUBE_INI_FILE_PATTERN = compile('^.*\\.youtube\\.ini$')
"""Regex pattern to test if a local file is a Youtube hook"""

class PyntrestHandler ():
    """Instances of this class handle the main processing of local albums
    and images in Pyntrest"""
    
    pil_handler = None
    main_images_path = None
    static_images_path = None
    static_fullsize_path = None
    static_athumbs_path = None
    static_ithumbs_path = None 
    
    def __init__(self, main_images_path, static_images_path):
        """Constructor"""
        
        if main_images_path is None:
            raise TypeError ('main_images_path not set.')
        if static_images_path is None:
            raise TypeError ('static_images_path not set.')
        
        main_images_path = path.abspath(main_images_path)
        static_images_path = path.abspath(static_images_path)
        static_images_path = path.join(static_images_path, 'images')
        
        self.pil_handler = PILHandler (pyntrest_config.IMAGE_THUMB_WIDTH,
            pyntrest_config.IMAGE_THUMB_HEIGHT, pyntrest_config.UPSCALE_FACTOR)
        self.main_images_path = main_images_path
        self.static_images_path = static_images_path
        self.static_fullsize_path = path.join (self.static_images_path, 'full_size')
        self.static_athumbs_path = path.join (self.static_images_path, 'album_thumbs')
        self.static_ithumbs_path = path.join (self.static_images_path, 'image_thumbs')
            
    def set_main_images_path (self, main_images_path):
        """Reset main images path to another location. Used from within
        unit tests."""
        
        self.main_images_path = main_images_path
    
    def on_startup(self):
        """Called once on startup to invoke the creation of all necessary 
        thumbnails and copying all the images into the folder that serves static 
        content"""
           
        print 'Preparing Pyntrest...'
        
        global current_subdir  # declare global counter
        current_subdir = 1
        
        mkdirs (self.static_images_path)
        mkdirs (self.static_athumbs_path)
        mkdirs (self.static_ithumbs_path)
        mkdirs (self.static_fullsize_path)
    
        # Obtain number of sub directories
        number_of_subdirs = 0
        for _, _, _ in walk (self.main_images_path):
            number_of_subdirs += 1
            
        print 'Found {0} directories...'.format(number_of_subdirs)
        # Call recursive method 
        self.on_startup_prepare_folder(self.main_images_path, '/', number_of_subdirs)
        print 'Preparation of Pyntrest done...'
    
    def on_startup_prepare_folder (self, current_album_path_abs, request_path, number_of_subdirs):
        """Recursive method to send a simulated HTTP GET request to invoke 
        content creation on the related subfolder"""
        
        global current_subdir  # declare global
        
        print ('{0}/{1} :: Creating data for path \'{2}\' and virtual path \'{3}\''
               .format(current_subdir, number_of_subdirs, current_album_path_abs, request_path)) 
        current_subdir = current_subdir + 1
        self.generate_view_context(request_path)
        subdirs = get_immediate_subdirectories(current_album_path_abs)
        for subdir in subdirs:
            self.on_startup_prepare_folder(path.join (current_album_path_abs, subdir),
                                      request_path + subdir + '/', number_of_subdirs)
    
    def check_if_album_exists (self, request_path):
        """Converts the given request path to the related absolute file system
        path to the user's image folder and tests whether this folder exists."""
        
        local_albumpath_abs = convert_url_path_to_local_filesystem_path(
                  self.main_images_path, request_path)
        if (path.exists(local_albumpath_abs) and 
            path.isdir(local_albumpath_abs)):
            return True
        else:
            return False
    
    def generate_view_context(self, request_path):
        """The core "magic" method that reads the requested album filesystem path 
        related to the virtual album path from the request and obtains all 
        necessary information to create a neat web photo album"""
    
        local_albumpath_abs = convert_url_path_to_local_filesystem_path(
                  self.main_images_path, request_path)
        local_albumpath_rel = convert_url_path_to_local_filesystem_path(
                                                     '', request_path) 
        mkdirs(path.join (self.static_fullsize_path, local_albumpath_rel))
        mkdirs(path.join (self.static_ithumbs_path, local_albumpath_rel))
        
        album_title, album_description, _ = read_optional_album_metadata (
                                                            local_albumpath_abs,
                                                            META_INI_FILE_PATTERN)    
    
        # setup sub albums
        subalbums = [] 
        for subalbum_name in get_immediate_subdirectories(local_albumpath_abs):
            self.process_subalbum (subalbums, subalbum_name, local_albumpath_rel, local_albumpath_abs)
        
        # sort subalbums by path 
        subalbums = sorted(subalbums, key=lambda subalbum: subalbum.path,
                           reverse=False)
        
        # setup images
        images = []
        for image_name in listdir(local_albumpath_abs):
            self.process_subimage(images, image_name, local_albumpath_rel, local_albumpath_abs)
            
        # update image descriptions
        image_descriptions = read_optional_image_metadata(local_albumpath_abs, META_INI_FILE_PATTERN)
        for image in images:
            basename = path.basename(image.location)
            if not image_descriptions is {}:
                print basename
            try:
                image_description = image_descriptions[basename]
                #print basename
                image.description = image_description
            except KeyError:
                pass # Ignore
                                
        # sort images by path
        images = sorted(images, key=lambda albumimage: albumimage.location,
                        reverse=False)
        
        # setup breadcrumb
        breadcrumbs = []
        breadcrumb_paths = get_absolute_breadcrumb_filesystem_paths (request_path)  
        local_albumpath_abs = self.main_images_path
        path_string = ''
        for breadcrumb_path in breadcrumb_paths:
            local_albumpath_abs = path.join(local_albumpath_abs, breadcrumb_path)
            path_string = path_string + '/' + breadcrumb_path
            path_string = sub ('[/]+' , '/', path_string)
            album_title, album_description, _ = read_optional_album_metadata (local_albumpath_abs,
                                                                        META_INI_FILE_PATTERN)        
            web_path = WebPath(title=album_title, path=path_string)
            breadcrumbs.append(web_path)
        page_title = breadcrumbs[0].title
        breadcrumbs[0].title = pyntrest_config.WORDING_HOME
    
        context = { 'page_title': page_title, 'col_width': pyntrest_config.IMAGE_THUMB_WIDTH, 'col_height' : 
                   pyntrest_config.IMAGE_THUMB_HEIGHT, 'images': images,
                   'subalbums': subalbums, 'album_title' : album_title,
                   'album_description' : album_description,
                   'lang_images' : pyntrest_config.WORDING_IMAGES, 'lang_albums' : pyntrest_config.WORDING_ALBUM,
                   'breadcrumbs' : breadcrumbs}
        
        return context
    
    def process_subalbum (self, subalbums, subalbum_name, local_albumpath_rel, local_albumpath_abs):
        """Uses the given sub-album name and creates a Album model for it, 
        including the search for optional descriptions and album covers and 
        the creation of all necessary thumbnails. Finally it appends the Album
        to the provided sub-album list."""
              
        local_subalbumpath_abs = path.join(local_albumpath_abs, subalbum_name)
        meta_title, meta_description, meta_cover = read_optional_album_metadata (local_subalbumpath_abs,
                                                                           META_INI_FILE_PATTERN)    
        
        local_subalbumcover_abs = None
        
        # find and set cover image
        
        # If sub album cover manually set..
        if meta_cover:
            # Check for existence..  
            cover_candidate = path.join(local_subalbumpath_abs, meta_cover)
            if path.exists(cover_candidate):
                local_subalbumcover_abs = cover_candidate
        
        # if no album cover was set manually or if it did not exist...
        if not local_subalbumcover_abs:
            # ... get first in folder 
            for cover_candidate in listdir(local_subalbumpath_abs):
                if IMAGE_FILE_PATTERN.match(cover_candidate.lower()):
                    local_subalbumcover_abs = path.join(local_subalbumpath_abs,
                    cover_candidate)
                    break
        
        # If still no album cover was found then this is an empty album hence we 
        # need to let the template use a default image
        if not local_subalbumcover_abs:
            
            # setup template context
            subalbum = Album(title=meta_title, description=meta_description,
                      path=subalbum_name, width=pyntrest_config.IMAGE_THUMB_WIDTH,
                      height=pyntrest_config.IMAGE_THUMB_HEIGHT, cover=None)    
            
        else:
            # otherwise prepare it for static serving 
            image_basename = path.basename(local_subalbumcover_abs)
            local_thumbnail_folder_abs = path.join (self.static_athumbs_path,
                                                local_albumpath_rel, subalbum_name)
            thumbnail_webpath = path.join (local_albumpath_rel, subalbum_name,
                                           image_basename)
            target_file = path.join(local_thumbnail_folder_abs, image_basename)
            mkdirs(local_thumbnail_folder_abs)
            self.pil_handler.create_album_thumbnail_if_not_present(
                                            local_subalbumcover_abs, target_file)
            
            # setup template context
            subalbum = Album(title=meta_title, description=meta_description,
                      path=subalbum_name, width=pyntrest_config.IMAGE_THUMB_WIDTH,
                      height=pyntrest_config.IMAGE_THUMB_HEIGHT,
                      cover=thumbnail_webpath)
    
        # append subalbum to context
        subalbums.append(subalbum)
    
    def process_subimage (self, images, image_name, local_albumpath_rel, local_albumpath_abs):
        """Uses the given sub-image path and creates a AlbumImage model for it, 
        including the creation of all necessary thumbnails and the check for
        whether the file is a Youtube video hook. Finally it appends the AlbumImage
        to the provided image list."""
        
        local_imagepath_abs = path.join(local_albumpath_abs, image_name)
    
        if IMAGE_FILE_PATTERN.match(local_imagepath_abs.lower()):
            
            static_fullsize_path_abs = path.join (
                    self.static_fullsize_path, local_albumpath_rel, image_name)
            static_thumb_path_abs = path.join (
                    self.static_ithumbs_path, local_albumpath_rel, image_name)
            
            # copy full size image to static folder 
            if not path.exists(static_fullsize_path_abs):
                copyfile(local_imagepath_abs, static_fullsize_path_abs)
            
            # calculate image size for masonry and copy to static folder
            width, height = self.pil_handler.create_image_thumbnail_if_not_present(
                                      local_imagepath_abs, static_thumb_path_abs)
    
            # add image to template context
            albumimage = AlbumImage(location=path.join(local_albumpath_rel,
                        image_name), title=image_name, width=width, height=height)
            images.append(albumimage)  
              
        elif YOUTUBE_INI_FILE_PATTERN.match(local_imagepath_abs):
            
            youtube_id = read_youtube_ini_file (local_imagepath_abs)
            # .75 is the fixed Youtube thumbnail width to height ratio
            thumb_height = int(float (pyntrest_config.IMAGE_THUMB_WIDTH) * 0.75) 
            albumimage = AlbumImage(location=path.join(
                        local_albumpath_rel, image_name), title=image_name,
                        width=pyntrest_config.IMAGE_THUMB_WIDTH,
                        height=thumb_height, youtubeid=youtube_id)
            images.append(albumimage)
