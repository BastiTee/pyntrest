"""Django default module for model definition"""

from django.db import models

class AlbumImage(models.Model):
    """A single image inside an album"""
    
    location =  models.FilePathField()
    title = models.CharField(max_length=200)
    width = models.IntegerField()
    height = models.IntegerField()
    youtubeid = models.CharField(max_length=20)
    description = models.CharField(max_length=5000)

class Album(models.Model):
    """A web photo album"""
    
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    path = models.FilePathField()
    cover = models.FilePathField()
    width = models.IntegerField()
    height = models.IntegerField()

class WebPath(models.Model):
    """A relative, described web path"""
    
    title = models.CharField(max_length=200)
    path = models.CharField(max_length=200)