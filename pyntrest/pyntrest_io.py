"""Pyntrest module providing I/O helper methods involved during the processing
of album requests."""

from ConfigParser import ConfigParser
from re import sub, compile, match, search
from os import path, makedirs, listdir, walk 
from time import time
from markdown2 import Markdown

def file_exists (path):
    """Tests if a file exists"""
    
    try:
        fobj = open(path)
        fobj.close()
        return True
    except IOError:
        return False
    
def mkdirs (directory):
    """Create directory structure if it does not exist"""
    
    if not directory:
        raise TypeError('directory not provided.')
    
    directory_abs = path.abspath(directory)
    if not path.exists(directory_abs):
        makedirs(directory_abs)

def findfiles (absolute_path, filter_regex=None, doprint=False):
    """Lists all files in given directory path recursively."""
        
    filelist = []
    for dirname, _, filenames in walk(absolute_path):
        for filename in filenames:
            absolute_path = path.join(dirname, filename)
            if filter_regex != None:
                matching = match(filter_regex, absolute_path.lower())
                if matching != None:
                    filelist.append(absolute_path)
                    if (doprint): 
                        print absolute_path
            else:
                filelist.append(absolute_path)
                if (doprint): 
                    print absolute_path
    return filelist
     
def get_immediate_subdirectories(file_path):
    """Return the sub-directories of a given file path, but 
    only the first level."""
    
    if not file_path:
        raise TypeError('file_path not provided.')
    
    directories = []
    for name in listdir(file_path):
        if (path.isdir(path.join(file_path, name)) 
            and not str(name).startswith('.')):
            directories.append(name)
    directories.sort()
    return directories

def cleanup_url_path (url_path):
    """Removes redundant or unwanted symbols from the provided URL path"""
    
    if not url_path:
        url_path = '/'
    
    clean_path = sub ('[/]+', '/', url_path)
    clean_path = sub ('index.html$', '', clean_path)
    return clean_path

def convert_url_path_to_local_filesystem_path (root_filesystem_path, 
                                                 url_path):
    """Creates a file system sub-folder path from the given URL path and appends 
    it to the given root filesystem path""" 
    
    if not root_filesystem_path:
        root_filesystem_path = ''
    if not url_path:
        url_path = ''
    url_path = cleanup_url_path(url_path)
    
    url_path = sub ('^/', '', url_path)
    path_elements = url_path.split('/')
    fs_path_abs = root_filesystem_path
    for path_element in path_elements:
        fs_path_abs = path.join(fs_path_abs, path_element)
    fs_path_abs = sub('\\\\' + '$', '', fs_path_abs)
    fs_path_abs = sub('/$', '', fs_path_abs)
    return fs_path_abs

def get_absolute_breadcrumb_filesystem_paths (url_path):
    """Splits up the current URL path and returns a list of path elements"""
    
    if not url_path:
        url_path = ''
    url_path = cleanup_url_path(url_path)
    
    url_path = sub ('^/', '', url_path)
    url_path = sub ('/$', '', url_path)
    subpaths = url_path.split ('/')
    if len(subpaths) == 1 and subpaths[0] == '':
        return subpaths
    else:
        return [''] + subpaths
    
def read_optional_album_metadata (album_path, filename ):
    """Checks if a given folder contains an INFO_FILE_NAME and tries to obtain 
    optional album information from a section named 'AlbumInfo'"""
    
    if not album_path:
        album_path = ''
    album_path = path.abspath(album_path)
    if not path.exists(album_path):
        raise TypeError('album_path does not exist!')
    if not filename:
        raise TypeError('filename not provided!')
    
    info_ini_file = path.join(album_path, filename)
    
    # set default values
    album_title = path.basename(album_path)
    album_description = ''
    album_cover = None
    album_sorted_rev = False
    album_hide_cover = False
    modified_albums_on_top = False
    
    # try to read file
    if path.exists(info_ini_file):
        config = ConfigParser()
        config.read(info_ini_file)
        if config.has_option('AlbumInfo', 'Title'):
            album_title = config.get('AlbumInfo', 'Title')
        if config.has_option('AlbumInfo', 'Description'):
            album_description = config.get('AlbumInfo', 'Description')
        if config.has_option('AlbumInfo', 'CoverImage'):
            album_cover = config.get('AlbumInfo', 'CoverImage')
        if config.has_option('AlbumInfo', 'ReverseImages'):
            reverse = config.get('AlbumInfo', 'ReverseImages')
            if reverse == 'True':
                album_sorted_rev = True
        if config.has_option('AlbumInfo', 'HideCover'):
            hidecover = config.get('AlbumInfo', 'HideCover')
            if hidecover == 'True':
                album_hide_cover = True
        if config.has_option('AlbumInfo', 'ModifiedAlbumsOnTop'):
            modtop = config.get('AlbumInfo', 'ModifiedAlbumsOnTop')
            if modtop == 'True':
                modified_albums_on_top = True
        
    return (album_title, album_description, album_cover, album_sorted_rev,
            album_hide_cover, modified_albums_on_top)

