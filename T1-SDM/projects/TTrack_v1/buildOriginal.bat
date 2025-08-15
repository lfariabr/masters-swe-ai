@echo off
echo [*] Building TTrack with PyInstaller for Windows...

:: Clean previous build artifacts
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

:: Run PyInstaller with the spec file
python -m PyInstaller TTrack.spec

echo [*] Build complete! Check the 'dist' folder.
echo [*] To run the application, double-click dist\TTrack.exe
