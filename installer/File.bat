@echo off
title Eyor Installer Environment Setup
echo 💻 Starting Eyor Environment Setup...
echo --------------------------------------

:: Run PowerShell script with Bypass policy
powershell -NoProfile -ExecutionPolicy Bypass -File "Packagesinstall.ps1"

echo.
echo ✅ Setup complete! Press any key to exit.
pause >nul
