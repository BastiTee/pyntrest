"""Django default module for model definition"""

from django.db import models

class AlbumImage(models.Model):
    """A single image inside an album"""
    
    type = models.CharField(max_length=10) 
    """Image type. Either img (Images), you (YouTube hooks) or txt (Text)""" 
    location =  models.FilePathField() 
    """Path to local static image""" 
    modified = models.BooleanField() 
    """Last modification timestamp as epoch"""
    title = models.CharField(max_length=200)
    """Image title"""
    description = models.CharField(max_length=5000)
    """Image short description"""
    width = models.IntegerField()
    """Thumbnail width"""
    height = models.IntegerField()
    """Thumbnail height"""
    youtubeid = models.CharField(max_length=20)
    """YouTube id (only for type 'you')"""
    text_content =  models.CharField(max_length=999999)
    """HTML text content (only for type 'txt')"""
    divid = models.CharField(max_length=1000)
    """Randomized HTML text content div id (only for type 'txt')"""
    geocoord = models.CharField(max_length=100)
    """Geo coordinates of image"""

class Album(models.Model):
    """A web photo album"""
    
    title = models.CharField(max_length=200)
    """Album title"""
    description = models.CharField(max_length=500)
    """Album short description"""
    path = models.FilePathField()
    """Path to local album""" 
    cover = models.FilePathField()
    """Album cover"""
    width = models.IntegerField()
    """Thumbnail width"""
    height = models.IntegerField()
    """Thumbnail height"""
    reversed = models.BooleanField()
    """True, if images are sorted reversed by name"""
    modified = models.BooleanField()
    """True, if images in sub album were modified in the configured timeframe"""
    last_modified = models.IntegerField()
    """Timestamp of latest modification"""

class WebPath(models.Model):
    """A relative, described web path"""
    
    title = models.CharField(max_length=200)
    """Main page title of the path"""
    path = models.CharField(max_length=200)
    """The relative web path"""
