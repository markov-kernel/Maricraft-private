# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for Maricraft Windows app."""

import os
import customtkinter
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Get CustomTkinter path for bundling assets
ctk_path = os.path.dirname(customtkinter.__file__)

# Collect psutil (has compiled binaries)
psutil_datas, psutil_binaries, psutil_hiddenimports = collect_all('psutil')

a = Analysis(
    ['maricraft/__main__.py'],
    pathex=[],
    binaries=psutil_binaries,
    datas=[
        ('maricraft/resources/maricraft_datapack', 'resources/maricraft_datapack'),
        ('maricraft/resources/maricraft_behavior', 'resources/maricraft_behavior'),
        (ctk_path, 'customtkinter'),  # Bundle CustomTkinter assets
    ] + psutil_datas,
    hiddenimports=[
        'pyautogui',
        'pyperclip',
        'pygetwindow',
        'pyscreeze',
        'PIL',
        'PIL._tkinter_finder',
        'customtkinter',
        'darkdetect',  # CTk dependency
    ] + psutil_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MariCraft',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window - GUI only
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='assets/icon.ico',  # Uncomment when you have an icon
)
