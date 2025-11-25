# ===========================================
# Assessment 3 - Release Build (Manual Steps)
# Matches Assessment 2B submission structure
# ===========================================

# 1. Go to Assessment3 folder
cd /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2025-T2/T2-MFA/assignments/Assessment3

# 2. Clean previous builds
rm -rf temp_source temp_build MFA501_Assessment3_Set3Problem1_Faria_Luis.zip

# 3. Create sourceCode.zip first
mkdir -p temp_source/eigenai

# Copy all eigenai files INTO the eigenai folder
cp ../../projects/eigenai/run_eigenai.sh temp_source/eigenai/
cp ../../projects/eigenai/run_eigenai.bat temp_source/eigenai/
cp ../../projects/eigenai/run_eigenai.py temp_source/eigenai/
cp ../../projects/eigenai/app.py temp_source/eigenai/
cp ../../projects/eigenai/requirements.txt temp_source/eigenai/
cp ../../projects/eigenai/README.md temp_source/eigenai/
cp -r ../../projects/eigenai/resolvers temp_source/eigenai/
cp -r ../../projects/eigenai/views temp_source/eigenai/
cp -r ../../projects/eigenai/assets temp_source/eigenai/

# Make executable
chmod +x temp_source/eigenai/run_eigenai.sh

# Clean __pycache__
find temp_source -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Create the sourceCode.zip
cd temp_source
zip -r ../MFA501_Assessment3_Set3Problem1_sourceCode_Faria_Luis.zip eigenai/ -x "*.pyc" -x "*__pycache__*"
cd ..

# Clean up temp
rm -rf temp_source

# 4. Create temp folder for final ZIP
mkdir -p temp_build

# 5. Copy all submission files to temp_build
cp MFA501_Assessment3_Set3Problem1_sourceCode_Faria_Luis.zip temp_build/
cp MFA501_Assessment3_releaseBuild_Faria_Luis.txt temp_build/MFA501_Assessment3_Set3Problem1_releaseBuild_Faria_Luis.txt
cp MFA501_Assessment3_code_Faria_Luis.txt temp_build/MFA501_Assessment3_Set3Problem1_codeForAi_Faria_Luis.txt

# Copy report files (if ready)
cp MFA501_Assessment3_Set3Problem1_report_Faria_Luis.docx temp_build/ 2>/dev/null || echo "⚠️  report.docx not found"
cp MFA501_Assessment3_Set3Problem1_report_Faria_Luis.pdf temp_build/ 2>/dev/null || echo "⚠️  report.pdf not found"

# Copy demo video (if ready)
cp MFA501_Assessment3_Set3Problem1_demo_Faria_Luis.mp4 temp_build/ 2>/dev/null || echo "⚠️  demo.mp4 not found"

# 6. Create final submission ZIP
cd temp_build
zip -r ../MFA501_Assessment3_Set3Problem1_Faria_Luis.zip * -x "*.DS_Store"
cd ..

# 7. Clean up
rm -rf temp_build MFA501_Assessment3_Set3Problem1_sourceCode_Faria_Luis.zip

# 8. Verify the result
echo "✅ Created: MFA501_Assessment3_Set3Problem1_Faria_Luis.zip"
unzip -l MFA501_Assessment3_Set3Problem1_Faria_Luis.zip

# ===========================================
# Test (Optional)
# ===========================================

# Extract to test folder
unzip MFA501_Assessment3_Set3Problem1_Faria_Luis.zip -d test_extraction

# Extract sourceCode.zip
cd test_extraction
unzip MFA501_Assessment3_Set3Problem1_sourceCode_Faria_Luis.zip

# Test the app
cd eigenai
./run_eigenai.sh

# Clean up test
cd ../../..
rm -rf test_extraction

# ===========================================
# Final Structure
# ===========================================
# MFA501_Assessment3_Set3Problem1_Faria_Luis.zip
# ├── MFA501_Assessment3_Set3Problem1_demo_Faria_Luis.mp4
# ├── MFA501_Assessment3_Set3Problem1_sourceCode_Faria_Luis.zip
# │   └── eigenai/
# │       ├── run_eigenai.sh
# │       ├── run_eigenai.bat
# │       ├── run_eigenai.py
# │       ├── app.py
# │       ├── requirements.txt
# │       ├── README.md  ← Stays inside eigenai!
# │       ├── resolvers/
# │       ├── views/
# │       └── assets/
# ├── MFA501_Assessment3_Set3Problem1_report_Faria_Luis.docx
# ├── MFA501_Assessment3_Set3Problem1_report_Faria_Luis.pdf
# ├── MFA501_Assessment3_Set3Problem1_codeForAi_Faria_Luis.txt
# └── MFA501_Assessment3_Set3Problem1_releaseBuild_Faria_Luis.txt