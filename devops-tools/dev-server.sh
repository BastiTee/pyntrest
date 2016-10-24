#!/bin/bash
[ ! -z $( command -v python3 ) ] && PYCOM="python3" || PYCOM="python"
[ -z $PYTHONPATH ] && {
    export PYTHONPATH=../bastis-python-toolbox;
} || {
    export PYTHONPATH=${PYTHONPATH}:../bastis-python-toolbox
}
echo "Using python binary: $PYCOM"
echo "Using python path:   $PYTHONPATH"
$PYCOM manage.py test && $PYCOM manage.py runserver localhost:8000

