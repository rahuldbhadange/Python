@echo off

if "%VIRTUAL_ENV%"=="" (
  echo VIRTUAL_ENV variable not set, please activate your virtual environment before running this script.
  echo ---
  echo One time virtual environment creation:
  echo python -mvenv %%HOME%%\envs\rrpsdev
  echo ---
  echo Virtual environment activation:
  echo %%HOME%%\envs\rrpsdev\Scripts\activate
  exit /b 1
)

python -m pip install --upgrade pip

pip install -e rrps.dt.api.fielddata -e rrps.dt.events -f ..\..\deps
if %errorlevel% neq 0 (
    echo An error occurred linking API and events %%d , please check the output above.
    exit /b %errorlevel%
  )

for /d %%d in (rrps.dt.integrator*) do (
  pip install -e %%d -f ..\..\deps
  if %errorlevel% neq 0 (
    echo An error occurred linking integrator package %%d , please check the output above.
    exit /b %errorlevel%
  )
)  