def read_optional_image_metadata (album_path, filename ):
    """Checks if a given folder contains an INFO_FILE_NAME and tries to obtain 
    optional image information from a section named 'ImageInfo'"""
    
    if not album_path:
        album_path = ''
    album_path = path.abspath(album_path)
    if not path.exists(album_path):
        raise TypeError('album_path does not exist!')
    if not filename:
        raise TypeError('filename not provided!')
    
    info_ini_file = path.join(album_path, filename)
    
    # set default values
    image_infos = {}
    
    # try to read file
    if path.exists(info_ini_file):
        config = ConfigParser()
        config.read(info_ini_file)
        if config.has_section('ImageInfo'):
            options = config.options('ImageInfo')
            for option in options:
                #print 'Adding detailed info for file {0}'.format(option)
                info = config.get('ImageInfo', option).strip()
                image_infos[option.lower()] = info
        
    #print image_infos
    return image_infos

def read_youtube_ini_file ( youtube_file_name ):
    """Checks for a YouTube video information file"""

    if not youtube_file_name:
        raise TypeError('youtube_file_path not provided.')
    youtube_file_path = path.abspath(youtube_file_name)
    if not path.exists(youtube_file_path):
        raise TypeError('youtube_file_path does not exist!') 

    # first try: extract the YouTube id directly from filename 
    # in this case it must be enclosed by % %
    match_obj = search('%([^%]+)%', youtube_file_name)
    if match_obj is not None:
        youtube_id = match_obj.group(1)
        if compile(".+").match(youtube_id) is not None:
            return youtube_id

    # second try: check file for config section with youtube id     
    config = ConfigParser()
    config.read(youtube_file_path)
    if config.has_option('VideoInfo', 'YoutubeId'):
        youtube_id = config.get('VideoInfo', 'YoutubeId')
        return youtube_id
    
    # if not just return empty handed
    return ''

def is_modified ( abs_path, is_file, max_age=48, feature_enabled=False, image_file_pattern=compile('^.*$') ):
    """Check if a file was created between now and now minus the given
    max age in hours. Return false if this feature is not configured."""
    
    if not feature_enabled:
        return False
    
    oldest_epoch = time() - ( max_age * 60.0 * 60.0 )
    is_modified = False
    last_change = 0
    
    # on files just check the file .. 
    if is_file:
        if path.getctime(abs_path) >= oldest_epoch or path.getmtime(abs_path) >= oldest_epoch:
            is_modified = True
        last_change = max(path.getctime(abs_path), path.getmtime(abs_path))
    # on folders find all images file and check those for changes ( if we would just inspect
    # the folder we'll get updates, e.g., simply because the folder was touched. 
    else:
        files = findfiles( abs_path, image_file_pattern, doprint=False)
        for subfile in files:
            if path.getctime(subfile) >= oldest_epoch or path.getmtime(subfile) >= oldest_epoch:
                is_modified = True
            last_change = max(last_change, path.getctime(abs_path), path.getmtime(abs_path))
    
    return is_modified, last_change

def get_html_content (local_file_path):
    """Converts a local markdown-formatted file to HTML"""
    
    if not local_file_path:
        raise TypeError('local_file_path not provided.')
    if not path.exists(local_file_path):
        raise TypeError('local_file_path does not exist!') 
    
    with open(local_file_path, 'r') as markdown_file:
        file_content=markdown_file.read()
        markdown_file.close()
    
    markdowner = Markdown()
    # first textual line is considered as title 
    title = file_content.strip().split('\n')[0]
    # the full thing will be converted to HTML 
    file_content = markdowner.convert(file_content)

    return file_content, title