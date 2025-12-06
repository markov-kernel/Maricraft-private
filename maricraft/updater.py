"""Auto-update functionality for Maricraft."""

from __future__ import annotations

import hashlib
import os
import sys
import subprocess
import tempfile
import urllib.request
import urllib.error
from pathlib import Path
from typing import Callable, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .version import UpdateInfo

from .constants import UPDATE_DOWNLOAD_TIMEOUT, UPDATE_MIN_EXE_SIZE


def get_current_exe_path() -> Optional[Path]:
    """Get the path to the currently running executable.

    Returns None if running from Python scripts (not frozen).
    """
    if getattr(sys, 'frozen', False):
        return Path(sys.executable)
    return None


def is_frozen() -> bool:
    """Check if running as a PyInstaller bundle."""
    return getattr(sys, 'frozen', False)


def get_download_path() -> Path:
    """Get a safe temporary path for downloading the update."""
    temp_dir = Path(tempfile.gettempdir())
    return temp_dir / "MariCraft_update.exe"


def get_backup_path(exe_path: Path) -> Path:
    """Get the backup path for the old executable."""
    return exe_path.with_suffix('.exe.bak')


def download_update(
    url: str,
    dest_path: Path,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    chunk_size: int = 8192,
) -> Tuple[bool, str]:
    """Download the update file with progress reporting.

    Args:
        url: URL to download from
        dest_path: Where to save the downloaded file
        progress_callback: Optional callback(downloaded_bytes, total_bytes)
        chunk_size: Size of download chunks

    Returns:
        Tuple of (success: bool, error_message: str)
    """
    try:
        request = urllib.request.Request(
            url,
            headers={'User-Agent': 'Maricraft-Updater/1.0'}
        )

        with urllib.request.urlopen(request, timeout=UPDATE_DOWNLOAD_TIMEOUT) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0

            with open(dest_path, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)

                    if progress_callback:
                        progress_callback(downloaded, total_size)

        return True, ""

    except urllib.error.HTTPError as e:
        return False, f"Download failed: HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, f"Connection failed: {e.reason}"
    except Exception as e:
        return False, f"Download error: {str(e)}"


def verify_hash(file_path: Path, expected_hash: str) -> Tuple[bool, str]:
    """Verify SHA256 hash of downloaded file.

    Args:
        file_path: Path to the file to verify
        expected_hash: Expected SHA256 hash (hex string)

    Returns:
        Tuple of (success: bool, error_message: str)
    """
    try:
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)

        actual_hash = sha256.hexdigest().lower()
        expected_hash = expected_hash.lower()

        if actual_hash == expected_hash:
            return True, ""
        else:
            return False, f"Hash mismatch: expected {expected_hash[:16]}..., got {actual_hash[:16]}..."

    except Exception as e:
        return False, f"Hash verification error: {str(e)}"


def create_updater_script(
    current_exe: Path,
    new_exe: Path,
    backup_exe: Path,
    pid: int,
) -> Path:
    """Create a batch script to perform the file swap.

    The script:
    1. Waits for the current process to exit (by PID)
    2. Creates a backup of the old exe
    3. Moves the new exe into place
    4. Launches the new exe
    5. Cleans up the backup and itself

    Args:
        current_exe: Path to current executable
        new_exe: Path to downloaded new executable
        backup_exe: Path for backup
        pid: Process ID of the running Maricraft instance

    Returns:
        Path to the created batch script
    """
    script_path = Path(tempfile.gettempdir()) / "maricraft_update.bat"

    script_content = f'''@echo off
setlocal enabledelayedexpansion

:: Maricraft Auto-Updater
:: This script is auto-generated and will self-delete

echo.
echo ========================================
echo   Maricraft Auto-Updater
echo ========================================
echo.

:: Wait for the main application to exit (by PID)
echo Waiting for Maricraft to close (PID: {pid})...
:waitloop
timeout /t 1 /nobreak >nul
tasklist /FI "PID eq {pid}" 2>nul | find /i "{pid}" >nul
if not errorlevel 1 goto waitloop

echo Maricraft closed. Proceeding with update...
echo.

:: Small delay to ensure file handles are released
timeout /t 2 /nobreak >nul

:: Create backup of old executable
echo Creating backup...
if exist "{backup_exe}" del /f /q "{backup_exe}"
if exist "{current_exe}" (
    move /y "{current_exe}" "{backup_exe}"
    if errorlevel 1 (
        echo ERROR: Could not backup old version.
        echo Please close any programs using MariCraft and try again.
        pause
        goto cleanup
    )
)

:: Move new executable into place
echo Installing new version...
move /y "{new_exe}" "{current_exe}"
if errorlevel 1 (
    echo ERROR: Could not install new version.
    echo Restoring backup...
    move /y "{backup_exe}" "{current_exe}"
    pause
    goto cleanup
)

echo.
echo ========================================
echo   Update successful!
echo ========================================
echo.

:: Clean up backup
echo Cleaning up...
if exist "{backup_exe}" del /f /q "{backup_exe}"

:: Relaunch Maricraft
echo Launching Maricraft...
start "" "{current_exe}"

:cleanup
:: Delete this script (uses a trick: cmd.exe releases the file after reading)
del /f /q "%~f0" >nul 2>&1
exit
'''

    script_path.write_text(script_content, encoding='utf-8')
    return script_path


