@echo off
REM ============================================================
REM  SAP Job Application Full Pipeline — Harsh Madan
REM  Runs all steps sequentially every day at 9 AM IST
REM ============================================================
cd /d "C:\Users\madan\OneDrive\Desktop\Linkdin Job Application"
set PYTHON="C:\Users\madan\AppData\Local\Python\bin\python.exe"

echo.
echo ============================================================
echo   SAP PIPELINE START — %DATE% %TIME%
echo ============================================================

echo.
echo [STEP 1] Apify LinkedIn Scrape...
%PYTHON% -u apify_scrape.py
echo   Done.

echo.
echo [STEP 2] Send Tailored Emails to Recruiters...
%PYTHON% -u send_sap_emails.py --all
echo   Done.

echo.
echo [STEP 3] LinkedIn Easy Apply...
%PYTHON% -u linkedin_easy_apply.py
echo   Done.

echo.
echo [STEP 4] Naukri Auto-Apply...
%PYTHON% -u naukri_auto_apply.py
echo   Done.

echo.
echo [STEP 5] Job Board Scrape (IIMJobs, Hirist, Instahyre, Indeed)...
%PYTHON% -u jobboard_apply.py
echo   Done.

echo.
echo [STEP 6] Headhunter Firm Outreach...
%PYTHON% -u headhunter_outreach.py --all
echo   Done.

echo.
echo [STEP 7] Direct Company/CIO Outreach...
%PYTHON% -u company_outreach.py --all
echo   Done.

echo.
echo [STEP 8] Telegram SAP Group Monitor...
%PYTHON% -u telegram_monitor.py
echo   Done.

echo.
echo [STEP 9] LinkedIn Auto-Post (Mondays only)...
%PYTHON% -u linkedin_autoposter.py
echo   Done.

echo.
echo ============================================================
echo   PIPELINE COMPLETE — %DATE% %TIME%
echo ============================================================
