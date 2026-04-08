@echo off
setlocal
cd /d "%~dp0"
title Apify Account Creator — Fresh $5 Credits
echo ============================================
echo  Apify Auto Account Creator
echo  Creates a new free Apify account using a
echo  disposable GuerrillaMail email address.
echo  Each account gives $5 free monthly credits.
echo ============================================
echo.
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

%PYTHON_CMD% -u apify_account_creator.py
if errorlevel 1 (
  echo.
  echo [ERROR] apify_account_creator.py failed.
  pause
  exit /b 1
)
echo.
echo Done. Check apify_accounts.json for your new token.
pause
