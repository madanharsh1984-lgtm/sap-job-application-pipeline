@echo off
echo ============================================================
echo   SAP Daily Job Application Pipeline
echo   Step 1: JobSpy Scrape (FREE - no Apify credits needed)
echo   Step 2: Send tailored emails with resume
echo   Step 3: LinkedIn Easy Apply
echo   Step 4: Naukri Auto-Apply (Google Sign-In)
echo ============================================================
echo.

set PYTHON="C:\Users\madan\AppData\Local\Python\bin\python.exe"
set OUT_DIR="C:\Users\madan\OneDrive\Desktop\Linkdin Job Application"

:: Install python-jobspy if not present
echo Checking python-jobspy...
%PYTHON% -c "import jobspy" 2>nul
if %errorlevel% neq 0 (
    echo Installing python-jobspy...
    %PYTHON% -m pip install python-jobspy
)
echo python-jobspy OK.
echo.

:: STEP 1 - Scrape jobs with JobSpy
echo [STEP 1] Scraping LinkedIn/Indeed/Google jobs via JobSpy...
%PYTHON% "%OUT_DIR%\jobspy_scrape.py"
echo.

:: STEP 2 - Send emails
echo [STEP 2] Sending tailored emails to recruiters...
%PYTHON% "C:\Users\madan\.accio\accounts\7078444127\agents\DID-F456DA-2B0D4C\project\send_emails.py"
echo.

:: STEP 3 - LinkedIn Easy Apply
echo [STEP 3] Running LinkedIn Easy Apply...
%PYTHON% "%OUT_DIR%\linkedin_easy_apply.py"
echo.

:: STEP 4 - Naukri Auto-Apply
echo [STEP 4] Running Naukri Auto-Apply (Google Sign-In)...
%PYTHON% "%OUT_DIR%\naukri_auto_apply.py"
echo.

echo ============================================================
echo   Pipeline complete! Check logs in Output Folder.
echo ============================================================
pause
