from pyntrest import pyntrest_config
from pyntrest_io import read_optional_album_metadata
from pyntrest_config import RSS_ENABLED, RSS_REFRESH_INTERVAL_SEC
from django.contrib.syndication.views import Feed
from os import walk
from os.path import dirname, abspath, getctime, join
from time import sleep, time, strftime, localtime
from re import match, sub
from threading import Thread
from datetime import datetime

rss_entries = []

class RSSItem ():

    title=''
    description=''
    link=''
    pubdate=''

class RSSFeed(Feed):

    title = 'Pyntrest'
    description = 'Pyntrest feed'
    link = ''

    def items(self):
        rss_log('Requested RSS feed (current size={})'.format(
                                len(rss_entries)))
        return rss_entries

    def item_title(self, entry):
        return entry.title

    def item_description(self, entry):
        return entry.description

    def item_link(self, entry):
        return entry.link

    def item_pubdate(self, entry):
        return datetime.fromtimestamp(entry.pubdate)

class RSSCandidate ():

    filepath = ''
    filepath_rel = ''
    isdir = ''
    type = ''
    ctime = 0
    ignored = False

    def __init__(self, filepath, isdir, album_cover=None, hide_cover=False):
        self.filepath = filepath.strip()
        self.filepath_rel = self.filepath.replace(
                abspath(pyntrest_config.YOUR_IMAGE_FOLDER), '').strip()
        self.isdir = isdir
        self.ctime = getctime(filepath)
        self.ignored = self.is_ignored(album_cover, hide_cover)

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
            self.type = 'image'
            return False
        # keep valid youtube hooks
        if match(pyntrest_config.YOUTUBE_INI_FILE_PATTERN,
                 self.filepath.lower()):
            self.type = 'youtube'
            return False
        # keep valid blog hooks
        if match(pyntrest_config.TEXT_MD_FILE_PATTERN, self.filepath.lower()):
            self.type = 'blog'
            return False
        # keep folder paths
        if self.isdir:
            self.type = 'dir'
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
        time_formatted = strftime('%d.%m.%Y-%H:%M:%S', localtime(self.ctime))
        rss_log('{} - {} - {} [{} / {}]'.format(
                dirlabel, inout, self.filepath_rel, self.ctime,
                time_formatted))

def rss_log(message):
    print '[RSS] {}'.format(message)

def rss_init ():

    if not RSS_ENABLED:
        rss_log('RSS feature disabled.')
        return
    interval = pyntrest_config.RSS_REFRESH_INTERVAL_SEC
    if pyntrest_config.RSS_REFRESH_INTERVAL_SEC < 5:
        interval = 5

    t1 = Thread(target=rss_refresh, args=(interval,))
    t1.start()

def get_main_feed():
    from pyntrest_project.urls import rss_feed
    return rss_feed

def rss_refresh(interval):

    main_images_path = abspath(pyntrest_config.YOUR_IMAGE_FOLDER)
    album_title, album_desc,_,_,_,_ = read_optional_album_metadata(
            main_images_path, pyntrest_config.META_INI_FILE_PATTERN)

    if album_title:
        get_main_feed().title = album_title
    if album_desc:
        get_main_feed().description = album_desc
    if pyntrest_config.EXTERNAL_BASE_URL:
        get_main_feed().link = pyntrest_config.EXTERNAL_BASE_URL

    rss_log('Refresh interval: {}'.format(interval))

    while True:
        rss_log('Refresh start-time: {}'.format(time()))
        candidates = []
        for dirname, _, filenames in walk(main_images_path):
            if '\.' in dirname or '/.' in dirname:
                continue

            _, _, album_cover, _, hide_cover, _ = (
                read_optional_album_metadata (dirname,
                    pyntrest_config.META_INI_FILE_PATTERN))
            folder_cand = RSSCandidate(dirname, True)
            if not folder_cand.ignored:
                candidates.append(folder_cand)
            for filename in filenames:
                absolute_path = join(dirname, filename)
                if '\.' in absolute_path or '/.' in absolute_path:
                    continue
                file_cand = RSSCandidate(absolute_path, False, album_cover,
                                         hide_cover)
                if not file_cand.ignored:
                    candidates.append(file_cand)

        candidates.sort(key=lambda x: x.ctime, reverse=False)
        chunks = create_chunks(candidates)
        update_rss_feed(chunks)

        rss_log('Refresh end-time: {}'.format(time()))
        sleep(interval)
        #break # only for developing

