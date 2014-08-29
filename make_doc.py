"""A script using epydoc to generate a Javadoc-like API documentation
of all the toolbox core modules"""

from manage import import_modules_with_check

success, _ = import_modules_with_check ([ 'PIL', 'django.http', 'epydoc'])
if not success:
    print 'Cannot generate documentation. You need to install epydoc first!'
    exit(1) 
    
from epydoc import cli
from os import environ
import sys

environ.setdefault("DJANGO_SETTINGS_MODULE", "pyntrest_project.settings")


sys.argv = ['epydoc', '--html', '-o', 'doc/code', '--name', 
            'Pyntrest', '--url', 
            'https://github.com/BastiTee/pyntrest', 'pyntrest']
options, names = cli.parse_arguments()
cli.main(options, names)
