@echo off
title Maricraft Debug
cd /d "%~dp0"

echo ========================================
echo MARICRAFT DEBUG MODE
echo ========================================
echo.

echo Checking Python...
python --version
echo.

echo Checking packages...
python -c "import pyautogui; print('pyautogui:', pyautogui.__version__)"
python -c "import pyperclip; print('pyperclip: OK')"
python -c "import pygetwindow; print('pygetwindow: OK')"
echo (Using native Win32 clipboard API - no extra dependencies needed)
echo.

echo Checking maricraft modules...
python -c "from maricraft import constants; print('constants: OK')"
python -c "from maricraft import settings; print('settings: OK')"
python -c "from maricraft import commands; print('commands: OK')"
python -c "from maricraft import automator; print('automator: OK')"
python -c "from maricraft import ui; print('ui: OK')"
echo.

echo ========================================
echo Starting Maricraft with full error output...
echo ========================================
echo.

python -m maricraft

echo.
echo ========================================
echo Exit code: %errorlevel%
echo ========================================
echo.
pause
