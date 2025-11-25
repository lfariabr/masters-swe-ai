@echo off
title EigenAI - Mathematical Foundations Portal
color 0B

echo ============================================================
echo   EigenAI - Mathematical Foundations Portal
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python version: %PYTHON_VERSION%
echo.

echo [INFO] Checking dependencies...
python -c "import streamlit" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INSTALL] Installing Streamlit...
    python -m pip install streamlit
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install Streamlit
        pause
        exit /b 1
    )
    echo [OK] Streamlit installed successfully
) else (
    echo [OK] Streamlit is already installed
)
echo.

echo ============================================================
echo   Launching EigenAI Portal...
echo ============================================================
echo [INFO] The app will open in your default web browser
echo [INFO] Press Ctrl+C to stop the application
echo ============================================================
echo.

REM Run the application
python -m streamlit run app.py

REM If streamlit exits with error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Application encountered an error
    pause
)