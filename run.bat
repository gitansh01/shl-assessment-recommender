@echo off
REM ==========================================
REM SHL Assessment Recommender - Windows Batch
REM ==========================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo  SHL Assessment Recommender - Setup
echo ========================================
echo.

REM Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

echo [1/4] Installing dependencies...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

echo.
echo [2/4] Installing Playwright browsers...
python -m playwright install >nul 2>&1
echo [OK] Playwright ready

echo.
echo [3/4] Building embedding index...
python scripts/build_index.py --catalog data/catalog.json --index data/index.pkl
if errorlevel 1 (
    echo [ERROR] Failed to build index
    pause
    exit /b 1
)
echo [OK] Embedding index built

echo.
echo ========================================
echo [4/4] Starting API server...
echo ========================================
echo.
echo Server starting at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Test endpoint (in another terminal):
echo   curl http://localhost:8000/health
echo.
echo Or run tests:
echo   python test_chat.py
echo.
echo Press Ctrl+C to stop server
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
