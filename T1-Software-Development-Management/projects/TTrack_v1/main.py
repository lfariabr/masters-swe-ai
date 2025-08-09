import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui.main_window import MainWindow
from dotenv import load_dotenv

# Load environment variables with proper path handling for PyInstaller
if hasattr(sys, '_MEIPASS'):
    # Running as PyInstaller bundle
    env_path = os.path.join(sys._MEIPASS, '.env')
    if not os.path.exists(env_path):
        # Try in the same directory as the executable
        env_path = os.path.join(os.path.dirname(sys.executable), '.env')
else:
    # Running in development
    env_path = '.env'

load_dotenv(env_path)

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('public/ttrack_app_icon.svg')))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())