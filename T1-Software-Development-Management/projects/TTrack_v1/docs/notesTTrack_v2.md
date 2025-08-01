# 🧠 TTrack – Torrens Degree Tracker

v2.0.0 notes, drafts, and ideas

## 🔬 Development Methodology

### Version Control Strategy
Following **GitFlow** with feature branches and semantic versioning:

| Version | Milestone | Status |
|---------|-----------|--------|
| **1.x** | Core development, UI/UX, processing engine, cross-platform builds | ✅ Complete |
| **2.0.0** | Database integration & cloud sync | ✅ Complete |
| **2.1.0** | Scaffold database | ✅ Complete |
| **2.2.0** | UI to database | 🔥 In Progress |
| **3.0.0** | Login authentication | 🕐 Not started |
| **3.1.0** | Basic history view | 🕐 Not started |
| **3.2.0** | Cloud sync | 🕐 Not started |
| **TBD** | AI Enhanced matching | 🕐 Not started |
| **TBD** | Enterprise scale | 🕐 Not started |

> Tip: ✅ = Done, 🔥 = In Progress, 🕐 = Not started

---

## ✅ Feature Progress

### ✔ Done

#### 🟢 v2.0.0 - `feature/ttrack-database`
- initial database integration
- the SUPER POWERFUL class **DatabaseManager** 🗄️
- create `utils/database.py` with logic to be filled in
- create `ui/tab_studentrecords.py` and implement it on `gui/main_window.py`

#### 🟢 v2.1.0 - `feature/scaffolding-database`
> ***Goal: Create a flexible backend layer to persist user-uploaded and processed data.***
- Scaffold `utils/database.py`
- Create reusable methods:
  - `save_transcript(user_id, transcript_df)` and `save_curriculum(user_id, curriculum_df)`
  - `fetch_user_history(user_id)`
  - `get_entry_by_id(entry_id)`
  - `delete_entry(entry_id)`
- Choose DB: MongoDB (schemaless) or PostgreSQL via Supabase (relational) - **Update: Go with Supabase**
  - to keep backend in pure python, we can use postgresql + supabase (BaaS - Backend as a Service)
  - we can also think about using MongoDB by using PyMongo using import MongoClient
  - framework option has been discarded since it would make app more complex and web is not our main focus
- Setup Supabase project and database schema via Supabase dashboard
- Added logic to `utils/database.py` using error handling and try/except blocks
- Added logic to `utils/data_processor.py` to save processed data to database using `DatabaseManager` class

#### ▫️ v2.2.0 - `feature/ui-to-database`
> ***Goal: Let users persist their processed data with a unique record ID.***
- After processing, provide a button "💾 Save This Session"
- Generate and show record_id (UUID or hash)
- Save both transcript and curriculum with current timestamp and user ID
- Display a toast/message: ✅ Session saved as ID: abc123

---

### 🔧 In Progress

#### ▫️ v3.0.0 - `feature/login-authentication`
***part1***
- created tab_login for ui and login_controller for logic
- did some research on supabase auth thinking about Torrens Microsoft Integration (https://supabase.com/docs/guides/auth)

***part2***
- Make it possible for users to register/login on the app via tab
- Save users on db

---

#### ▫️ v3.1.0 - `feature/basic-history-view`
> ***Goal: Let users retrieve previously saved sessions.***
- Update tab "Student Records" to show a list of saved records instead of mock data
- Fetch and repopulate transcript + curriculum tables
- Show timestamp, file summary, match summary

#### ▫️ v3.2.0 - `feature/cloud-sync`
> ***Goal: Prepare app to run with DB even when offline or in fallback mode.***
- Abstract DB calls with try/except wrappers
- Provide fallback to local CSV save if cloud is unavailable
- Add .env support for database URL/secrets

### 🗂️ Backlog

#### Hotfixes
- Pytest adjustments to new UI structure (`feature/frontend-tests`)
- Pytest coverage on **DatabaseManager** and **DataProcessor**
- Pytest coverage on warnings 17 passed, 38 warnings
- Auto detect os theme (`feature/auto-detect-os-theme`)

#### Future
- `feature/logic-layer` 
  - Engine: deeper logic like tags, topics or even semantic similarity (based on description) 
- `feature/ai-integration` 
  - AI or Machine Learning to summarize transcript and curriculum and recommend elective subjects 
  - AI chatbot to answer questions about the transcript, curriculum and recommendations 