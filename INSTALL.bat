@echo off
title Maricraft Installer
color 0A

echo ========================================
echo    MARICRAFT INSTALLER / UPDATER
echo ========================================
echo.

:: Check if Python is already installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo.
    echo Please install Python first:
    echo 1. Go to https://www.python.org/downloads/
    echo 2. Click "Download Python"
    echo 3. Run the installer
    echo 4. IMPORTANT: Check "Add Python to PATH" at the bottom!
    echo 5. Restart your computer
    echo 6. Run this INSTALL.bat again
    echo.
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

echo ========================================
echo Installing/Updating packages...
echo ========================================
echo.

:: Install all required packages
echo Installing pyautogui...
python -m pip install --upgrade pyautogui --quiet 2>nul
if %errorlevel% neq 0 (
    python -m pip install --upgrade pyautogui --user --quiet 2>nul
)

echo Installing pygetwindow...
python -m pip install --upgrade pygetwindow --quiet 2>nul
if %errorlevel% neq 0 (
    python -m pip install --upgrade pygetwindow --user --quiet 2>nul
)

echo Installing pyperclip...
python -m pip install --upgrade pyperclip --quiet 2>nul
if %errorlevel% neq 0 (
    python -m pip install --upgrade pyperclip --user --quiet 2>nul
)

echo Installing customtkinter (modern UI)...
python -m pip install --upgrade customtkinter --quiet 2>nul
if %errorlevel% neq 0 (
    python -m pip install --upgrade customtkinter --user --quiet 2>nul
)

echo Installing psutil (Bedrock detection)...
python -m pip install --upgrade psutil --quiet 2>nul
if %errorlevel% neq 0 (
    python -m pip install --upgrade psutil --user --quiet 2>nul
)

echo.
echo ========================================
echo Verifying installation...
echo ========================================
echo.

set INSTALL_OK=1

python -c "import pyautogui; print('[OK] pyautogui')" 2>nul
if %errorlevel% neq 0 (
    echo [FAIL] pyautogui
    set INSTALL_OK=0
)

python -c "import pygetwindow; print('[OK] pygetwindow')" 2>nul
if %errorlevel% neq 0 (
    echo [FAIL] pygetwindow
    set INSTALL_OK=0
)

python -c "import pyperclip; print('[OK] pyperclip')" 2>nul
if %errorlevel% neq 0 (
    echo [FAIL] pyperclip
    set INSTALL_OK=0
)

python -c "import customtkinter; print('[OK] customtkinter')" 2>nul
if %errorlevel% neq 0 (
    echo [FAIL] customtkinter
    set INSTALL_OK=0
)

python -c "import psutil; print('[OK] psutil')" 2>nul
if %errorlevel% neq 0 (
    echo [FAIL] psutil
    set INSTALL_OK=0
)

if %INSTALL_OK%==0 (
    echo.
    echo [!] Some packages failed to install.
    echo Try running: python -m pip install pyautogui pygetwindow pyperclip customtkinter psutil
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Creating desktop shortcut...
echo ========================================
echo.

:: Create/update desktop shortcut using PowerShell
powershell -Command "& {$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Maricraft.lnk'); $Shortcut.TargetPath = '%~dp0RUN_MARICRAFT.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Minecraft Command Helper'; $Shortcut.Save(); Write-Host '[OK] Desktop shortcut created/updated'}" 2>nul

echo.
echo ========================================
echo    INSTALLATION COMPLETE!
echo ========================================
echo.
echo You can now:
echo   - Double-click "Maricraft" on your desktop
echo   - Or double-click "RUN_MARICRAFT.bat" here
echo.
echo If updating: Just run Maricraft - no restart needed!
echo.
pause
