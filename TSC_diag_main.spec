# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['TSC_diag_main.py'],
    pathex=[],
    binaries=[],
    datas=[('Talgo_logo.png', '.')],  # tu imagen
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TSC_diag_main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    # aquí estaba el problema:
    console=False,              # ← NO consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TSC_diag_main',
)
