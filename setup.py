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
            "packages": ["pygame"],
            "include_files": ["README.md", "LICENSE", "CREDITS.txt", "assets"],
        }
    },
    executables=[Executable("spinny_gun.py", base=base)],
)
