# 🧠 TTrack – Torrens Degree Tracker

v2.0.0 notes, drafts, and ideas

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

---

## ✅ Feature Progress

### ✔ Done

#### 🔹 v2.0.0 - `feature/ttrack-database`
- initial database integration
- create `utils/database.py` with logic to be filled in
- create `ui/tab_studentrecords.py` and implement it on `gui/main_window.py`

---

### 🔧 In Progress

#### 🔸 v2.1.0 - `feature/tbd`
- Work on `utils/database.py` to implement database logic with either mongodb or postgresql
- make it possible for users to save processed transcript and curriculum for future use (with a unique id)

### 🗂️ Backlog

- Pytest adjustments to new UI structure (`feature/frontend-tests`)
- Auto detect os theme (`feature/auto-detect-os-theme`)
- v2.0.0 - `feature/db-integration` 
  - Integrate with DB (MongoDB or Supabase PostgreSQL – 500MB free tier)
  - Make it possible for users to save processed transcript and curriculum for future use (with a unique id)
- v3.0.0 - `feature/logic-layer` 
  - Engine: deeper logic like tags, topics or even semantic similarity (based on description) 
- v4.0.0 - `feature/ai-integration` 
  - AI or Machine Learning to summarize transcript and curriculum and recommend elective subjects 
  - AI chatbot to answer questions about the transcript, curriculum and recommendations 
- v5.0.0 - `feature/login-authentication`
  - Make it possible for users to register/login on the app