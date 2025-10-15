
cd ~/Desktop/sEngineer/masters_SWEAI/T1-SDM/projects/TTrack_v1

zip -r ../TTrack_source_$(date +%Y-%m-%d).zip . \
  -x "*.git*" "*.DS_Store" "__pycache__/*" "*.pyc" ".pytest_cache/*" "dist/*" "build/*"