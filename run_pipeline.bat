@echo off
setlocal
cd /d "%~dp0"
REM ============================================================
REM  SAP Job Application Full Pipeline — Harsh Madan
REM  Runs all steps sequentially every day at 9 AM IST
REM ============================================================
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

echo.
echo ============================================================
echo   SAP PIPELINE START — %DATE% %TIME%
echo ============================================================

echo.
echo [STEP 1] Apify LinkedIn Scrape...
%PYTHON_CMD% -u apify_scrape.py
echo   Done.

echo.
echo [STEP 2] Send Tailored Emails to Recruiters...
%PYTHON_CMD% -u send_sap_emails.py --all
echo   Done.

echo.
echo [STEP 3] LinkedIn Easy Apply...
%PYTHON_CMD% -u linkedin_easy_apply.py
echo   Done.

echo.
echo [STEP 4] Naukri Auto-Apply...
%PYTHON_CMD% -u naukri_auto_apply.py
echo   Done.

echo.
echo [STEP 5] Job Board Scrape (IIMJobs, Hirist, Instahyre, Indeed)...
%PYTHON_CMD% -u jobboard_apply.py
echo   Done.

echo.
echo [STEP 6] Headhunter Firm Outreach...
%PYTHON_CMD% -u headhunter_outreach.py --all
echo   Done.

echo.
echo [STEP 7] Direct Company/CIO Outreach...
%PYTHON_CMD% -u company_outreach.py --all
echo   Done.

echo.
echo [STEP 8] Telegram SAP Group Monitor...
%PYTHON_CMD% -u telegram_monitor.py
echo   Done.

echo.
echo [STEP 9] LinkedIn Auto-Post (Mondays only)...
%PYTHON_CMD% -u linkedin_autoposter.py
echo   Done.

echo.
echo ============================================================
echo   PIPELINE COMPLETE — %DATE% %TIME%
echo ============================================================
