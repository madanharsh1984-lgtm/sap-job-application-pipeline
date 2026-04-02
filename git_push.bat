@echo off
:: ============================================================
:: git_push.bat — Push latest changes to GitHub
:: Run this after every code change to the pipeline
:: Repo: https://github.com/madanharsh1984-lgtm/sap-job-application-pipeline
:: ============================================================

cd /d "C:\Users\madan\OneDrive\Desktop\Linkdin Job Application"

:: Load token from temp file if exists (avoids interactive password prompt)
set TOKEN_FILE=C:\Users\madan\AppData\Local\Temp\gh_token.txt
if exist "%TOKEN_FILE%" (
    set /p GH_TOKEN=<%TOKEN_FILE%
    git remote set-url origin https://madanharsh1984-lgtm:%GH_TOKEN%@github.com/madanharsh1984-lgtm/sap-job-application-pipeline.git
)

git add .
git status

:: Prompt for commit message
set /p MSG=Enter commit message (or press Enter for default): 
if "%MSG%"=="" set MSG=Update pipeline scripts

git commit -m "%MSG%"
git push origin main

echo.
echo Done. Changes pushed to GitHub.
pause
