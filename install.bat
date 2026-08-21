@echo off
title HACKBEN Auto-Setup Launcher
color 0A
cls
echo ===================================================
echo     HACKBEN - 1-CLICK AUTO-INSTALLER & LAUNCHER
echo ===================================================
echo.

if not exist "%~dp0venv" (
    echo [1/3] Membuat Python Virtual Environment...
    python -m venv "%~dp0venv"
    echo [2/3] Mengunduh seluruh bahan dan library...
    "%~dp0venv\Scripts\python.exe" -m pip install --upgrade pip
    "%~dp0venv\Scripts\pip.exe" install -r "%~dp0requirements.txt"
    echo [3/3] Memasang Chromium Engine...
    "%~dp0venv\Scripts\playwright.exe" install chromium
)

cls
echo ===================================================
echo     MEMULAI HACKBEN AUTOMATION DASHBOARD...
echo ===================================================
"%~dp0venv\Scripts\python.exe" "%~dp0main.py"
pause
