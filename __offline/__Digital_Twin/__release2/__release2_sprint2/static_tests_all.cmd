@echo off

set INCLUDES=%~1

if "%INCLUDES%" == "" (
  set INCLUDES=setup_all.py rrps.dt.integrator.talendtimdocument rrps.dt.integrator.talendfirmware rrps.dt.integrator.sapwarrantyrecall
)

run_all.cmd flake8.cfg.recommended pylint.rc.recommended %INCLUDES%
