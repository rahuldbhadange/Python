@echo off

set INCLUDES=%~1

if "%INCLUDES%" == "" (
  set INCLUDES=rrps setup.py
)

..\..\..\3rd\python3\static_checks\run.cmd flake8.cfg ..\..\..\3rd\python3\static_checks\pylint.rc.recommended %INCLUDES%