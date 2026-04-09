@echo off
setlocal
cd /d "%~dp0"
title SAP Job Application Pipeline — Full Run
echo ============================================================
echo  SAP Job Application Pipeline — Harsh Madan
echo  %DATE% %TIME%
echo ============================================================
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

echo [STEP 1a] Scraping LinkedIn jobs via Bright Data...
%PYTHON_CMD% -u brightdata_scrape.py
echo.

echo [STEP 1b] Searching for recruiter posts with emails (DDG/Bing search)...
%PYTHON_CMD% -u brightdata_posts_scrape.py
echo.

echo [STEP 1c] Finding company HR emails for job records (known email lookup)...
%PYTHON_CMD% -u find_company_emails.py
echo.

echo [STEP 2] Sending email applications to recruiter leads...
%PYTHON_CMD% -u send_sap_emails.py
echo.

echo [STEP 3] LinkedIn Easy Apply (Playwright)...
%PYTHON_CMD% -u linkedin_easy_apply.py
echo.

echo [STEP 4] Naukri Auto-Apply (Playwright)...
%PYTHON_CMD% -u naukri_auto_apply.py
echo.

echo ============================================================
echo  Pipeline complete! Check summary files for results.
echo ============================================================
pause
