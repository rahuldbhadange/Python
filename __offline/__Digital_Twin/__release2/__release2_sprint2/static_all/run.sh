#!/usr/bin/env bash
# Copyright (c) 2015 Iotic Labs Ltd. All rights reserved.

if [ "$#" -lt 3 ]; then
    echo -e "Usage: run.sh FLAKE8CFG PYLINTCFG item1 item2 ...
Where each item can be a python module of source file\n"
    exit 1
fi

FLAKE8CFG=$1
shift
PYLINTCFG=$1
shift

pushd `dirname $0` > /dev/null
BASEDIR=`pwd`
popd > /dev/null

FLAKE8_PYTHONPATH=${BASEDIR}/flake8/lib:${PYTHONPATH}
PYLINT_PYTHONPATH=${BASEDIR}/pylint/lib:${PYTHONPATH}

echo -e "\n=== flake8 ===\n"
PYTHONPATH=${FLAKE8_PYTHONPATH} /usr/bin/env python3 -s -mflake8 --config ${FLAKE8CFG} $@
RESULT=$?

echo -e "\n=== pylint ===\n"
PYTHONPATH=${PYLINT_PYTHONPATH} /usr/bin/env python3 -s -mpylint --rcfile=${PYLINTCFG} $@
RESULT=$?

grep -qrE "^# (pylint: *skip-file|flake8: *noqa)" $@
if [ "$?" -eq 0 ]; then
    >&2 echo -e "\n\n*** Warning: The following files are being ignored by flake8 and/or pylint ***"
    for i in `grep -lrE "^# (pylint: *skip-file|flake8: *noqa)" $@`; do
        >&2 echo $i
    done
    RESULT=1
fi

exit ${RESULT}
