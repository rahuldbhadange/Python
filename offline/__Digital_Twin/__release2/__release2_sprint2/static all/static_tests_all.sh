#!/bin/bash

if [ -z "$1" ]; then
    INCLUDES="setup_all.py"
else
    INCLUDES=$*
fi

run.sh flake8.cfg pylint.rc "$INCLUDES"
