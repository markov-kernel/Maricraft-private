@echo off
echo ========================================
echo Building MariCraft.exe
echo ========================================
echo.

echo Installing dependencies...
pip install pyautogui pygetwindow pyperclip pyinstaller

echo.
echo Building executable...
pyinstaller maricraft.spec --clean

echo.
echo ========================================
if exist "dist\MariCraft.exe" (
    echo BUILD SUCCESSFUL!
    echo.
    echo Your executable is at: dist\MariCraft.exe
    echo.
    echo You can copy MariCraft.exe to any Windows computer
    echo and run it without needing Python installed.
) else (
    echo BUILD FAILED - Check the output above for errors
)
echo ========================================
pause
