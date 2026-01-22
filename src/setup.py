'''Contains packaging information about nwversioninfofiles.py.'''

# GLOBAL MODULES
from setuptools import setup

# INFORMATION
MODULE_ALIAS : str = "nwvinfo"
MODULE_NAME : str = "nwversioninfofiles"
MODULE_VERSION : str = "1.0.0"

# SETUP
if __name__ == "__main__":
    setup(
        name = MODULE_NAME,
        version = MODULE_VERSION,
        description = "An application that facilitates the creation of Version Info Files for PyInstaller.",
        author = "numbworks",
        url = f"https://github.com/numbworks/{MODULE_NAME}",
        py_modules = [ MODULE_NAME ],
        install_requires = [
            "pyinstaller==6.11.1"
        ],
        python_requires = ">=3.12",
        license = "MIT"
    )