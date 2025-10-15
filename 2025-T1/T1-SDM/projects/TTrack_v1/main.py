import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui.main_window import MainWindow
from cryptography.fernet import Fernet

# Encryption key - must match the one in encrypt_env.py
ENCRYPTION_KEY = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='

def load_encrypted_env():
    """Load and decrypt environment variables from .env.enc"""
    cipher = Fernet(ENCRYPTION_KEY)
    
    # Find .env.enc file (works with PyInstaller)
    if hasattr(sys, '_MEIPASS'):
        # Running as PyInstaller bundle
        env_path = os.path.join(sys._MEIPASS, '.env.enc')
    else:
        # Running in development
        env_path = '.env.enc'
    
    if not os.path.exists(env_path):
        print(f"⚠️  Warning: Encrypted environment file not found at {env_path}")
        print("   Run 'python encrypt_env.py' to create .env.enc")
        return
    
    try:
        # Read and decrypt the environment file
        with open(env_path, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = cipher.decrypt(encrypted_data).decode('utf-8')
        
        # Parse and set environment variables
        for line in decrypted_data.strip().split('\n'):
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
        
        print("✅ Environment variables loaded from encrypted file")
        
    except Exception as e:
        print(f"❌ Error loading encrypted environment: {e}")
        print("   Make sure .env.enc was created with encrypt_env.py")

# Load encrypted environment variables BEFORE any other imports that need them
load_encrypted_env()

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