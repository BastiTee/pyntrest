"""Project settings for Pytnrest"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'dmg1ndqjabb*88&+sp&x))%2xrxni5u6$pq-*1xk*nvxhfao$8'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'pyntrest'
)
MIDDLEWARE_CLASSES = ()
ROOT_URLCONF = 'pyntrest_project.urls'
WSGI_APPLICATION = 'pyntrest_project.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3.pyntrest_project')
    }
}
TEMPLATE_CONTEXT_PROCESSORS = {
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request'
}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
