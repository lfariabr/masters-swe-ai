# 🧠 TTrack – Torrens Degree Tracker

v1.0.0 notes, drafts, and ideas

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
| **1.14.0** | macOS distribution | ✅ Complete |
| **1.15.0** | Windows distribution | ✅ Complete |
| **1.16.0** | Electron | ✅ Complete |
| **1.17.0** | PyQt5 refactor | ✅ Complete |

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
- Electron: v2 of TTrack in React+Node.js wrapped by Electron (https://github.com/lfariabr/react_electron_demo.git)
- Project Architecture: `src/components`, `src/pages`, `src/services`, `src/utils`, `src/styles`, `src/hooks`, `src/constants`

#### 🔹 v1.17.0 - `feature/frontend-refactor`
- PyQt5 refactor of UI for separation of concerns: 
- `theme_manager.py` --> containing detect system, check dark mode, update theme and toggle theme
- `tab_controller.py` --> controller of tabs for **setup**, **enable/disable** and **get** tabs (input and result)
- `data_processor.py` --> sets transcript and curriculum data and processes it via `engine.py`
- `main_window.py` --> `self.theme_manager`, `self.tab_controller`, `self.data_processor` + `init_ui()`