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
| **3.0.0** | Layered Architecture Rollout | ✅ Complete |
| **3.1.0** | Login Controller | ✅ Complete |
| **3.2.0** | AuthService | ✅ Complete |
| **3.3.0** | Basic history view | ✅ Complete |
| **3.4.0** | Cloud sync | 🔥 In Progress |
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

#### 🟢 v2.2.0 - `feature/ui-to-database`
> ***Goal: Let users persist their processed data with a unique record ID.***
- After processing, provide a button "💾 Save This Session"
- Generate and show record_id (UUID or hash)
- Save both transcript and curriculum with current timestamp and user ID
- Display a toast/message: ✅ Session saved as ID: abc123

#### 🟢 v3.0.0 - `feature/structure-reorganization`
- Core, Services and Controllers directories created and restructured, looking more professional

#### 🟢 v3.1.0 - `feature/login-authentication`
- created tab_login for ui and login_controller for logic
- did some research on supabase auth thinking about Torrens Microsoft Integration (https://supabase.com/docs/guides/auth)

#### 🟢 v3.2.0 - `feature/login-authentication`
> ***Goal: Make it possible for users to register/login on the app via tab and save users on db.***
- Created `AuthService` class and integrated it in `main_window`
- Created `LoginController` class, child of AuthService
- Implemented the login, register and logout logic to use in `tab_login.py`

#### 🟢 v3.3.0 - `feature/basic-history-view`
> ***Goal: Let users retrieve previously saved sessions.***
- Update tab "Student Records" to show a list of saved records instead of mock data
- Fetch and repopulate transcript + curriculum tables
- Show timestamp, file summary, match summary
- Main changes:
  - Added `get_processed_data()` method to `DatabaseManager` for loading specific session details
  - Added `fetch_user_history()` to retrieve all sessions tied to the logged-in user
  - Added `get_entry_by_id()` to retrieve session by unique ID (for future deep linking)
  - Added `delete_entry()` for removing obsolete or unwanted sessions (planned feature integration)

---

### 🔧 In Progress

#### ▫️ v3.4.0 - `feature/cloud-sync`(Cloud Sync: Fallback and Encryption)
> ***Goal: Prepare app to run with DB even when offline or in fallback mode.***
- Abstract DB calls with try/except wrappers
- Provide fallback to local CSV save if cloud is unavailable
- Add .env support for database URL/secrets

***refs***
- https://supabase.com/docs/guides/auth/social-login/auth-azure
- https://www.reddit.com/r/Supabase/comments/1ecwowt/how_to_keep_local_db_up_to_date_with_remote/

### 🗂️ Backlog

#### Hotfixes
***v3.5.0 - check back UX during login/logout. Fine tune.***
  - UX because buttons and dialogs are not so cool
  - UI because tabs should be hidden when not logged in and login tab disappear when logged in

***v3.6.0 - check back UX during basic-history-view***
  - UX because results_data, summary_data and electives_data json needs to be treated for better displaying
  - consider adding "Course Name" column to transcript, curriculum and results table

- https://dev.to/jps27cse/how-to-prevent-your-supabase-project-database-from-being-paused-using-github-actions-3hel
- Pytest adjustments to new UI structure (`feature/frontend-tests`)
- Pytest coverage on **DatabaseManager**, **DataProcessor**, **LoginController** and **AuthService** (warnings 17 passed, 38 warnings)
- Auto detect os theme (`feature/auto-detect-os-theme`)

#### Future
- `feature/logic-layer` 
  - Engine: deeper logic like tags, topics or even semantic similarity (based on description) 
- `feature/ai-integration` 
  - AI or Machine Learning to summarize transcript and curriculum and recommend elective subjects 
  - AI chatbot to answer questions about the transcript, curriculum and recommendations 