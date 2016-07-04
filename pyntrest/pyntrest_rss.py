from pyntrest_config import RSS_ENABLED, RSS_REFRESH_INTERVAL_SEC
from os import walk, path
from time import sleep, time
from threading import Thread
from re import match
from pyntrest import pyntrest_config
from pyntrest_io import read_optional_album_metadata

def rss_init ():

    if not RSS_ENABLED:
        print 'RSS feature disabled.'
        return
    interval = 5
    if RSS_REFRESH_INTERVAL_SEC < 5:
        interval = 5
        
    t1 = Thread(target=rss_refresh, args=(interval,))
    t1.start()
 
def rss_refresh(interval):
    
    main_images_path = path.abspath(pyntrest_config.YOUR_IMAGE_FOLDER)
    
    print 'RSS :: Refresh interval: {}'.format(interval)
    
    candidates = []
    while True:
        print 'RSS :: Refresh start-time: {}'.format(time())
        
        for dirname, _, filenames in walk(main_images_path):
            if '\.' in dirname:
                continue
            
            _, _, album_cover, _, hide_cover, _ = (
                read_optional_album_metadata (dirname,
                    pyntrest_config.META_INI_FILE_PATTERN))
            candidates.append(
                    RSSCandidate(dirname, True))
            for filename in filenames:
                absolute_path = path.join(dirname, filename)
                if '\.' in absolute_path:
                    continue
                candidates.append(
                    RSSCandidate(absolute_path, False, album_cover, hide_cover))
        
        print 'RSS :: Refresh end-time: {}'.format(time())
        sleep(interval)
        break # only for developing

class RSSCandidate ():
    
    filepath = ''
    filepath_rel = ''
    isdir = ''
    ctime = 0
    ignored = False
    
    def __init__(self, filepath, isdir, album_cover=None, hide_cover=False):
        self.filepath = filepath.strip()
        self.filepath_rel = self.filepath.replace(
                path.abspath(pyntrest_config.YOUR_IMAGE_FOLDER), '').strip()
        self.isdir = isdir
        self.ctime = path.getctime(filepath)
        self.ignored = self.is_ignored(album_cover, hide_cover)
        self.print_debug()
        
    def is_ignored(self, album_cover=None, hide_cover=False):
        
        # ignore root folder path 
        if self.filepath_rel == '':
            return True
        # ignore metadata files 
        if self.filepath.endswith(pyntrest_config.META_INI_FILE_PATTERN):
            return True
        # ignore intro files 
        if self.filepath.endswith(pyntrest_config.INTRO_MD_FILE_PATTERN):
            return True
        # ignore hidden cover files  
        if hide_cover and self.filepath.endswith(album_cover):
            return True
        # keep valid image files 
        if match(pyntrest_config.IMAGE_FILE_PATTERN, self.filepath.lower()):
            return False
        # keep valid youtube hooks 
        if match(pyntrest_config.YOUTUBE_INI_FILE_PATTERN, 
                 self.filepath.lower()):
            return False
        # keep valid blog hooks
        if match(pyntrest_config.TEXT_MD_FILE_PATTERN, self.filepath.lower()):
            return False
        # keep folder paths 
        if self.isdir:
            return False
        # anything else is not valid
        return True
        
    def print_debug(self):
        dirlabel = '   '
        if self.isdir:
            dirlabel = 'DIR'
        inout = '<I>'
        if not self.ignored:
            inout = '   '
        print 'RSS :: {} - {} - {} [{}]'.format(
                dirlabel, inout, self.filepath_rel, self.ctime)
        
    