@echo off
REM Quick Test and Fix Script for Image Description Toolkit GUI

echo.
echo ================================================
echo Image Description Toolkit - Quick Test and Fix
echo ================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Python is available: 
python --version
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r gui_requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Running GUI tests...
python test_gui.py

pause
