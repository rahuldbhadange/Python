@echo off

set INCLUDES=%~1

if "%INCLUDES%" == "" (
  set INCLUDES=setup.py
)

..\..\..\3rd\python3\static_checks\run.cmd ..\..\..\3rd\python3\static_checks\flake8.cfg.recommended ..\..\..\3rd\python3\static_checks\pylint.rc.recommended %INCLUDES%