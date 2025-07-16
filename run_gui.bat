@echo off
REM Image Description Toolkit - Windows Setup Script
REM This script installs the required dependencies and runs the GUI application

echo.
echo ===============================================
echo Image Description Toolkit - Windows Setup
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo Python is installed. Checking version...
python --version

echo.
echo Installing GUI dependencies...
echo.

REM Install GUI requirements
pip install -r gui_requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

REM Offer to create desktop shortcut
echo Would you like to create a desktop shortcut? (y/n)
set /p createShortcut=
if /i "%createShortcut%"=="y" (
    echo Creating desktop shortcut...
    python create_shortcut.py
    echo.
)

REM Check if Ollama is running
echo Checking if Ollama is running...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Ollama is not running or not accessible
    echo Please ensure Ollama is installed and running
    echo Download from: https://ollama.com
    echo.
    echo You can install a vision model with:
    echo   ollama pull moondream
    echo.
    echo The GUI will start anyway, but image processing won't work without Ollama
    echo.
    pause
)

echo.
echo Starting Image Description Toolkit GUI...
echo.

REM Run the GUI application
python image_description_gui.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start the GUI application
    echo Please check the error messages above
    echo.
    pause
    exit /b 1
)

echo.
echo GUI application closed normally
echo.
pause
