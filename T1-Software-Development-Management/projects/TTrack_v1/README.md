
# 🧠 TTrack – Torrens Degree Tracker

TTrack is a desktop application designed to help students and academic staff **track academic progress** by comparing a student’s **official transcript** with their **prescribed curriculum**. It automates the validation of completed, missing, and elective subjects, offering a clean interface and clear dashboard outputs.

> Built with sweat, coffee, and Ctrl+Z by Luis — acting as both the Project Manager and Tech Lead, going full gear to rock this motherf***er on!

---

## 🚀 How to Run

```bash
cd T1-Software-Development-Management/projects/TTrack_v1
source venv/bin/activate
python main.py
```

---

## 📦 Project Details

| Key       | Value            |
|-----------|------------------|
| **Name**  | TTrack           |
| **Version** | 1.5.0         |
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

---

### 🔧 In Progress

#### 🔸 v1.5.0 – `feature/ttracker-engine-expansion`
- `match_transcript_with_curriculum`: compares both files and tags subjects as Done or Missing
- `generate_progress_summary`: groups by subject type (Core, Elective, etc.) and shows how many are Done/Missing
- `suggest_electives`: gives basic elective suggestions based on what’s still missing
- TODO: deeper logic like tags, topics or even semantic similarity (based on description).

---

### 🗂️ Backlog

- Make `tab_results2` functional: processed result shown properly
- Fix dark mode button text color
- Add more pages (Homepage, About)
- Integrate with DB (MongoDB or Supabase PostgreSQL – 500MB free tier)

---

## 📅 Version Control Roadmap

| Version | Modules            | Status         |
|---------|---------------------|----------------|
| 1.0.0   | Modules 1–4         | ✅ Done        |
| 2.0.0   | Modules 5–8         | 🕐 Not started |
| 3.0.0   | Modules 9–12        | 🕐 Not started |

---

## 🤝 Contributors
- **Luis** – Fullstack, Project Manager
- **Hussain** – Fullstack (Electron prototype)
- **Rosa** – UI Designer
- **Victor** – DBM / Supabase setup
- **Nomayer** – QA, Stakeholder liaison

---

## 📎 Proposal & Docs
This project is part of **SDM404 – Software Development Management** at Torrens University. Full proposal PDF includes:
- Timeline & Milestones
- Risk Analysis
- Budget & Roles
- Dev Notes & Meeting Logs

---

## 🧩 Fun Fact
This system was built side-by-side using both **Electron+React** and **Python+PyQt5** prototypes, with the aim of presenting both to the lecturer for discussion and final implementation direction.

---

## 👀 Next Milestone
💡 Delivering a full Results Page with transcript/curriculum comparison, dashboard visuals, and elective recommendations, all locally processed with zero dependency on admin support.

---

> “Software eats degrees… unless TTrack tracks them first.”
