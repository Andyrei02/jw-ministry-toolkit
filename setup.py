# python setup.py build
# python setup.py bdist_msi
# python setup.py build_exe


import sys
import os
from cx_Freeze import setup, Executable


# base="Win32GUI" should be used only for Windows GUI app
# base = None
target = Executable(
    script="main.py",
    base="Win32GUI",
    # compress=False,
    # copyDependentFiles=True,
    # appendScriptToExe=True,
    # appendScriptToLibrary=False,
    # icon="icons\\app_icon.ico",
    copyright="Copyright (C) 2023 MIT",
    # shortcutName="Jw-ministry-toolkit",
    )

build_exe_options = {
            "packages": [],
            # 'excludes': [],
            "zip_include_packages": ["PyQt5"],
            "include_files": ["assets/", "config.py", "LICENSE"],
}

setup(
    name = "Jw-ministry-toolkit",
    version = "1.0",
    description = "JW Ministry Toolkit",
    options = {
          'build_exe': build_exe_options},
    executables = [target]
)
