### 🔧 Building the Application

#### Prerequisites
- Python 3.8+ (3.10.x recommended for best compatibility)
- pip (latest version)
- PyInstaller (`pip install pyinstaller`)
- Required libraries: `pip install -r requirements.txt`

#### Building on macOS
```bash
# First time only: Make the build script executable
chmod +x build_mac.sh

# Install dependencies if not already installed
pip install -r requirements.txt

# Run the build script
./build_mac.sh

# The application bundle will be created in the 'dist' folder
open dist/TTrack.app
```

#### Building on Windows
```cmd
# Install dependencies if not already installed
pip install -r requirements.txt

# Run the build script
build.bat

# The executable will be available in the 'dist' folder
# Run it by double-clicking dist\TTrack.exe
```

#### Distribution
- The built application is self-contained and can be distributed as-is
- Each OS requires its own build process:
  - macOS: Creates `TTrack.app` in the `dist` folder
  - Windows: Creates `TTrack.exe` in the `dist` folder
- **Note**: You cannot build for Windows from macOS or vice versa. Each platform build must be performed on the respective operating system.
- For Windows, the application is built as `TTrack.exe`