@echo off
title Maricraft
cd /d "%~dp0"

:: Quick dependency check (silent)
python -c "import customtkinter" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo Missing dependencies! Running installer...
    echo.
    call INSTALL.bat
    if %errorlevel% neq 0 exit /b 1
)

echo Starting Maricraft...
echo.

python -m maricraft

echo.
echo ========================================
if %errorlevel% neq 0 (
    echo ERROR: Something went wrong!
    echo Error code: %errorlevel%
    echo.
    echo Try running DEBUG_MARICRAFT.bat for details.
) else (
    echo Maricraft closed normally.
)
echo ========================================
echo.
echo Press any key to close this window...
pause >nul
