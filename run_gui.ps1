# Image Description Toolkit - Windows Setup Script (PowerShell)
# This script installs the required dependencies and runs the GUI application

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Image Description Toolkit - Windows Setup" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python is installed: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing GUI dependencies..." -ForegroundColor Yellow
Write-Host ""

# Install GUI requirements
try {
    pip install -r gui_requirements.txt
    if ($LASTEXITCODE -ne 0) {
        throw "pip install failed"
    }
    Write-Host ""
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Write-Host "Please check your internet connection and try again" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check if Ollama is running
Write-Host "Checking if Ollama is running..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -Method GET -TimeoutSec 5 -UseBasicParsing
    Write-Host "Ollama is running and accessible!" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "WARNING: Ollama is not running or not accessible" -ForegroundColor Yellow
    Write-Host "Please ensure Ollama is installed and running" -ForegroundColor Yellow
    Write-Host "Download from: https://ollama.com" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can install a vision model with:" -ForegroundColor Yellow
    Write-Host "  ollama pull moondream" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "The GUI will start anyway, but image processing won't work without Ollama" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to continue"
}

Write-Host ""
Write-Host "Starting Image Description Toolkit GUI..." -ForegroundColor Green
Write-Host ""

# Run the GUI application
try {
    python image_description_gui.py
    if ($LASTEXITCODE -ne 0) {
        throw "GUI application failed"
    }
    Write-Host ""
    Write-Host "GUI application closed normally" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "ERROR: Failed to start the GUI application" -ForegroundColor Red
    Write-Host "Please check the error messages above" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Read-Host "Press Enter to exit"
