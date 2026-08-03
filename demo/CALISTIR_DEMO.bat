@echo off
setlocal
cd /d "%~dp0\.."
py -3.12 demo\demo_app.py
if errorlevel 1 (
  echo.
  echo Demo baslatilamadi. Python 3.12 kurulumunu kontrol edin.
  pause
)
