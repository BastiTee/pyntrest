#!/usr/bin/env python3

from os import environ, path, chdir
import sys
import shutil

# change to manage.py's folder
abspath = path.abspath(__file__)
dname = path.dirname(abspath)
chdir(dname)

if __name__ == "__main__":

    from bptbx import b_iotools

    environ.setdefault("DJANGO_SETTINGS_MODULE", "pyntrest_project.settings")

    import_success, failed_modules = b_iotools.import_modules_with_check(
                                                 [ 'PIL', 'django.http',
                                                 'markdown2', 'bs4' ])
    if not import_success:
        print ('Sorry, but there are some packages missing: '
               + '{0}\nPlease refer to README.md to find out what '
               + 'you\'ve missed or, assuming you have \'pip\' installed,\n'
               + 'run \'pip install -r requirements.txt\''
               ).format(failed_modules)
        exit(1)

    # this needs to be done here because why want to check for missing
    # packages first
    from django.core.management import execute_from_command_line

    # Create default configuration if not available
    basic_config_file = path.abspath(
                        path.join('pyntrest', 'pyntrest_config.py'))
    basic_config_file_default = path.abspath(
                        path.join('pyntrest', 'pyntrest_config.py.default'))
    if not path.exists(basic_config_file):
        shutil.copy(basic_config_file_default, basic_config_file)

    # Startup the server
    execute_from_command_line(sys.argv)
