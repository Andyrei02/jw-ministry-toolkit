# python setup.py build
# python setup.py bdist_msi
# python setup.py build_exe


import sys
import os
from cx_Freeze import setup, Executable


description = 'The JW Ministry Toolkit is an application designed to make it easier for Jehovah`s Witnesses to create forms and spreadsheets. It provides a user-friendly interface to streamline the form creation process and other related tasks.'

additional_files = [
        ('resources/config.ini', 'resources/config.ini'),
        ('resources/font/', 'resources/font/'),
        ('resources/images/', 'resources/images/'),
        ('resources/ui_design/', 'resources/ui_design/'),
        ('resources/workbooks_dict.json', 'resources/workbooks_dict.json'),
        (os.path.join(os.path.dirname(__file__), 'venv/lib/site-packages/pymupdf'), 'lib/pymupdf')
        ]

# base="Win32GUI" should be used only for Windows GUI app
# base = None
target = Executable(
    script="main.py",
    base="Win32GUI" if sys.platform == 'win32' else None,
    target_name='JWMinistryToolkit',
    # compress=False,
    # copyDependentFiles=True,
    # appendScriptToExe=True,
    # appendScriptToLibrary=False,
    # icon="icons\\app_icon.ico",
    copyright="Copyright (C) 2023 MIT",
    # shortcutName="Jw-ministry-toolkit",
    )

build_exe_options = {
            "packages": [
                'aiohttp', 'bs4', 'lxml', 'PIL', 'fitz', 'PyPDF2', 'PyQt5', 'dotenv', 'requests'
                ],
            'includes': ['pymupdf', 'fitz'],
            'excludes': [],
            # "zip_include_packages": ["PyQt5"],
            "include_files": additional_files,
}

setup(
    name = "Jw-ministry-toolkit",
    version = "1.0",
    description = description,
    options = {'build_exe': build_exe_options},
    executables = [target]
)
