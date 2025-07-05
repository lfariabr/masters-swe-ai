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

---

### 🔧 In Progress

tbd

---

### 🗂️ Backlog

#### 🔸 v1.15.0 - `feature/windows-distribution`
- Write test usage case at `buildingApp.md` -> url: https://github.com/lfariabr/masters-swe-ai/tree/master/T1-Software-Development-Management/projects/TTrack_v1/docs/buildingApp.md

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
