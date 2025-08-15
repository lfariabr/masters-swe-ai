# 🧠 TTrack – Torrens Degree Tracker

v2.0.0 notes, drafts, and ideas

## 🔬 Development Methodology

### Version Control Strategy
Following **GitFlow** with feature branches and semantic versioning:

| Version | Milestone | Status |
|---------|-----------|--------|
| **1.x** | Core development, UI/UX, processing engine, cross-platform builds | ✅ Complete |
| **2.0.0** | Supabase Backend Integration | ✅ Complete |
| **2.1.0** | Scaffold database | ✅ Complete |
| **2.2.0** | UI to database | ✅ Complete |

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

#### 🟢 v2.2.0 - `feature/ui-to-database`
> ***Goal: Let users persist their processed data with a unique record ID.***
- After processing, provide a button "💾 Save This Session"
- Generate and show record_id (UUID or hash)
- Save both transcript and curriculum with current timestamp and user ID
- Display a toast/message: ✅ Session saved as ID: abc123