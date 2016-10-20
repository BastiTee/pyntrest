@echo off
SETLOCAL
SET PYTHONPATH=%PYTHONPATH%;../bastis-python-toolbox
python manage.py test
python manage.py runserver localhost:8000
ENDLOCAL
