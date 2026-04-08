@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM start-saas.bat — One-click launcher for the JobAccelerator AI SaaS platform
REM ═══════════════════════════════════════════════════════════════════════════
REM Double-click this file or run it from CMD inside the project folder.
REM Requires: Docker Desktop installed and running.
REM ═══════════════════════════════════════════════════════════════════════════

echo.
echo ============================================================
echo   JobAccelerator AI — SaaS Platform Launcher
echo ============================================================
echo.

REM Check Docker is available
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH.
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit /b 1
)

REM Check Docker daemon is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Desktop is not running.
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)

REM Create .env from template if it doesn't exist
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo Created .env from .env.example
    ) else (
        echo SECRET_KEY=auto-generated-key-%RANDOM%%RANDOM%> .env
        echo Created .env with auto-generated SECRET_KEY
    )
)

REM Set SECRET_KEY if not already in environment
if "%SECRET_KEY%"=="" (
    set SECRET_KEY=local-dev-key-%RANDOM%%RANDOM%
)

echo Starting all services...
echo.
echo   Frontend:    http://localhost:3000
echo   Backend API: http://localhost:8000
echo   Swagger:     http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop all services.
echo.

docker-compose up --build
