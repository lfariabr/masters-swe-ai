#!/usr/bin/env python3
"""
EigenAI Launcher
Automatically creates virtual environment and launches the application
"""
import subprocess
import sys
import os
import venv
from pathlib import Path

def check_python_version():
    """Ensure Python 3.9+ is installed"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def setup_venv():
    """Create and activate virtual environment if needed"""
    script_dir = Path(__file__).parent
    venv_dir = script_dir / ".venv"
    
    # Check if already in a venv
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Already running in virtual environment")
        return sys.executable
    
    # Create venv if it doesn't exist
    if not venv_dir.exists():
        print("📦 Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
        print("✅ Virtual environment created")
    
    # Determine venv python path
    if sys.platform == "win32":
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:
        venv_python = venv_dir / "bin" / "python3"
    
    return str(venv_python)

def install_dependencies(python_path):
    """Install required packages in virtual environment"""
    print("\n📦 Checking dependencies...")
    
    # Get the directory of this script
    script_dir = Path(__file__).parent
    requirements_file = script_dir / "requirements.txt"
    
    # Check if streamlit is installed
    result = subprocess.run(
        [python_path, "-c", "import streamlit"],
        capture_output=True
    )
    
    if result.returncode != 0:
        print("📥 Installing dependencies from requirements.txt...")
        subprocess.check_call([python_path, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install all dependencies from requirements.txt
        if requirements_file.exists():
            subprocess.check_call([python_path, "-m", "pip", "install", "-r", str(requirements_file)])
            print("✅ All dependencies installed successfully")
        else:
            # Fallback: install manually if requirements.txt is missing
            subprocess.check_call([python_path, "-m", "pip", "install", "streamlit", "matplotlib", "numpy", "sympy"])
            print("✅ Dependencies installed successfully")
    else:
        print("✅ Dependencies already installed")

def launch_app(python_path):
    """Launch the Streamlit application"""
    print("\n🚀 Launching EigenAI Portal...")
    print("=" * 60)
    print("📌 The app will open in your default web browser")
    print("📌 Press Ctrl+C to stop the application")
    print("=" * 60)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "app.py")
    
    # Launch Streamlit using venv python
    subprocess.run([python_path, "-m", "streamlit", "run", app_path])

def main():
    print("=" * 60)
    print("🧠 EigenAI - Mathematical Foundations Portal")
    print("=" * 60)
    
    check_python_version()
    venv_python = setup_venv()
    install_dependencies(venv_python)
    launch_app(venv_python)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 EigenAI closed. Thank you!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)