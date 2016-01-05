"""Django default module for model definition"""

from django.db import models

class AlbumImage(models.Model):
    """A single image inside an album"""
    
    type = models.CharField(max_length=3)
    location =  models.FilePathField()
    title = models.CharField(max_length=200)
    width = models.IntegerField()
    height = models.IntegerField()
    description = models.CharField(max_length=5000)
    modified = models.BooleanField()
    youtubeid = models.CharField(max_length=20)
    thumbnail = models.CharField(max_length=1000)
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