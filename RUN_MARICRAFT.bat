@echo off
title Maricraft
cd /d "%~dp0"

echo Starting Maricraft...
echo.

python -m maricraft

echo.
echo ========================================
if %errorlevel% neq 0 (
    echo ERROR: Something went wrong!
    echo Error code: %errorlevel%
    echo.
    echo Try running INSTALL.bat again.
) else (
    echo Maricraft closed normally.
)
echo ========================================
echo.
echo Press any key to close this window...
pause >nul
