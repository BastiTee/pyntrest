#!/usr/bin/env python

from os import environ, path
import sys
import shutil
    
def import_modules_with_check (module_names):
    """Checks if a given set of modules exists. Returns a boolean that
    indicates the import success and a list of failed module names"""
    
    success = True
    failed_modules = []
    for module_name in module_names:
        try:
            map(__import__, [module_name])
        except ImportError:
            success = False
            failed_modules.append(module_name)
            
    return success, failed_modules

if __name__ == "__main__":
    
    environ.setdefault("DJANGO_SETTINGS_MODULE", "pyntrest_project.settings")
    
    is_test = False
    if len(sys.argv) == 2 and sys.argv[1] == 'test':
        is_test = True

    # Check for depending packages if this is not a unit test run        
    if not is_test:
        import_success, failed_modules = import_modules_with_check(
                                                 [ 'PIL', 'django.http' ])
        if not import_success:
            print ('Sorry, but there are some packages missing: '
                   + '{0}\nPlease refer to README.md to find out what ' + 
                   'you\'ve missed.').format(failed_modules)
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
        
