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
        echo IMPORTANT: Edit .env and set SECRET_KEY to a strong random string before deploying to production.
    ) else (
        echo SECRET_KEY=CHANGE-ME-BEFORE-PRODUCTION> .env
        echo Created .env with placeholder SECRET_KEY
        echo IMPORTANT: Edit .env and set SECRET_KEY to a strong random string before deploying to production.
    )
)

REM Set SECRET_KEY for this session if not already set (local development only)
if "%SECRET_KEY%"=="" (
    set SECRET_KEY=local-dev-only-change-for-production
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
