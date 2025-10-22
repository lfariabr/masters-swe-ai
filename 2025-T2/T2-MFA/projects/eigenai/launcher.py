import os
import sys
import subprocess

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp dir
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

    subprocess.Popen(command, shell=True)
    print("🌐 Streamlit is starting... open http://localhost:8501")

if __name__ == "__main__":
    main()


# rm -rf build dist launcher.spec
# pyinstaller --onefile --noconsole --add-data "app.py:." --hidden-import=streamlit.runtime.scriptrunner.script_runner launcher.py
# cd dist
# ./launcher