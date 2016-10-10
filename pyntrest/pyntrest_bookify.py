"""TODO"""
from pyntrest_io import (read_optional_album_metadata, findfiles,
    convert_url_path_to_local_filesystem_path, get_html_content)
from pyntrest import pyntrest_config

def generate_view_context(pyntrest_handler):
    """TODO"""
    
    local_albumpath_abs = convert_url_path_to_local_filesystem_path(
                  pyntrest_handler.main_images_path, '/')
    album_title, _, _, _, _, _ = read_optional_album_metadata (
         local_albumpath_abs, pyntrest_config.META_INI_FILE_PATTERN)
    
    intro_files = findfiles(local_albumpath_abs, 
                          pyntrest_config.INTRO_MD_FILE_PATTERN)
    blog_files = findfiles(local_albumpath_abs, 
                          pyntrest_config.TEXT_MD_FILE_PATTERN)
    txt_files = intro_files + blog_files
    txt_files = sorted(txt_files, key=None, reverse=True)
    
    content = []
    for txt_file in txt_files:
        if 'Gute_Reise' in txt_file:
            continue

        html_content, _ = get_html_content(txt_file)
        content.append(html_content)
    
    full_html = '\n'.join(content)
    #print full_html
    
    context = { 'page_title': album_title, 'full_html': full_html }
    return context
