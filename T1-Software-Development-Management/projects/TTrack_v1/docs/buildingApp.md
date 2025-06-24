### 🔧 Building the Application

#### Prerequisites
- Python 3.8+
- pip
- PyInstaller (`pip install pyinstaller`)

#### Building on macOS
```bash
# Make the build script executable
chmod +x build_mac.sh

# Run the build script
./build_mac.sh

# The application bundle will be created in the 'dist' folder
open dist/TTrack.app
```

#### Building on Windows
1. Run the build script:
   ```
   build.bat
   ```
2. The executable will be available in the 'dist' folder

#### Distribution
- The built application is self-contained and can be distributed as-is
- For macOS, the application is bundled as `TTrack.app`
- For Windows, the application is built as `TTrack.exe`