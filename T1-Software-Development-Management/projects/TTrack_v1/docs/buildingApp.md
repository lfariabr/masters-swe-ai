### 🔧 Building the Application

#### Prerequisites
- Python 3.8+ (3.10.x recommended for best compatibility)
- pip (latest version)
- PyInstaller (`pip install pyinstaller`)
- Required libraries: `pip install -r requirements.txt`

#### Building on macOS
```bash
# First time only: Make the build script executable x
chmod +x build_mac.sh

# Install dependencies and build the app
pip install -r requirements.txt
./build_mac.sh

# Copy .env to the app bundle and open it
cp .env "dist/TTrack.app/Contents/MacOS/.env"
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
copy .env dist\.env
dist\TTrack.exe
```

#### Distribution
- The built application is self-contained and can be distributed as-is
- Each OS requires its own build process:
  - macOS: Creates `TTrack.app` in the `dist` folder
  - Windows: Creates `TTrack.exe` in the `dist` folder
- **Note**: You cannot build for Windows from macOS or vice versa. Each platform build must be performed on the respective operating system.
- For Windows, the application is built as `TTrack.exe`

#### QA macBook behavior:
1 - A random terminal window pop ups with the following writings:
Last login: Sat Jul  5 10:28:42 on ttys004
/Users/luisfaria/.zprofile:3: command not found: pyenv
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/T1-Software-Development-Management/projects/TTrack_v1/dist/TTrack ; exit;
> /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/T1-Software-Development-Management/projects/TTrack_v1/dist/TTrack ; exit;
qt.svg: Cannot open file '/Users/luisfaria/public/ttrack_app_icon.svg', because: No such file or directory
qt.svg: Cannot open file '/Users/luisfaria/public/ttrack_app_icon.svg', because: No such file or directory
2 - TTrack app opens but logo from /public/ttrack_app_icon.svg is not displayed
3 - When I click on buttons Try with Sample Data or Download the Template, app suddenly crashes
4 - If I try to upload files and process data, it happens as expected, data is processed and Results page appear with correctly expected information.

FIX:
1 - Created TTrack-macOs.spec file to use exclusively on build_mac.sh
2 - Added data directory to TTrack-macOs.spec file
3 - Rolled back tab_input to previous version and tested building again
4 - Works fine

#### QA Windows behavior:
1 - The application runs perfectly when I download from the upload artifact part:
Run actions/upload-artifact@v4
With the provided path, there will be 1 file uploaded
Artifact name is valid!
Root directory input is valid!
Beginning upload of artifact content to blob storage
Uploaded bytes 8388608
Uploaded bytes 16777216
Uploaded bytes 25165824
Uploaded bytes 33554432
Uploaded bytes 41943040
Uploaded bytes 50331648
Uploaded bytes 58720256
Uploaded bytes 67108864
Uploaded bytes 75324035
Finished uploading artifact content to blob storage!
SHA256 digest of uploaded artifact zip is 0916c5504b5051e695548832c3037a06d0f130d8cf310178207480cd8b9e934b
Finalizing artifact upload
Artifact TTrack-exe.zip successfully finalized. Artifact ID 3471654212
Artifact TTrack-exe has been successfully uploaded! Final size is 75324035 bytes. Artifact ID is 3471654212
Artifact download URL: https://github.com/lfariabr/masters-swe-ai/actions/runs/16097055928/artifacts/3471654212
2 - I noticed, however, that the logo, which should be retrieved from public folder is not being loaded

FIX:
1 - Added `resource_path` at `main.py` to deal with PyInstaller bundle