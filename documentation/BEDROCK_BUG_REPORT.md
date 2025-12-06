# Bedrock Edition Detection Bug Report

**Date:** 2025-12-06
**Status:** RESOLVED
**Priority:** High
**Root Cause:** User has GDK (Xbox App/Launcher) version, not Microsoft Store UWP version

---

## Problem Summary

Maricraft fails to detect Minecraft Bedrock Edition in two areas:
1. **Runtime detection**: Not detecting when Bedrock is the active window
2. **World discovery**: Not finding Bedrock worlds in the Install Datapack dialog

---

## User's Environment

| Property | Value |
|----------|-------|
| **Window Title** | `Minecraft` (just "Minecraft", no version) |
| **App Name** | `Minecraft.Windows` |
| **Exe Path** | `C:\XboxGames\Minecraft for Windows\Content\Minecraft.Windows.exe` |
| **Saves Path** | `C:\Users\marin\AppData\Roaming\Minecraft Bedrock\...` |
| **Installation Type** | Xbox Game Pass / Minecraft Launcher (NOT Microsoft Store) |

---

## Issue 1: Window Detection

### Current Code
**File:** `maricraft/ui/app.py` (line 253-284)

```python
def _detect_bedrock_window(self) -> bool:
    """Check if Minecraft Bedrock Edition is the active window."""
    try:
        import re
        import pygetwindow as gw

        active = gw.getActiveWindow()
        if active and active.title:
            title = active.title.strip()

            # Explicit Bedrock indicators
            if "for Windows" in title:
                return True

            # Java Edition has version number: "Minecraft 1.20.1" or "Minecraft* 1.21.1"
            java_pattern = r"^Minecraft\*?\s+\d+\.\d+"
            if re.match(java_pattern, title):
                return False  # It's Java Edition

            # Title is exactly "Minecraft" (no version) = Bedrock
            if title == "Minecraft":
                return True

    except Exception:
        pass
    return False
```

### What We Tried

| Attempt | Code | Result |
|---------|------|--------|
| 1. Check for "Minecraft for Windows" | `return "Minecraft for Windows" in title` | FAILED - Title is just "Minecraft" |
| 2. Check for exact "Minecraft" title | `if title == "Minecraft": return True` | FAILED - Still not detecting |
| 3. Regex to exclude Java (has version) | `r"^Minecraft\*?\s+\d+\.\d+"` | FAILED - Still not detecting |

### Possible Causes

1. **`pygetwindow` not returning correct title** - The library may not be getting the UWP app window correctly
2. **UWP apps have different window handling** - Xbox/Microsoft Store apps may use different window classes
3. **Active window detection failing** - `gw.getActiveWindow()` may return None or wrong window
4. **Exception being silently caught** - The try/except may be hiding the real error

### Debugging Needed

Add logging to see what's actually happening:
```python
def _detect_bedrock_window(self) -> bool:
    try:
        import pygetwindow as gw
        active = gw.getActiveWindow()
        print(f"DEBUG: Active window = {active}")
        print(f"DEBUG: Title = {active.title if active else 'None'}")
        # ... rest of code
    except Exception as e:
        print(f"DEBUG: Exception = {e}")
    return False
```

### Alternative Approaches to Try

1. **Check process name instead of window title:**
   ```python
   import psutil
   for proc in psutil.process_iter(['name']):
       if 'Minecraft.Windows' in proc.info['name']:
           return True
   ```

2. **Use win32gui directly (Windows API):**
   ```python
   import win32gui
   hwnd = win32gui.GetForegroundWindow()
   title = win32gui.GetWindowText(hwnd)
   ```

3. **Check window class name:**
   ```python
   import win32gui
   hwnd = win32gui.GetForegroundWindow()
   class_name = win32gui.GetClassName(hwnd)
   # UWP apps have class "ApplicationFrameWindow"
   ```

---

## Issue 2: World Discovery

### Current Code
**File:** `maricraft/datapack.py` (line 179-228)

```python
def get_all_bedrock_worlds_paths() -> List[Path]:
    """Get all Bedrock Edition worlds directories on Windows."""
    paths = []

    # 1. Microsoft Store / UWP installation
    localappdata = os.environ.get("LOCALAPPDATA")
    if localappdata:
        uwp_path = (
            Path(localappdata) / "Packages" /
            "Microsoft.MinecraftUWP_8wekyb3d8bbwe" /
            "LocalState" / "games" / "com.mojang" / "minecraftWorlds"
        )
        if uwp_path.exists():
            paths.append(uwp_path)

    # 2. Xbox Game Pass / Minecraft Launcher installation
    appdata = os.environ.get("APPDATA")
    if appdata:
        gamepass_path = (
            Path(appdata) / "Minecraft Bedrock" / "games" / "com.mojang" / "minecraftWorlds"
        )
        if gamepass_path.exists():
            paths.append(gamepass_path)

        # Also check without 'games' subfolder
        alt_gamepass_path = (
            Path(appdata) / "Minecraft Bedrock" / "minecraftWorlds"
        )
        if alt_gamepass_path.exists() and alt_gamepass_path not in paths:
            paths.append(alt_gamepass_path)

    return paths
```

