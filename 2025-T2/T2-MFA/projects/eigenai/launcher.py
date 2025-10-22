import os
import sys
import subprocess
import time

def resource_path(relative_path):
    """Get absolute path to resource (works for dev and PyInstaller)"""
    try:
        base_path = sys._MEIPASS  # temporary folder used by PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    app_path = resource_path("app.py")

    print("🚀 Launching EigenAI Streamlit app...")
    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        app_path,
        "--server.address=127.0.0.1",
        "--server.port=8501",
        "--server.headless=true"
    ]

    # Start Streamlit in the background
    subprocess.Popen(command, shell=True)

    # Give Streamlit a few seconds to start
    time.sleep(3)

    print("🌐 Streamlit should now be running — open http://localhost:8501")
    os.system("start http://localhost:8501")

if __name__ == "__main__":
    main()
