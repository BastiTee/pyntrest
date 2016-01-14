![Pyntrest-Logo](doc/images/logo.png)
> Automated web photo albums for convenience lovers

[![Build Status](https://travis-ci.org/BastiTee/pyntrest.png)](https://travis-ci.org/BastiTee/pyntrest)

Pyntrest is a Python/Django-based application that automatically generates a fully fledged web photo album from a local folder without the necessity to do boring stuff like setting up databases, content management systems or creating thumbnails. Pyntrest is for convenience lovers like me. 

### The basics

* Pyntrest uses a local folder and assumes that each (sub-) folder is a web photo album 
* It will automatically scan for images and create web photo albums on request 
* Web photo albums are browsable just like on your disk
* Albums and images are presented in fancy Pintrest-like canvas
* It's responsive and minimalistic 
* It lazy-loads images which is nice for the user's bandwidth

### The optional stuff

* An info.ini file can be created per web photo album to provide more information such as title, description, a cover image and details for individual photos or videos
* It supports embedding YouTube videos by providing the youtube id of the video in a text file or the filename itself.
* Anything that Pyntrest relies on will be generated but if you decide to you can create thumbnails etc. yourself

For folder or file management, i.e., the actual content management, you can use whatever you want to use (Dropbox, Drive, FTP, etc.) I, for example, use Dropbox to synchronize a folder on my webspace with my mobile device. If the image arrives at the webspace's folder, Pyntrest automatically detects the picture and it's instantly available on the corresponding web photo album. The same applies to new subalbums, optional album info files or youtube hooks.

## How to start

Basic instructions are as follows:

* Install Python 2.7.x
* Clone or download Pyntrest
* Go to the downloaded folder and run `pip install -r requirements.txt` (assuming you have [pip](https://pypi.python.org/pypi/pip) installed, Attention: On unix you also need to have `gcc` and `python-devel` packages installed in order to compile `pillow`)
* If that does not work, then manually install [Django web framework](https://pypi.python.org/pypi/Django) and [Pillow](https://pypi.python.org/pypi/Pillow) (please refer to `requirements.txt` for correct versions, you can also use PIL instead of Pillow if you prefer)
* _Recommended_: Run `python manage.py test` to test the installation (see next chapter for possible solutions on errors)
* Run `python manage.py runserver` (on image folders with lots of images this will take a while since Pyntrest performs a startup scan of your folder and creates all the necessary thumbnails)
* Open `http://localhost:8000` in a browser and enjoy

What you should see is a web photo album that is automatically generated from the local folder `<pyntrest>/sample_images`. Of course you can also use your own images and brandings. For that please refer to `<pyntrest>/pyntrest/pyntrest_config.py` and change the settings as you desire. Pyntrest is fully compatible with wsgi servers like unicorn or Apache using mod_wsgi. Hence it is possible to use it in combination with production servers. 

## Options for folders 

Subfolders and/or the root of your local image folder can be enriched and configured by providing an `info.ini` file (see  `<pyntrest>/sample_images` for some examples. The following options can be set. 

### AlbumInfo Section 

In the album info section you can provide detailed information about your image. The section is labeled `[AlbumInfo]`. After the section label you can provide various options in the form `<Key>=<Value>` to configure the album. Valid options are:

* `Title` - Title of the album. Will appear in the album header. 
* `Description` - Short description of the album. Will appear in the album header. 
* `CoverImage` - Image to be used as album cover. If not set, the first image will be used. If no image is available, then a placeholder will be created. 
* `HideCover` - Allowed values are `True` or `False`. If set to true, the cover image will not appear within the sub album. If not set or set to false, the default (cover not hidden) will be used.  
* `ReverseImages` - Allowed values are `True` or `False`. If set to true, the album images will be sorted in descending order. If not set or set to false, the default (ascending order) will be used. This has no effect on the folders within the album.
* `ModifiedAlbumsOnTop` - Allowed values are `True` or `False`. If set to true, the sub album folders will be sorted so that the album is on top that was modified or created last. If not set or set to false, the default order (ascending by name) will be used. This has no effect on the images within the album.

```
[AlbumInfo]
Title=Pyntrest
Description=Automated web photo albums for convenience lovers
CoverImage=im-001.jpg
HideCover=False
ReverseImages=True
ModifiedAlbumsOnTop=False
```

### ImageInfo Section 

In the image info section you can provide details for individual photos. The section is labeled `[ImageInfo]`. After the section label you can simply provide `<Image-Filename>=<Your-Description>` to add an image description. 

```
[ImageInfo]
image-01.jpg=My favourite image! 
im-0041.youtube.ini=This funny video was made in 2009. 
image-02.jpeg=Oh! Look at Johnnys face :) 
```

## Common problems on startup

 * If tests fail with an error like the one below, then you need to install `libjpeg-devel` for your platform and rerun the Pillow installation 

```
E.........EEEE.E
======================================================================
ERROR: test (pyntrest_tests.test_pyntrest_core.CoreTestSuite)
----------------------------------------------------------------------
Traceback (most recent call last):
  ...
IOError: decoder jpeg not available
```

## Project info

Pyntrest relies on a number of awesome open source projects:

* [Python](https://www.python.org/)
* [Django web framework](https://pypi.python.org/pypi/Django)
* [Pillow - Python Image Library (PIL) fork](https://pypi.python.org/pypi/Pillow)
* [markdown2 - Markdown in Python](https://github.com/trentm/python-markdown2)
* [jQuery](http://jquery.com/)
* [Masonry - Cascading grid layout library](http://masonry.desandro.com/)
* [fancyBox - Fancy jQuery Lightbox Alternative](http://fancyapps.com/fancybox/)
* [jQuery Lazy - Delayed image loading plugin for jQuery](http://jquery.eisbehr.de/lazy/)
* [jQuery Lazy - Delayed image loading plugin for jQuery](http://jquery.eisbehr.de/lazy/)
* [FontAwesome - The iconic font and CSS toolkit](http://fontawesome.io)
* [html5-boilerplate](https://github.com/h5bp/html5-boilerplate)
    
Furthermore I've incorporated numerous images for testing purposes. All those images are licensed under [CC0 1.0 Universal (CC0 1.0) ](http://creativecommons.org/publicdomain/zero/1.0/) and were fetched at http://unsplash.com/

Pyntrest is licensed under [Apache Licence v2](http://www.apache.org/licenses/LICENSE-2.0.html). 

## Screenshots

Below you find the latest screenshots of Pyntrest.

![Overview](doc/images/latest-screenshot-1.jpg)
![Image overlay](doc/images/latest-screenshot-2.jpg)
![Video overlay](doc/images/latest-screenshot-3.jpg)

