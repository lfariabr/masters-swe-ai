# EigenAI 
## Smart Tutor for Math/Programming

## What is EigenAI?

EigenAI plays on "eigenvalues" and AI foundations".

It is a learning assistant web app for Torrens' Mathematical Foundations of Artificial Intelligence subject and can work as a tutor for students interested in math/programming subjects.

The app will act as a companion tutor that walks students through each problem set interactively — showing process, formulas, and results with animations.

## How does it work?

The app will act as a companion tutor that walks students through each problem set interactively — showing process, formulas, and results with animations.

### Prerequisites
- **Python 3.9+** with pip package manager
- **Virtual environment** 
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

### Installation & Launch
```bash
# Navigate to project directory
cd 2025-T2/T2-MFA/projects/eigenai

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Launch application
streamlit run app.py
```

## 🏗️ System Architecture

```text
EigenAI/
├── 🚀 app.py                # Entry point (Streamlit orchestration)
├── 📁 assets/               # Static assets
├── 📊 docs/                 # Documentation & specs
├── 🧳 utils/                # Logic layer 
│   ├── determinant.py
│   ├── eigen_solver.py
├── 📱 views/                # Presentation layer (UI screens)
│   ├── home.py
│   ├── set1Problem1.py
│   ├── set1Problem2.py
│   ├── set2Problem1.py
│   ├── set2Problem2.py
├── 🧪 tests/                # Unit test suite (To be done!!!)
└── 📚 requirements.txt
```

---

## EigenAI Roadmap

| Version | Status | Description |
| --- | - | --------- |
| v0.0.1 | ✅ | Streamlit setup assets, pages and utils |
| v0.0.2 | ✅ | Sidebar menu, logo, title and docs |
| v0.0.3 | ✅ | Resolver refactor and assessment docs build up |
| v0.0.4 | ✅ | UX and UI improvements |
| v0.0.9 | ✅ | PyInstaller + release build documentation |
| v0.1.0 | ✅ | Assessment 2A submission |
| v0.1.2 | ✅ | Added integration solver for Set 2 Problem 1 |
| v0.1.3 | ✅ | Added Hill Climbing algorithm for Set 2 Problem 2 |
| v0.1.4 | ✅ | Reviewed Set 2 Problem 1 (Numerical Integration) |
| v0.1.5 | ✅ | Updated Set 2 Problem 1 with matplotlib for graphic visuals |
| v0.1.6 | ✅ | Added sympy library to display mathematical expressions and equations |
| v0.1.7 | ✅ | Added Set 2 Problem 2 (RRBF Gradient Calculator) |
| v0.1.8 | ✅ | Added Set 3 Problem 1 (Hill Climbing Binary Image Reconstruction) |
| v0.2.0 | ✅ | Assessment 2B submission (Integration + RRBF) |
| v0.2.4 | ✅ | Added stochastic sampling to Hill Climber and UI |
| v0.2.6 | ✅ | Added complex pattern to constructor and UI |
| v0.3.0 | ✅ | Assessment 3 submission (Hill Climbing Algorithm) |
| vX.X.X | 🕐 | Test coverage |
| vX.X.X | 🕐 | Login + Authentication |
| vX.X.X | 🕐 | LLM plug with rate limiting |
| vX.X.X | 🕐 | BaaS with Supabase |
| vX.X.X | 🕐 | Backend Framework (FastAPI, Flask) |
| vX.X.X | 🕐 | Weekly digest with Agentic Integration |
| vX.X.X | 🕐 | Security enhancements |

> Detailed changelog can be found in [`CHANGELOG.md`](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/projects/eigenai/docs/changelog.md)

---

*Built with ❤️ and rigorous engineering principles by EigenAI team*

**"Whether it’s concrete or code, structure is everything."**