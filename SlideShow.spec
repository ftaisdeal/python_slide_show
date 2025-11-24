# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['slideshow_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PIL',
        'PIL.Image', 
        'PIL.ImageTk',
        'PIL.ExifTags',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'pathlib',
        'platform',
        'locale'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SlideShow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SlideShow',
)

app = BUNDLE(
    coll,
    name='SlideShow.app',
    icon=None,
    bundle_identifier='com.slideshow.app',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'CFBundleName': 'SlideShow',
        'CFBundleDisplayName': 'SlideShow',
        'CFBundleIdentifier': 'com.slideshow.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2025',
        'LSMinimumSystemVersion': '10.13.0',
        'LSApplicationCategoryType': 'public.app-category.graphics-design',
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeExtensions': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp'],
                'CFBundleTypeName': 'Image Files',
                'CFBundleTypeRole': 'Viewer',
                'LSHandlerRank': 'Alternate'
            }
        ]
    },
)
