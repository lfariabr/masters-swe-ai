import os
import subprocess
import sys
import webbrowser

def main():
    # Prevent recursive re-launch
    if os.environ.get("EIGENAI_LAUNCHED"):
        return

    os.environ["EIGENAI_LAUNCHED"] = "1"

    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        app_path,
        "--server.headless=false"
    ]

    print("🚀 Launching EigenAI Streamlit app...")

    try:
        # Start the Streamlit process
        process = subprocess.Popen(command)

        # Automatically open the browser once
        webbrowser.open_new("http://localhost:8501")

        # Wait for process to finish
        process.wait()

    except KeyboardInterrupt:
        print("💤 Shutting down EigenAI...")
        process.terminate()

if __name__ == "__main__":
    main()

# rm -rf build dist launcher.spec
# pyinstaller --onefile --noconsole --add-data "app.py:." --hidden-import=streamlit.runtime.scriptrunner.script_runner launcher.py
# cd dist
# ./launcher