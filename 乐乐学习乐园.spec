# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['kids_learning_main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'kids_game_v3',
        'kids_pinyin', 
        'kids_math',
        'kids_english',
        'kids_thinking',
        'kids_vehicles',
        'learning_data',
        'learning_base',
        'voice_config_shared',
        'word_database',
        'drawing_utils',
    ],
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
    a.binaries,
    a.datas,
    [],
    name='乐乐学习乐园',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
