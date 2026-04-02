@echo off
set PYTHON=C:\Users\madan\AppData\Local\Python\bin\python.exe
set SCRIPT=C:\Users\madan\OneDrive\Desktop\Linkdin Job Application\naukri_auto_apply.py
set LOG=C:\Users\madan\AppData\Local\Temp\naukri_run_log.txt

taskkill /f /im chrome.exe /t 2>nul
taskkill /f /im chromedriver.exe /t 2>nul
ping -n 5 127.0.0.1 >nul

"%PYTHON%" -u "%SCRIPT%" >> "%LOG%" 2>&1
