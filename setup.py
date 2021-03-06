"""
Creates exe or installer using cx_Freeze
Note: can only freeze for target OS on that OS.
"""

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="RAstral Rampart",
    version="2.3.0",
    description="An arcade-style space game written with Pygame",
    author="Caleb Werth & Russell Spry",
    options={
        "build_exe": {
            "packages": ["pygame"],
            "include_files": [
                "README.md",
                "LICENSE",
                "requirements.txt",
                "assets",
            ],
        }
    },
    executables=[Executable("main.py", base=base)],
)
