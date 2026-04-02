@echo off
title SAP Job Application Pipeline — Full Run
echo ============================================================
echo  SAP Job Application Pipeline — Harsh Madan
echo  %DATE% %TIME%
echo ============================================================
echo.

set PYTHON="C:\Users\madan\AppData\Local\Python\bin\python.exe"
set DIR="C:\Users\madan\OneDrive\Desktop\Linkdin Job Application"
cd /d %DIR%

echo [STEP 1] Scraping LinkedIn jobs via Bright Data...
%PYTHON% -u brightdata_scrape.py
echo.

echo [STEP 2] Sending email applications to recruiter leads...
%PYTHON% -u send_sap_emails.py
echo.

echo [STEP 3] LinkedIn Easy Apply (Selenium)...
%PYTHON% -u linkedin_easy_apply.py
echo.

echo [STEP 4] Naukri Auto-Apply (Selenium)...
%PYTHON% -u naukri_auto_apply.py
echo.

echo ============================================================
echo  Pipeline complete! Check summary files for results.
echo ============================================================
pause
