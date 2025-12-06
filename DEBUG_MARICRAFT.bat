@echo off
title Maricraft Debug
color 0E
cd /d "%~dp0"

echo ========================================
echo MARICRAFT DEBUG MODE
echo ========================================
echo.

echo [1] Checking Python...
python --version
if %errorlevel% neq 0 (
    echo FAIL: Python not found!
    pause
    exit /b 1
)
echo.

echo [2] Checking required packages...
echo.
python -c "import pyautogui; print('  pyautogui:', pyautogui.__version__)"
python -c "import pyperclip; print('  pyperclip: OK')"
python -c "import pygetwindow; print('  pygetwindow: OK')"
python -c "import customtkinter; print('  customtkinter:', customtkinter.__version__)"
python -c "import psutil; print('  psutil:', psutil.__version__)"
echo.

echo [3] Checking maricraft modules...
echo.
python -c "from maricraft import constants; print('  constants: OK')"
python -c "from maricraft import settings; print('  settings: OK')"
python -c "from maricraft import commands; print('  commands: OK')"
python -c "from maricraft import automator; print('  automator: OK')"
python -c "from maricraft import datapack; print('  datapack: OK')"
python -c "from maricraft import version; print('  version: OK')"
python -c "from maricraft.ui import App; print('  ui (new): OK')"
echo.

echo [4] Checking config directory...
python -c "from maricraft.ui.state import get_config_dir; print('  Config dir:', get_config_dir())"
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