### What We Tried

| Attempt | Path Checked | Result |
|---------|--------------|--------|
| 1. Microsoft Store path | `%LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\...\minecraftWorlds` | FAILED - User has Xbox install |
| 2. Xbox Game Pass path | `%APPDATA%\Minecraft Bedrock\games\com.mojang\minecraftWorlds` | FAILED - Still not found |
| 3. Alternative path | `%APPDATA%\Minecraft Bedrock\minecraftWorlds` | FAILED - Still not found |

### User's Actual Path

From user's log file location:
```
C:/Users/marin/AppData/Roaming/Minecraft Bedrock/logs/ContentLog2025-12-06_13-05-55
```

This suggests saves might be at:
```
C:/Users/marin/AppData/Roaming/Minecraft Bedrock/games/com.mojang/minecraftWorlds
```
OR
```
C:/Users/marin/AppData/Roaming/Minecraft Bedrock/minecraftWorlds
```

### Debugging Needed

1. **Verify the actual worlds path:**
   - Ask user to navigate to their Bedrock worlds folder
   - Get exact path where `levelname.txt` files exist

2. **Add logging to path detection:**
   ```python
   def get_all_bedrock_worlds_paths():
       print(f"DEBUG: APPDATA = {os.environ.get('APPDATA')}")
       print(f"DEBUG: LOCALAPPDATA = {os.environ.get('LOCALAPPDATA')}")

       # Check each path
       for path in potential_paths:
           print(f"DEBUG: Checking {path} - exists: {path.exists()}")
   ```

---

## Known Bedrock Installation Paths

| Installation Method | Worlds Path |
|---------------------|-------------|
| **Microsoft Store (UWP)** | `%LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds` |
| **Xbox Game Pass** | `%APPDATA%\Minecraft Bedrock\games\com.mojang\minecraftWorlds` (unconfirmed) |
| **Minecraft Launcher** | Unknown - may vary |
| **Xbox App install to custom folder** | `C:\XboxGames\...` - saves location unknown |

---

## Files Modified

| File | Changes Made |
|------|--------------|
| `maricraft/ui/app.py` | Updated `_detect_bedrock_window()` with regex pattern |
| `maricraft/datapack.py` | Added `get_all_bedrock_worlds_paths()` for multiple paths |
| `maricraft/datapack.py` | Updated `list_bedrock_worlds()` to check all paths |
| `maricraft/datapack.py` | Updated `get_all_minecraft_instances()` to add all Bedrock instances |
| `maricraft/ui/components/install_dialog.py` | Added Bedrock-specific imports and logic |

---

## Next Steps

1. **Add debug logging** to both window detection and path detection
2. **Ask user to provide:**
   - Exact path to their Bedrock worlds folder
   - Screenshot of window title bar
   - Output from debug logging
3. **Consider using Windows-specific APIs** (`win32gui`, `win32process`) instead of `pygetwindow`
4. **Test with actual Bedrock installation** to verify paths

---

## Related Code Locations

- Window detection: `maricraft/ui/app.py:253-301`
- Path detection: `maricraft/datapack.py:179-228`
- World listing: `maricraft/datapack.py:231-262`
- Instance listing: `maricraft/datapack.py:265-324`
- Install dialog: `maricraft/ui/components/install_dialog.py`

---

## RESOLUTION (2025-12-06)

### Root Cause

The user has the **GDK (Game Development Kit) version** of Minecraft Bedrock, installed via Xbox App/Launcher. This version:
- Has executable at `C:\XboxGames\Minecraft for Windows\Content\Minecraft.Windows.exe`
- Stores saves in `%APPDATA%\Minecraft Bedrock\Users\{UUID}\games\com.mojang\minecraftWorlds`
- Uses different file structure than Microsoft Store UWP version

### Fix 1: Window Detection (app.py)

Replaced `pygetwindow` title-based detection with `ctypes` + `psutil` process name detection:
- Checks for `minecraft.windows.exe` process (primary)
- Falls back to `applicationframehost.exe` with title check (UWP wrapper)

### Fix 2: World Discovery (datapack.py)

Updated `get_all_bedrock_worlds_paths()` to scan GDK structure:
- Checks `%APPDATA%\Minecraft Bedrock\Users\*\games\com.mojang\minecraftWorlds`
- Iterates over user UUID folders to find all accounts' worlds
- Still supports legacy UWP path as fallback