def launch_updater_and_exit(script_path: Path) -> None:
    """Launch the updater script and exit the application.

    This function does not return - it exits the current process.
    """
    # Launch the batch script in a new console window
    CREATE_NEW_CONSOLE = 0x00000010

    subprocess.Popen(
        ['cmd.exe', '/c', str(script_path)],
        creationflags=CREATE_NEW_CONSOLE,
        close_fds=True,
    )

    # Exit the application
    sys.exit(0)


def perform_update(
    update_info: "UpdateInfo",
    progress_callback: Optional[Callable[[str, int, int], None]] = None,
) -> Tuple[bool, str]:
    """Perform the complete update installation process.

    This should be called after the update has already been downloaded.
    It verifies the hash, creates the updater script, and launches it.

    Args:
        update_info: Information about the update
        progress_callback: Optional callback(stage: str, current: int, total: int)

    Returns:
        Tuple of (success: bool, error_message: str)
        Note: On success, this function does not return (exits to updater script)
    """
    def report(stage: str, current: int = 0, total: int = 100):
        if progress_callback:
            progress_callback(stage, current, total)

    # Step 1: Verify we're running as a frozen executable
    current_exe = get_current_exe_path()
    if current_exe is None:
        return False, "Auto-update only works when running as MariCraft.exe"

    # Step 2: Check download exists
    download_path = get_download_path()
    if not download_path.exists():
        return False, "Update file not found. Please try again."

    # Step 3: Verify file size
    if download_path.stat().st_size < UPDATE_MIN_EXE_SIZE:
        download_path.unlink()
        return False, "Downloaded file appears corrupted (too small)"

    # Step 4: Verify SHA256 hash
    report("Verifying download...", 10, 100)
    if update_info.sha256:
        success, error = verify_hash(download_path, update_info.sha256)
        if not success:
            download_path.unlink()
            return False, f"Security check failed: {error}"

    # Step 5: Create the updater script
    report("Preparing installation...", 50, 100)
    backup_path = get_backup_path(current_exe)

    try:
        script_path = create_updater_script(current_exe, download_path, backup_path, os.getpid())
    except Exception as e:
        download_path.unlink()
        return False, f"Could not create updater script: {e}"

    # Step 6: Launch updater and exit
    report("Installing update...", 90, 100)

    # This will exit the application
    launch_updater_and_exit(script_path)

    # This line should never be reached
    return True, ""


def download_update_async(
    update_info: "UpdateInfo",
    on_complete: Callable[[bool, str], None],
    on_progress: Optional[Callable[[int, int], None]] = None,
) -> None:
    """Download update in background thread.

    Args:
        update_info: Information about the update
        on_complete: Callback(success: bool, error: str) when done
        on_progress: Optional callback(downloaded: int, total: int)
    """
    import threading

    def do_download():
        if not update_info.exe_download_url:
            on_complete(False, "No download URL available")
            return

        dest_path = get_download_path()

        # Clean up any previous partial download
        if dest_path.exists():
            try:
                dest_path.unlink()
            except Exception:
                pass

        success, error = download_update(
            update_info.exe_download_url,
            dest_path,
            progress_callback=on_progress
        )

        on_complete(success, error)

    thread = threading.Thread(target=do_download, daemon=True)
    thread.start()


def is_update_downloaded() -> bool:
    """Check if an update has been downloaded and is ready to install."""
    download_path = get_download_path()
    return download_path.exists() and download_path.stat().st_size >= UPDATE_MIN_EXE_SIZE


def cleanup_downloaded_update() -> None:
    """Remove any downloaded update file."""
    download_path = get_download_path()
    if download_path.exists():
        try:
            download_path.unlink()
        except Exception:
            pass
