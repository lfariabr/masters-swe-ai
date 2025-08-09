# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('services/data/sample_academic_transcript.xlsx', 'services/data'),
        ('services/data/sample_prescribed_curriculum.xlsx', 'services/data'),
        ('public/ttrack_logo.svg', 'public'),
        ('public/ttrack_app_icon.svg', 'public'),
        ('.env.example', '.'),  # Include .env.example for user reference
    ],
    hiddenimports=[
        'dotenv',
        'supabase',
        'supabase.client',
        'postgrest',
        'gotrue',
        'realtime',
        'storage3',
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
    name='TTrack',
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
app = BUNDLE(
    exe,
    name='TTrack.app',
    icon='TTrack.icns',
    bundle_identifier=None,
)