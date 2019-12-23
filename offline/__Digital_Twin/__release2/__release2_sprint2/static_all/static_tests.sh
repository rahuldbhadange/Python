#!/bin/bash

if [ -z "$1" ]; then
    INCLUDES="rrps setup.py"
else
    INCLUDES=$*
fi

../../../3rd/python3/static_checks/run.sh flake8.cfg pylint.rc "$INCLUDES"
