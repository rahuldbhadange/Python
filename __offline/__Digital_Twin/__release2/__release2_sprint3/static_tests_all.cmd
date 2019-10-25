@echo off

set INCLUDES=%~1

set /p input = "Choose the integrator for a static test:"
set /p input = "rrps.dt.integrator.talendtimdocument"
set /p input = "rrps.dt.integrator.talendfirmware"
set /p input = "rrps.dt.integrator.sapwarrantyrecall"

set /p integrator_static = " enter name of integrator "

echo %integrator_static% >> "integrator_static"


if "%INCLUDES%" == "" (
  set INCLUDES=setup_all.py integrator_static

)

run_all.cmd flake8.cfg.recommended pylint.rc.recommended %INCLUDES%
