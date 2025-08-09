@echo off
setlocal enabledelayedexpansion

echo [*] TTrack Windows Build Process Starting...
echo [*] %date% %time%

:: Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Error: Python not found. Please install Python 3.8+ and add to PATH.
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [+] Using Python %PYTHON_VERSION%

:: Check for PyInstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [!] PyInstaller not found. Installing...
    python -m pip install PyInstaller
    if errorlevel 1 (
        echo [!] Error: Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo [+] PyInstaller installed successfully
) else (
    echo [+] PyInstaller already installed
)

:: Verify dependencies
echo [*] Verifying dependencies...
python -c "import PyQt5, pandas, openpyxl, dotenv, supabase" >nul 2>&1
if errorlevel 1 (
    echo [!] Some dependencies missing. Installing from requirements.txt...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [!] Error: Failed to install dependencies
        pause
        exit /b 1
    )
)
echo [+] All dependencies verified

:: Clean previous build artifacts
echo [*] Cleaning previous build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: Build the application
echo [*] Building TTrack application...
python -m PyInstaller TTrack.spec --noconfirm
if errorlevel 1 (
    echo [!] Error: PyInstaller build failed
    pause
    exit /b 1
)

echo [+] Build completed successfully

:: Copy .env.example for user setup
echo [*] Setting up environment template...
if exist .env.example (
    copy .env.example "dist\.env.example" >nul
    echo [+] Copied .env.example to dist folder
) else (
    echo [!] Warning: .env.example not found
)

:: Create setup instructions
echo [*] Creating user setup instructions...
(
echo # TTrack Setup Instructions
echo.
echo ## Database Configuration
echo 1. Copy `.env.example` to `.env` in the same directory as TTrack.exe
echo 2. Edit `.env` with your Supabase credentials:
echo    ```
echo    SUPABASE_URL=https://your-project.supabase.co
echo    SUPABASE_KEY=your-anon-key-here
echo    ```
echo 3. Save and run TTrack.exe
echo.
echo ## Security Note
echo Never share your .env file - it contains your private database credentials.
) > "dist\SETUP.md"

echo [+] Created user setup instructions
echo [+] Build process complete!
echo.
echo Distribution files:
echo   [+] dist\TTrack.exe (main application)
echo   [+] dist\SETUP.md (user setup guide)
echo   [+] dist\.env.example (credential template)
echo.
echo To test the build:
echo   1. Copy your .env to: dist\.env
echo   2. Run: dist\TTrack.exe
echo.
pause
