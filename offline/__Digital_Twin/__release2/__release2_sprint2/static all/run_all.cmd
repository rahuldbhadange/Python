@echo off

pip install flake8 pylint

set BASEDIR=%~dp0

set FLAKE8CFG=%~1
set PYLINTCFG=%~2

echo flake8 %FLAKE8CFG%
echo pyline %PYLINTCFG%

shift
shift

set files= 
:loop
if [%1]==[] goto endloop
set files=%files% %1
shift
goto loop
:endloop
echo Arguments %files%

set FLAKE8_PYTHONPATH=%BASEDIR%\flake8\lib:%PYTHONPATH%
set PYLINT_PYTHONPATH=%BASEDIR%\pylint\lib:%PYTHONPATH%

echo === flake8 ===
set PYTHONPATH=%FLAKE8_PYTHONPATH%
python -s -mflake8 --config %FLAKE8CFG% %files%

echo === pylint ===
set PYTHONPATH=%PYLINT_PYTHONPATH%
python -s -mpylint --rcfile=%PYLINTCFG% %files%