"""TODO"""
from pyntrest import pyntrest_config, pyntrest_io
import re
from os import path
from bs4 import BeautifulSoup

class BookChapter():
    """TODO"""

    title = ''
    """ - """
    html_content = ''
    """ - """
    level = 0
    """ - """
    ignore = False
    """ - """
    subchapters = []
    """ - """

def convert_to_bookchapter( absolute_path, level ):

    # album_title, album_description, album_cover, album_sorted_rev,
    # album_hide_cover, modified_albums_on_top, ignoreinbook)
    album_metadata = pyntrest_io.read_optional_album_metadata (
         absolute_path, pyntrest_config.META_INI_FILE_PATTERN)

    book_chapter = BookChapter()
    book_chapter.level = level
    book_chapter.title = album_metadata[0]
    book_chapter.subchapters = []
    book_chapter.ignore = album_metadata[6]

    subfiles = pyntrest_io.get_immediate_subfiles(absolute_path)
    content = []
    for subfile in subfiles:
        if re.match(pyntrest_config.INTRO_MD_FILE_PATTERN, subfile):
            html_content, _ = pyntrest_io.get_html_content(
                path.join(absolute_path, subfile))
            content.insert(0, html_content)
        if re.match(pyntrest_config.TEXT_MD_FILE_PATTERN, subfile):
            html_content, _ = pyntrest_io.get_html_content(
                path.join(absolute_path, subfile))
            content.append(html_content)

    book_chapter.html_content = u'\n'.join(content)

    # remove emoticons
    try:
        # Wide UCS-4 build
        myre = re.compile(u'['
            u'\U0001F300-\U0001F64F'
            u'\U0001F680-\U0001F6FF'
            u'\u2600-\u26FF\u2700-\u27BF]+',
            re.UNICODE)
    except re.error:
        # Narrow UCS-2 build
        myre = re.compile(u'('
            u'\ud83c[\udf00-\udfff]|'
            u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
            u'[\u2600-\u26FF\u2700-\u27BF])+',
            re.UNICODE)
    book_chapter.html_content = myre.sub(
        u'', book_chapter.html_content) # no emoji

    for direct in pyntrest_io.get_immediate_subdirectories(absolute_path, True):
        book_chapter.subchapters.append(
            convert_to_bookchapter(path.join(absolute_path, direct), level+1))

    return book_chapter

def assemble_full_html ( book_chapter, full_html_arr):
    if not book_chapter.ignore:
        hl = '1'
        if book_chapter.level > 0:
            hl = str(book_chapter.level)
        full_html_arr.append('<h' + hl + '>' + book_chapter.title + '</h'+hl+'>')

        # replace headings with correct level
        soup = BeautifulSoup(book_chapter.html_content, 'html.parser')
        headings = []
        for i in range(1,8):
            for heading in soup.find_all('h'+str(i)):
                headings.append(heading)
        for heading in headings:
            old_level = int(re.sub('h', '', heading.name))
            new_level = old_level + book_chapter.level
            #print '{} {}>>{}'.format(heading, old_level, new_level)
            new_tag = soup.new_tag('h' + str(new_level))
            new_tag.string = heading.string
            heading.replace_with(new_tag)
        book_chapter.html_content = soup.prettify()

        full_html_arr.append(book_chapter.html_content)
    else:
        print ('Skipped book chapter {}'.format(book_chapter.title))
    for subchapter in book_chapter.subchapters:
        assemble_full_html(subchapter, full_html_arr)
    return full_html_arr

def generate_view_context(pyntrest_handler):
    """TODO"""

    full_html_arr = []
    local_albumpath_abs = pyntrest_io.convert_url_path_to_local_filesystem_path(
          pyntrest_handler.main_images_path, '/')

    book = convert_to_bookchapter(local_albumpath_abs, 0)


    full_html_arr = assemble_full_html(book, full_html_arr)
    full_html = '\n'.join(full_html_arr)

    soup = BeautifulSoup(full_html, 'html.parser')
    for s in soup('hr'):
        s.extract()
    for s in soup('iframe'):
        s.extract()

    full_html = soup.prettify()

    context = { 'page_title': book.title, 'toc_label': 'Inhalt',
               'full_html': full_html }
    return context
