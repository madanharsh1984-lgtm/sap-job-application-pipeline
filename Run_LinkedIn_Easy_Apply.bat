@echo off
setlocal
cd /d "%~dp0"
set "SCRIPT=linkedin_easy_apply.py"
set "LOG=%TEMP%\linkedin_run_log.txt"

set "PYTHON_CMD="
where python >nul 2>&1 && set "PYTHON_CMD=python"
if not defined PYTHON_CMD (
  where py >nul 2>&1 && set "PYTHON_CMD=py -3"
)

if not defined PYTHON_CMD (
  echo [ERROR] Python was not found in PATH.
  exit /b 1
)

taskkill /f /im chrome.exe /t 2>nul
taskkill /f /im chromedriver.exe /t 2>nul
ping -n 5 127.0.0.1 >nul

%PYTHON_CMD% -u "%SCRIPT%" >> "%LOG%" 2>&1
