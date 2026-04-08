@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_CMD="
where python >nul 2>&1 && set "PYTHON_CMD=python"
if not defined PYTHON_CMD (
  where py >nul 2>&1 && set "PYTHON_CMD=py -3"
)

if not defined PYTHON_CMD (
  echo [ERROR] Python was not found in PATH.
  echo Install Python 3.10+ and re-run this file.
  pause
  exit /b 1
)

echo Installing required Python packages...
%PYTHON_CMD% -m pip install python-jobspy selenium webdriver-manager python-docx requests
if errorlevel 1 (
  echo.
  echo [ERROR] Package installation failed.
  pause
  exit /b 1
)

echo.
echo Done! Press any key to close.
pause
