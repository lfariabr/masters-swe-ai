# info.py

import sys
import os

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and PyInstaller onefile exe.
    """
    if hasattr(sys, '_MEIPASS'):
        # Running inside a PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Running in normal dev environment
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
