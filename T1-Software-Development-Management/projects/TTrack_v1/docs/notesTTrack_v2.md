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
| **3.4.0** | Cloud sync | ✅ Complete |
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

#### 🟢 v3.4.0 - `feature/cloud-sync`(Cloud Sync: Fallback and Encryption)
> ***Goal: Prepare app to run with DB even when offline or in fallback mode.***
- Provide fallback to save processed data in CSV if cloud is unavailable
- Abstract DB calls with try/except wrappers
- SyncService created to handle cloud sync logic, but not in use. Studying.
- SyncStatusWidget created to display sync status and progress, but not in use. Studying.

#### 🟢 v3.5.0 - `feature/database-url-secrets`
> ***Goal: Add .env support for database URL/secrets.***
- add dotenv in main.py
- enhance .env.example
- update TTrack.spec and TTrack-macOs.spec 
- create docs/BUILD.md
- make downloaded app authentication work

#### 🟢 v3.6.0 - `feature/login-ux`
> ***Goal: improve UX with cool buttons and dialogs***
- fine tuning for login and logout
- tabs should be hidden when not logged in and login tab disappear when logged in (work on tab_controller.py)

#### 🟢 v3.7.0 - `feature/pitch-deck`
  - fine tune web form: https://forms.gle/zaH4BGeibhDrfVcL8
  - schedule in advance (check with Dr. Atif)
  - draw a PPT to display on the meeting with a "FOR DUMMIES" version of the TTrack
  - story telling:
    - from PM to SWE focused on backend
    - Data from Torrens & curiosity for process improvement & automation
    - draw what I think is current flow (W/O app and compare it with app)

#### 🟢 v3.8.0 - `feature/basic-history-view`
> ***Goal: improve UX with cool buttons and dialogs***
- UX because results_data, summary_data and electives_data json needs to be treated for better displaying
- add "Credit Points" and "Student Name" to Student Records table (when saving, on database and exhibition @ student recordes)
- increase the size of the tables displayed in table results for a height of minimum 50 pixels each
- when clicking LOGGED IN and clicking on "Process Data", user should be sent to Results, not to Student Records

#### 🟢 v3.9.0 - `hotfix/database-url-secrets` 
> ***Goal: encrypt .env automatically on .exe/app files***
- Encrypt password
- Incorporate encryption in build process
- Make unecessary for user to manually edit or insert .env
```bash Run macOs build
python encrypt_env.py
pyinstaller TTrack-macOs.spec
```
```bash Run Windows build
python encrypt_env.py
pyinstaller TTrack.spec
```

#### 🟢 v3.10.0 -`feature/engine-matching`: 
> ***Goal: Adjust engine matching with PDF provided by Dr. Atif for Masters in IT***
- Map out .pdf of course
- Update `engine.py` logic with `suggest_electives_v2`, `match_transcript_with_curriculum_v2` and `generate_progress_summary_v2`
- Update `data_processor.py` logic with `process_data_v2`, `save_session_to_database_v2`
- Upgrade displayed info for final user
- Summary of what has been done on the algorithm:
```Python
# 1) load the canonical structures
curriculum_df = load_curriculum_df()
elective_bank_df = load_elective_bank_df()

# 2) your transcript_df must have at least ['Subject Code'] (and ideally 'Subject Name')
# transcript_df = pd.read_csv(...)

# 3) match
result_df = match_transcript_with_curriculum_v2(transcript_df, curriculum_df, elective_bank_df)

# 4) summary + suggestions
summary_df = generate_progress_summary_v2(result_df)
recs_df = suggest_electives_v2(result_df, elective_bank_df, transcript_df, max_electives=3)
```
  
---

### 🔧 In Progress

  > Notes you can show in the UI (nice UX)
	> •	WIL gating: mark ITW601 as “Available soon” until REM502 and total 70 CP reached; mark ITA602 locked until ITW601 is ✅. (Your PDF states the WIL/prereq notes and 3 elective requirement.  ￼)
	> •	Elective slots: students need 3 electives; any subjects from the Elective Bank count (respecting each elective’s prereqs).  ￼
	> •	Completion %: compute both by type and overall (sum credits for ✅ / 160 total).

### 🗂️ Backlog

- ⚙️ `feature/course-name-column`: 
  - add "Course Name" column to transcript, curriculum and results table
- ⚙️ `feature/frontend-tests`: 
  - Pytest adjustments to new UI structure 
- ⚙️ `feature/backend-tests`: 
  - Pytest coverage on **DatabaseManager**, **DataProcessor**, **LoginController** and **AuthService** (warnings 17 passed, 38 warnings) 

***refs***
- https:/x/supabase.com/docs/guides/auth/social-login/auth-azure
- https://www.reddit.com/r/Supabase/comments/1ecwowt/how_to_keep_local_db_up_to_date_with_remote/
- https://dev.to/jps27cse/how-to-prevent-your-supabase-project-database-from-being-paused-using-github-actions-3hel

#### Future
- `feature/database-persistence`: use SyncService and SyncStatusWidget for local data persistence
- `feature/auto-detect-os-theme`: Auto detect os theme 
- `feature/logic-layer` 
  - Engine: deeper logic like tags, topics or even semantic similarity (based on description) 
- `feature/azure-integration`
  - Azure integration for easy login/register with Microsoft accounts
- `feature/ai-integration` 
  - AI or Machine Learning to summarize transcript and curriculum and recommend elective subjects 
  - AI chatbot to answer questions about the transcript, curriculum and recommendations 