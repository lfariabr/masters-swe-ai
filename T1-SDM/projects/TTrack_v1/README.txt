# 🎓 TTrack
## Academic Progress Intelligence System

Academic progress tracking system that intelligently matches student transcripts with curriculum requirements using advanced data processing algorithms.

---

## What is TTrack?

Manual transcript checks are slow and error-prone. TTrack offers:
- Desktop app built with PyQt5 for cross-platform use
- Excel/CSV file upload and preprocessing with pandas
- Intelligent matching of transcript vs curriculum with fuzzy logic
- Real-time progress analytics and elective recommendations
- Database integration with Supabase for cloud storage and user authentication
- One-click build into standalone Windows/macOS executables

---

## Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Virtual environment** (recommended)
- **Excel/CSV support** via pandas

### Installation & Execution
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Launch application
python main.py
```

---

## System Architecture

TTrack implements a **modular, event-driven architecture** following SOLID principles and separation of concerns:

```
TTrack/
├── 🎯 main.py                    # Application entry point & orchestration
├── 🎮 controllers/               # Login, Tabs and Theme controllers
├── 🧠 core/                      # Data processing & business logic
├── 📦 dist/                      # Production builds
├── 📚 docs/                      # Technical documentation
├── 🖥️ gui/                       # Presentation layer
├── 🖼️ public/                    # Public assets like logo, icons, etc.
├── 📊 services/                  # Database & data sample
├── 🧪 tests/                     # Testing coverage
└── 🎨 ui/                        # UI components & layouts
```

### Core Engine Architecture

### Intelligent Matching Algorithm

The **TTrack Engine** (`core/data_processor.py`) implements sophisticated data processing:

```python
def match_transcript_with_curriculum(transcript_df, curriculum_df):
    """
    Advanced transcript-curriculum matching using pandas merge operations
    with intelligent subject code normalization and status classification.
    
    Algorithm Complexity: O(n log n) where n = curriculum size
    Memory Efficiency: Optimized DataFrame operations with lazy evaluation
    """
```

**Key Features:**
- **Subject Code Normalization**: Handles variations in formatting, case sensitivity
- **Fuzzy Matching**: Intelligent comparison algorithms for subject identification  
- **Status Classification**: Binary classification (✅ Done / ❌ Missing)
- **Progress Analytics**: Aggregated statistics by subject type and completion status
- **Elective Recommendations**: Suggestions based on curriculum gaps

### Data Processing Pipeline

1. **Input Validation** → Pandas DataFrame normalization
2. **Code Standardization** → String processing & cleaning
3. **Relational Matching** → Left-join operations with indicator columns
4. **Status Mapping** → Binary classification logic
5. **Analytics Generation** → Grouped aggregations & summaries
6. **Recommendation Engine** → Filtered elective suggestions

---

### Enterprise Features
- **Standalone Executables**: No Python installation required
- **Cross-Platform Compatibility**: Windows, macOS, Linux support
- **Self-Contained**: All dependencies bundled
- **Professional Branding**: Custom icons & application metadata

---

### TTrack Roadmap

### Phase 1: PyQt5 + pandas integration (v1.0.0) ✅ **COMPLETE**
- ✅ PyQt5 + pandas integration
- ✅ Light/Dark mode support
- ✅ File upload and preview with pandas
- ✅ Matching engine: Transcript × Curriculum
- ✅ Created build scripts for both Windows (.exe) and macOS (.app)
- ✅ Run all tests: `pytest tests/`

### Phase 2: Supabase Backend Integration (v2.0.0) ✅ **COMPLETE**
- ✅ Electron: v2 of TTrack in React+Node.js wrapped by Electron
- ✅ Database Backend: PostgreSQL with 500MB+ capacity
- ✅ User Authentication: Secure login & role-based access

### Phase 3: Distribution and Engine Matching (v3.0.0) 🔄 **IN PROGRESS**
- ✅ Layered Architecture with Core, Services and Controllers
- ✅ Cloud Sync: Fallback and Encryption
- ✅ New Engine Matching Logic 2.0
- ✅ Pytest coverage to new classes (`DatabaseManager`, `AuthService`, `LoginController`)

### Phase 4: AI Enhancement (v4.0.0) 📋 **PLANNED**
- 📋 API Integration: University system connectivity
- 📋 Semantic Matching: NLP-based subject similarity detection
- 📋 Predictive Analytics: Graduation timeline forecasting
- 📋 Recommendation Engine: Personalized course suggestions
- 📋 Machine Learning: Continuous improvement algorithms

### Phase 5: Enterprise Scale (v5.0.0) 🚀 **FUTURE**
- 🚀 Multi-tenant Architecture: Institution-wide deployment
- 🚀 Advanced Analytics: Business intelligence dashboards
- 🚀 Integration APIs: Third-party system connectivity
- 🚀 Mobile Applications: iOS/Android companion apps

---

*Built with ❤️ and rigorous engineering principles.*

**"Software eats degrees… unless TTrack tracks them first."**
