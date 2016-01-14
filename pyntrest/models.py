"""Django default module for model definition"""

from django.db import models

class AlbumImage(models.Model):
    """A single image inside an album"""
    
    type = models.CharField(max_length=10) 
    """Image type. Either img (Images), you (YouTube hooks) or txt (Text)""" 
    location =  models.FilePathField() # local path 
    modified = models.BooleanField() # last modification timestamp 
    title = models.CharField(max_length=200) # title of the image 
    description = models.CharField(max_length=5000) # short description 
    width = models.IntegerField() # thumb width
    height = models.IntegerField() # thumb height 
    youtubeid = models.CharField(max_length=20) # YouTube id (only for type 'you')
    text_content =  models.CharField(max_length=999999)
    divid = models.CharField(max_length=1000)

class Album(models.Model):
    """A web photo album"""
    
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    path = models.FilePathField()
    cover = models.FilePathField()
    width = models.IntegerField()
    height = models.IntegerField()
    reversed = models.BooleanField()
    modified = models.BooleanField()
    last_modified = models.IntegerField()

class WebPath(models.Model):
    """A relative, described web path"""
    
    title = models.CharField(max_length=200)
    path = models.CharField(max_length=200)