@echo off
title SAP Job Application - Daily Outlook Draft Creator
echo =====================================================
echo   SAP Job Application - Outlook Draft Creator
echo =====================================================
echo.
echo  Creates Outlook drafts with tailored resumes.
echo  Nothing is sent - you review and send from Outlook.
echo.
echo  Make sure Outlook is OPEN before continuing.
echo.
pause

C:\Users\madan\AppData\Local\Python\bin\python.exe "%~dp0Create_SAP_Job_Drafts.py"

echo.
pause
