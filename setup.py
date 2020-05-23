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
    name="Spinny Gun",
    version="1.0.0",
    description="test",
    options={
        "build_exe": {
            "packages": ["pygame", "dbm"],
            "include_files": ["README.md", "LICENSE", "CREDITS.txt", "assets"],
        }
    },
    executables=[Executable("main.py", base=base)],
)
