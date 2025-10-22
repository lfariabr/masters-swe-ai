#!/usr/bin/env python3
"""
EigenAI Launcher
Automatically checks dependencies and launches the application
"""
import subprocess
import sys
import os

def check_python_version():
    """Ensure Python 3.9+ is installed"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install required packages"""
    print("\n📦 Checking dependencies...")
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("📥 Installing Streamlit...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit installed successfully")

def launch_app():
    """Launch the Streamlit application"""
    print("\n🚀 Launching EigenAI Portal...")
    print("=" * 60)
    print("📌 The app will open in your default web browser")
    print("📌 Press Ctrl+C to stop the application")
    print("=" * 60)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "app.py")
    
    # Launch Streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])

def main():
    print("=" * 60)
    print("🧠 EigenAI - Mathematical Foundations Portal")
    print("=" * 60)
    
    check_python_version()
    install_dependencies()
    launch_app()

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