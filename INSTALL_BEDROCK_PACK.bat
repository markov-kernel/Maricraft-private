@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   Maricraft Behavior Pack Installer
echo   For Minecraft Bedrock Edition (Windows)
echo ============================================
echo.

REM Define both possible Bedrock installation paths
set "GDK_BASE=%APPDATA%\Minecraft Bedrock\Users"
set "UWP_PATH=%LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds"

set "MC_PATH="
set "INSTALL_TYPE="

REM Check GDK path first (Xbox App/Launcher - newer installation)
if exist "%GDK_BASE%" (
    for /d %%U in ("%GDK_BASE%\*") do (
        if exist "%%U\games\com.mojang\minecraftWorlds" (
            set "MC_PATH=%%U\games\com.mojang\minecraftWorlds"
            set "INSTALL_TYPE=Xbox App/Launcher"
            goto :found_path
        )
    )
)

REM Fallback to UWP path (Microsoft Store)
if exist "%UWP_PATH%" (
    set "MC_PATH=%UWP_PATH%"
    set "INSTALL_TYPE=Microsoft Store"
    goto :found_path
)

REM Neither path found
echo ERROR: No Minecraft Bedrock installation found!
echo.
echo Checked locations:
echo - Xbox App: %GDK_BASE%\*\games\com.mojang\minecraftWorlds
echo - Microsoft Store: %UWP_PATH%
echo.
echo Make sure Minecraft Bedrock Edition is installed.
pause
exit /b 1

:found_path
echo Found Minecraft Bedrock Edition (%INSTALL_TYPE%)
echo Path: %MC_PATH%
echo.

REM Get the script's directory (where the behavior pack source is)
set "SCRIPT_DIR=%~dp0"
set "PACK_SOURCE=%SCRIPT_DIR%maricraft\resources\maricraft_behavior"

if not exist "%PACK_SOURCE%" (
    echo ERROR: Behavior pack not found at:
    echo %PACK_SOURCE%
    pause
    exit /b 1
)

echo Behavior pack source: %PACK_SOURCE%
echo.
echo ============================================
echo   Available Worlds:
echo ============================================

set count=0
for /d %%W in ("%MC_PATH%\*") do (
    set /a count+=1
    set "world_!count!=%%W"

    REM Try to get world name from levelname.txt
    if exist "%%W\levelname.txt" (
        set /p wname=<"%%W\levelname.txt"
        echo !count!. !wname!
    ) else (
        echo !count!. %%~nxW
    )
)

if %count%==0 (
    echo No worlds found!
    pause
    exit /b 1
)

echo.
echo ============================================
set /p choice="Enter world number to install pack (1-%count%): "

REM Validate choice
if "%choice%"=="" goto invalid
if %choice% LSS 1 goto invalid
if %choice% GTR %count% goto invalid

set "WORLD_PATH=!world_%choice%!"
echo.
echo Installing to: %WORLD_PATH%
echo.

REM Create behavior_packs folder if needed
if not exist "%WORLD_PATH%\behavior_packs" (
    mkdir "%WORLD_PATH%\behavior_packs"
)

REM Remove old pack if exists
if exist "%WORLD_PATH%\behavior_packs\maricraft_behavior" (
    echo Removing old version...
    rmdir /s /q "%WORLD_PATH%\behavior_packs\maricraft_behavior"
)

REM Copy new pack
echo Copying behavior pack...
xcopy /e /i /y "%PACK_SOURCE%" "%WORLD_PATH%\behavior_packs\maricraft_behavior" > nul

REM Update world_behavior_packs.json
set "PACKS_FILE=%WORLD_PATH%\world_behavior_packs.json"
echo Updating world_behavior_packs.json...

REM Create or update the packs file
echo [{"pack_id":"a1b2c3d4-e5f6-7890-abcd-ef1234567890","version":[2,1,0]}] > "%PACKS_FILE%"

echo.
echo ============================================
echo   Installation Complete!
echo ============================================
echo.
echo The Maricraft behavior pack has been installed.
echo.
echo Next steps:
echo 1. Start Minecraft Bedrock Edition
echo 2. Open the world you just installed to
echo 3. Make sure cheats are enabled in world settings
echo 4. Type: /reload
echo 5. Try: /function gear/super_sword
echo.
pause
exit /b 0

:invalid
echo Invalid selection!
pause
exit /b 1
