cd ~/Desktop/sEngineer/masters_SWEAI/T1-SEP/projects/clinictrends_ai

zip -r ../clinictrends_ai_$(date +%Y-%m-%d).zip . \
  -x "*.git*" "*.DS_Store" "__pycache__/*" "*.pyc" ".pytest_cache/*" "dist/*" "build/*"
