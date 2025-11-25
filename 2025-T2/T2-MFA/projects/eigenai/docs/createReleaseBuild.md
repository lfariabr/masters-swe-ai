# Go to Assessment3 folder
cd /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2025-T2/T2-MFA/assignments/Assessment3

# Build folder for Submission
mkdir -p Assessment3_Submission_Faria_Luis

# Copy main scripts and config
cp ../../projects/eigenai/run_eigenai.sh Assessment3_Submission_Faria_Luis/
cp ../../projects/eigenai/run_eigenai.bat Assessment3_Submission_Faria_Luis/
cp ../../projects/eigenai/run_eigenai.py Assessment3_Submission_Faria_Luis/
cp ../../projects/eigenai/app.py Assessment3_Submission_Faria_Luis/
cp ../../projects/eigenai/requirements.txt Assessment3_Submission_Faria_Luis/
cp -r ../../projects/eigenai/resolvers Assessment3_Submission_Faria_Luis/
cp -r ../../projects/eigenai/views Assessment3_Submission_Faria_Luis/
cp -r ../../projects/eigenai/assets Assessment3_Submission_Faria_Luis/ 2>/dev/null || true

# Copy documentation and readme
cp MFA501_Assessment3_releaseBuild_Faria_Luis.txt Assessment3_Submission_Faria_Luis/README.txt
cp MFA501_Assessment3_code_Faria_Luis.txt Assessment3_Submission_Faria_Luis/
cp ../../projects/eigenai/docs/assessment3.md Assessment3_Submission_Faria_Luis/assessment3_report.md

# Remove __pycache__ folders (cleaner submission)
find Assessment3_Submission_Faria_Luis -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Make script executable
chmod +x Assessment3_Submission_Faria_Luis/run_eigenai.sh

# Create the submission ZIP
zip -r MFA501_Assessment3_Faria_Luis.zip Assessment3_Submission_Faria_Luis/

---

# Test if it works

# Extract to test folder
unzip MFA501_Assessment3_Faria_Luis.zip -d test_extraction

# Go into folder
cd test_extraction/Assessment3_Submission_Faria_Luis

# Test the executable
./run_eigenai.sh

# Clean Up
rm -rf Assessment3_Submission_Faria_Luis test_extraction MFA501_Assessment3_Faria_Luis.zip
