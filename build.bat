@echo off
title Maricraft Build
color 0B

echo ========================================
echo Building MariCraft.exe
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python first.
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
echo.
python -m pip install --upgrade pyautogui pygetwindow pyperclip customtkinter pyinstaller --quiet
if %errorlevel% neq 0 (
    echo Warning: Some packages may have failed. Continuing anyway...
)

echo.
echo [2/3] Verifying dependencies...
python -c "import pyautogui, pygetwindow, pyperclip, customtkinter; print('All dependencies OK')"
if %errorlevel% neq 0 (
    echo ERROR: Missing dependencies. Run INSTALL.bat first.
    pause
    exit /b 1
)

echo.
echo [3/3] Building executable...
echo.
pyinstaller maricraft.spec --clean --noconfirm

echo.
echo ========================================
if exist "dist\MariCraft.exe" (
    echo BUILD SUCCESSFUL!
    echo.
    echo Your executable is at: dist\MariCraft.exe
    echo.
    echo You can copy MariCraft.exe to any Windows computer
    echo and run it without needing Python installed.
    echo.
    echo File size:
    for %%A in ("dist\MariCraft.exe") do echo   %%~zA bytes (%%~zA / 1048576 = MB approx)
) else (
    echo BUILD FAILED - Check the output above for errors
    echo.
    echo Common fixes:
    echo   1. Run INSTALL.bat first
    echo   2. Close any running MariCraft.exe
    echo   3. Delete the 'build' and 'dist' folders and try again
)
echo ========================================
echo.
pause