def update_rss_feed(chunks):
    del rss_entries[:]
    index = 1
    for chunk in reversed(chunks):
        if not chunk or len(chunk) <= 0:
            continue
        rss_item = RSSItem()
        #----------------------------------------------------------------------
        if chunk[0].type == 'dir':

            atitle = sub('^[\\\\/]+', '', chunk[0].filepath_rel)
            rss_item.title = (
                pyntrest_config.RSS_WORDING_NEW_ALBUM.format(u''+atitle))
            at, ad,_,_,_,_ = read_optional_album_metadata(
                    chunk[0].filepath, pyntrest_config.META_INI_FILE_PATTERN)
            if at:
                rss_item.title = (pyntrest_config
                    .RSS_WORDING_NEW_ALBUM.format(unicode(at)))
            if ad:
                rss_item.description = ad
            rss_item.link = to_webpath(chunk[0].filepath_rel)

        #----------------------------------------------------------------------
        elif chunk[0].type == 'image':
            if len(chunk) > 1:
                rss_item.title = (
                    pyntrest_config.RSS_WORDING_NEW_IMAGES_MULTI
                    .format(len(chunk)))
            else:
                rss_item.title = pyntrest_config.RSS_WORDING_NEW_IMAGES_SINGLE

        #----------------------------------------------------------------------
        elif chunk[0].type == 'youtube':
            if len(chunk) > 1:
                rss_item.title = (
                    pyntrest_config.RSS_WORDING_NEW_YOUTUBE_MULTI
                    .format(len(chunk)))
            else:
                rss_item.title = pyntrest_config.RSS_WORDING_NEW_YOUTUBE_SINGLE

        #----------------------------------------------------------------------
        elif chunk[0].type == 'blog':
            if len(chunk) > 1:
                rss_item.title = (
                    pyntrest_config.RSS_WORDING_NEW_BLOG_MULTI
                    .format(len(chunk)))
            else:
                rss_item.title = pyntrest_config.RSS_WORDING_NEW_BLOG_SINGLE

        #----------------------------------------------------------------------
        if chunk[0].type != 'dir':
            for subchunk in chunk:
                rss_item.description+=sub(
                                '^[\\\\/]+', '', subchunk.filepath_rel)+'<br/>'
            rss_item.link = to_webpath(dirname(chunk[0].filepath_rel))

        #----------------------------------------------------------------------
        rss_item.pubdate = chunk[0].ctime

        rss_entries.append(rss_item)
        index+=1

def create_chunks(candidates):
    chunk_width = pyntrest_config.RSS_CHUNK_WIDTH_MINS*60
    chunks = []
    current_chunk = []
    current_ts = None

    # create basic chunks by timestamp
    for candidate in candidates:
        if candidate.isdir:
            if current_chunk: # if current chunk is not empty
                chunks.append(current_chunk)
                current_chunk = []
            current_chunk.append(candidate)
            chunks.append(current_chunk)
            current_chunk = []
            current_ts = None
            continue
        if not current_ts:
            current_ts = candidate.ctime
            current_chunk.append(candidate)
        else:
            ts_diff = candidate.ctime - current_ts
            if ts_diff > chunk_width:
                chunks.append(current_chunk)
                current_chunk = []
            current_ts = candidate.ctime
            current_chunk.append(candidate)
    chunks.append(current_chunk)

    # split up chunks by type
    typed_chunks = []
    for subchunk in chunks:
        image_chunk = []
        youtube_chunk = []
        blog_chunk = []
        directory_chunk = []
        for candidate in subchunk:
            if candidate.type == 'image':
                image_chunk.append(candidate)
            elif candidate.type == 'youtube':
                youtube_chunk.append(candidate)
            elif candidate.type == 'blog':
                blog_chunk.append(candidate)
            elif candidate.type == 'dir':
                directory_chunk.append(candidate)
        if image_chunk:
            typed_chunks.append(image_chunk)
        if youtube_chunk:
            typed_chunks.append(youtube_chunk)
        if blog_chunk:
            typed_chunks.append(blog_chunk)
        if directory_chunk:
            typed_chunks.append(directory_chunk)

    print_chunks_debug(typed_chunks)

    return typed_chunks

def to_webpath ( filepath ):
    base_url = pyntrest_config.EXTERNAL_BASE_URL
    ref_url = sub('[\\\\/]+','/',filepath)
    if base_url:
        return base_url + ref_url
    return ref_url

def print_chunks_debug(chunks):
    chunk_id = 1
    for chunk in chunks:
        rss_log('CHUNK #{} ---------'.format(chunk_id))
        for candidate in chunk:
            candidate.print_debug()
        chunk_id+=1
