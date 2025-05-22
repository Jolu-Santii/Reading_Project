# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['MUNDO_DE_LETRAS\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('MUNDO_DE_LETRAS/recursos', 'recursos/'), ('MUNDO_DE_LETRAS/ImagenesLecturas', 'ImagenesLecturas/'), ('MUNDO_DE_LETRAS/lecturas', 'lecturas/'), ('MUNDO_DE_LETRAS/lista_ejercicios', 'lista_ejercicios/'), ('MUNDO_DE_LETRAS/preguntas', 'preguntas/'), ('MUNDO_DE_LETRAS/reporte', 'reporte/')],
    hiddenimports=['PIL._tkinter_finder', 'customtkinter', 'tkinter', 'PIL', 'json', 'sqlite3'],
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
    name='Mundo_de_Letras',
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
    icon=['MUNDO_DE_LETRAS\\recursos\\book.ico'],
)
