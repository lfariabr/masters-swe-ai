# 🧠 TTrack – Torrens Degree Tracker

TTrack is a desktop application designed to help students and academic staff **track academic progress** by comparing a student’s **official transcript** with their **prescribed curriculum**. It automates the validation of completed, missing, and elective subjects, offering a clean interface and clear dashboard outputs.

---

## 🚀 How to Run

(If already with virtual env)
```bash
cd T1-Software-Development-Management/projects/TTrack_v1
source venv/bin/activate
python main.py
```

(If not with virtual env)
```bash
cd T1-Software-Development-Management/projects/TTrack_v1
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 📦 Project Details

| Key       | Value            |
|-----------|------------------|
| **Name**  | TTrack           |
| **Version** | 1.13.0         |
| **Stack** | Python, PyQt5, pandas, openpyxl |
| **Goal**  | Compare transcript data with curriculum and return smart academic progress insights |
| **Alt. Stack (Prototype)** | Electron + Node.js + React (explored in parallel) |

---

## 🔬 Development Methodology

### Version Control Strategy
Following **GitFlow** with feature branches and semantic versioning:

| Version | Milestone | Status |
|---------|-----------|--------|
| **1.0.0** | Core PyQt5 + pandas integration | ✅ Complete |
| **1.1.0** | Theme system implementation | ✅ Complete |
| **1.2.0** | Template system & file I/O | ✅ Complete |
| **1.3.0** | Matching engine & modular refactor | ✅ Complete |
| **1.4.0** | Engine optimization & documentation | ✅ Complete |
| **1.5.0** | Advanced matching algorithms | ✅ Complete |
| **1.6.0** | Build system & distribution | ✅ Complete |
| **1.7.0** | Theme refinements & UX polish | ✅ Complete |
| **1.8.0** | Sprint review (Sonnet x GPT Memmories) | ✅ Complete |
| **1.9.0** | Layout refactoring | ✅ Complete |
| **1.10.0** | Pytest integration | ✅ Complete |
| **1.11.0** | Build distribution macOS | ✅ Complete |
| **1.12.0** | Sample data to interface | ✅ Complete |
| **1.13.0** | Build distribution Windows | ✅ Complete |
| **2.0.0** | Database integration & cloud sync | 🔄 Planned |
| **3.0.0** | AI Enhanced matching | 🔄 Planned |
| **4.0.0** | Enterprise scale | 🔄 Planned |


### Code Quality Standards
- **Test Coverage**: >85% with pytest
- **Type Safety**: mypy static analysis
- **Code Style**: black + isort formatting
- **Documentation**: Comprehensive docstrings + technical specs
- **Performance**: Profiled with cProfile for optimization

---

## ✅ Feature Progress

### ✔ Done

#### 🔹 v1.0.0
- Initial PyQt5 GUI with pandas integration

#### 🔹 v1.1.0
- Light/Dark mode support

#### 🔹 v1.2.0
- Created templates for Transcript & Curriculum
- File upload and preview with pandas

#### 🔹 v1.3.0
- Matching engine: Transcript × Curriculum
- Modular refactor: `ui/`, `resolvers/` directories
- Results tab with basic processed output
- Introduced `tab_results2.py` layout

#### 🔹 v1.4.0
- Engine logic restructured
- Internal comments, TODOs added for new output logic

#### 🔹 v1.5.0 - `feature/ttracker-engine-expansion`
- `match_transcript_with_curriculum`: compares both files and tags subjects as Done or Missing
- `generate_progress_summary`: groups by subject type (Core, Elective, etc.) and shows how many are Done/Missing
- `suggest_electives`: gives basic elective suggestions based on what’s still missing

#### 🔹 v1.6.0 - `feature/ttracker-exe-test`
- Added PyInstaller configuration for creating standalone executables
- Created build scripts for both Windows (.exe) and macOS (.app)
- Documentation for building and distributing the application

#### 🔹 v1.7.0 - `feature/ttracker-dark-mode`
- Refined logic for dark mode toggle button to work with the UI

#### 🔹 v1.8.0 - `feature/ttracker-sprint_review`
- Cross checked Windsurf's memory with the project's history using Claude Sonnet 4 and matched against ChatGPT master's AI memmories

#### 🔹 v1.9.0 - `feature/tab-results`
- add A-Z sorting on results table (done)
- add student name and university to results tab (done)
- update progress bar (done)

#### 🔹 v1.10.0 - `feature/pytest`
- Run all tests: `pytest tests/`
- Run a specific test file: `pytest tests/test_curriculum_matching.py -v`
- Run tests with coverage report: `pytest --cov=. tests/` OR `pytest --cov=. --cov-report=term-missing tests/`

#### 🔹 v1.11.0 - `feature/build-distribution`
- Build distribution (macOS at build_mac.sh)
- Build distribution (Windows at build.bat)  
- Updated docs @ [buildingApp.md](https://github.com/lfariabr/masters-swe-ai/tree/master/T1-Software-Development-Management/projects/TTrack_v1/docs/buildingApp.md)  
- Adds workflow to build windows.exe

#### 🔹 v1.12.0 - `feature/sample-data-to-interface`
- Add 2 cool buttons to load sample data (transcript and curriculum) from the `data` folder

#### 🔹 v1.13.0 - `feature/windows-distribution`
- Update `TTrack.spec` to include `data/` and logo assets
- Add `info.py` with `resource_path()` helper for Windows EXE distribution
- Update `tab_input.py` to use `resource_path()` for loading bundled files

#### 🔹 v1.14.0 - `feature/macos-distribution`
- Update `TTrack-macOs.spec` to include `data/` and logo assets
- Uses `build_mac.sh` to build macOS app referencing `TTrack-macOs.spec`

#### 🔹 v1.15.0 - `feature/windows-distrib2`
- Write test usage case at `buildingApp.md` -> url: https://github.com/lfariabr/masters-swe-ai/tree/master/T1-Software-Development-Management/projects/TTrack_v1/docs/buildingApp.md

#### 🔹 v1.16.0 - `feature/electron`
- Electron: v2 of TTrack in React+Node.js wrapped by Electron
https://github.com/lfariabr/react_electron_demo.git

> Setup Commands
```bash
npm uninstall electron-prebuilt-compile
npm install
npm install --save-dev electron
npm run start-electron
```

> Project Architecture
```bash
# Setting up modular structure
mkdir -p src/components src/pages src/services src/utils src/styles src/hooks src/constants
```

> Component Structure
- **UI Components:**
  - `FileUploader`: Handles transcript and curriculum file uploads
  - `DataTable`: Displays tabular data with headers and rows
  - `ProgressChart`: SVG circular visualization for degree completion
  - `InputPage`: Manages upload workflow and initial data display
  - `ResultsPage`: Tabbed interface for viewing results

> Service Layer
- `apiService.js`: HTTP communication with backend
  - Upload file handling
  - Local fallback processing when server unavailable
  - Export functionality
- `resolverService.js`: Core matching algorithm
  - Transcript-curriculum course matching
  - Status tracking (completed/missing)
  - Recommendations generation

> Server Implementation
- Express backend (port 5000)
- File upload/processing endpoints
- CORS configuration for cross-origin requests
- Graceful server handling in Electron context

> Electron Integration
- Main process spawns Express server
- Development mode loads React dev server
- Production loads static build files
- Proper resource cleanup on exit

> UI/UX Enhancements
- Comprehensive CSS styling:
  - Tab navigation system
  - Progress visualization
  - Error message handling
  - Processing overlay with spinner
  - Dark mode support
  - Responsive design

> Future Tasks
- Improved Electron security (contextIsolation)
- Testing suite implementation
- Distribution packaging
- Offline mode optimization

#### 🔹 v1.17.0 - `feature/frontend-refactor`
- PyQt5 refactor of UI for separation of concerns: `theme_manager.py`, `tab_controller.py`, `data_processor.py` --> all correctly linked to `main_window.py`


---

### 🔧 In Progress

#### 🔸 v1.18.0 - `feature/frontend-tests`
- Pytest adjustments to new UI structure

### 🗂️ Backlog

#### 🔸 v2.0.0 - `feature/db-integration`
- Integrate with DB (MongoDB or Supabase PostgreSQL – 500MB free tier)

- engine: deeper logic like tags, topics or even semantic similarity (based on description). (v3)
- Login, authentication (v4)

---

## 📎 Proposal & Docs
This project is part of **SDM404 – Software Development Management** at Torrens University. Full proposal PDF includes:
- Timeline & Milestones
- Risk Analysis
- Budget & Roles
- Dev Notes & Meeting Logs
