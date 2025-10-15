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

Phase 1: Foundation
Phase 2: Intelligence Enhancement
Phase 3: AI-Powered Insights

> Detailed changelog can be found in [`CHANGELOG.md`](2025-T2/T2-MFA/projects/eigenai/docs/changelog.md)

---

*Built with ❤️ and rigorous engineering principles by the EigenAI team*

**"Whether it’s concrete or code, structure is everything."**