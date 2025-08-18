# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('services/data/sample_academic_transcript_v2.xlsx', 'services/data'),
        ('services/data/sample_prescribed_curriculum.xlsx', 'services/data'),
        ('public/ttrack_logo.svg', 'public'),
        ('public/ttrack_app_icon.svg', 'public'),
        ('.env.enc', '.'),  # Include encrypted environment file
    ],
    hiddenimports=[
        'cryptography',
        'cryptography.fernet',
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

# Exclude plaintext .env files from bundle for security
a.datas = [x for x in a.datas if not (x[0].endswith('.env') and not x[0].endswith('.env.enc'))]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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