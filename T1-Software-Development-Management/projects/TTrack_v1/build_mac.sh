echo "[*] Building TTrack with PyInstaller..."
rm -rf build/ dist/
python3 -m PyInstaller TTrack.spec
echo "[*] Build complete! Check the 'dist' folder."