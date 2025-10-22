# EigenAI - Mathematical Foundations Portal
## Release Build Instructions

### System Requirements
- **Python 3.9 or higher** (Download from python.org)
- **Internet connection** (for first-time setup only)

### Quick Start

#### Windows:
1. **Extract the ZIP file** to a folder (e.g., `C:\Users\YourName\Desktop\eigenai`)
2. **Navigate to the folder** in File Explorer
3. **Double-click** `run_eigenai.bat`
4. **Wait** for dependencies to install (first run only, ~30 seconds)
5. Application will automatically open in your default browser
6. **Alternative Method:** Right-click inside the folder → "Open in Terminal" → type `python run_eigenai.py`

**Note:** If Windows shows a security warning, click "More info" → "Run anyway"

#### macOS/Linux:
1. Open Terminal
2. Navigate to the EigenAI folder
3. Run: `chmod +x run_eigenai.sh`
4. Run: `./run_eigenai.sh`

### What's Included
- [app.py](masters_SWEAI/2025-T2/T2-MFA/projects/eigenai/app.py:0:0-0:0) - Main application
- [views/](masters_SWEAI/2025-T2/T2-MFA/projects/eigenai/views:0:0-0:0) - User interface screens
- [resolvers/](masters_SWEAI/2025-T2/T2-MFA/projects/eigenai/resolvers:0:0-0:0) - Mathematical algorithms
  - [determinant.py](masters_SWEAI/2025-T2/T2-MFA/projects/eigenai/resolvers/determinant.py:0:0-0:0) - Recursive determinant calculator
  - [eigen_solver.py](masters_SWEAI/2025-T2/T2-MFA/projects/eigenai/resolvers/eigen_solver.py:0:0-0:0) - Eigenvalue/eigenvector solver
- [requirements.txt](masters_SWEAI/2025-T2/T2-MFA/projects/eigenai/requirements.txt:0:0-0:0) - Dependencies

### Features
- **Set 1 - Problem 1:** Recursive determinant calculation (n×n matrices)
- **Set 1 - Problem 2:** Eigenvalue & eigenvector computation (2×2 matrices)
- **Set 2:** Coming in Module 10

### Troubleshooting

**Issue:** "Python not found"
- **Solution:** Install Python 3.9+ from https://www.python.org/downloads/

**Issue:** "Module not found" error
- **Solution:** Run `pip install streamlit` manually

**Issue:** Browser doesn't open automatically
- **Solution:** Open browser and go to http://localhost:8501

### Support
For questions, contact: luis.faria@student.torrens.edu.au

### Academic Project
Part of MFA501 - Mathematical Foundations of AI
Torrens University Australia - 2025 T2