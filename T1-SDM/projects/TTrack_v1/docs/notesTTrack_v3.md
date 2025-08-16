# 🧠 TTrack – Torrens Degree Tracker

v2.0.0 notes, drafts, and ideas

## 🔬 Development Methodology

### Version Control Strategy
Following **GitFlow** with feature branches and semantic versioning:

| Version | Milestone | Status |
|---------|-----------|--------|
| **3.0.0** | Layered Architecture Rollout | ✅ Complete |
| **3.1.0** | Login Controller | ✅ Complete |
| **3.2.0** | AuthService | ✅ Complete |
| **3.3.0** | Basic history view | ✅ Complete |
| **3.4.0** | Cloud sync | ✅ Complete |
| **3.5.0** | .env setup for Supabase | ✅ Complete |
| **3.6.0** | Login UX | ✅ Complete |
| **3.7.0** | Pitch deck work | ✅ Complete |
| **3.8.0** | Student Records UX | ✅ Complete |
| **3.9.0** | Encryption on Build process | ✅ Complete |
| **3.10.0** | Engine Matching 2.0 | ✅ Complete |
| **4.0.0** | Pytest robust coverage | 🕐 Not started |
| **TBD** | AI Enhanced matching | 🕐 Not started |
| **TBD** | Enterprise scale | 🕐 Not started |

> Tip: ✅ = Done, 🔥 = In Progress, 🕐 = Not started

---

## ✅ Feature Progress

### ✔ Done

#### 🟢 v3.0.0 - `feature/structure-reorganization`
- Core, Services and Controllers directories created and restructured, looking more professional

#### 🟢 v3.1.0 - `feature/login-authentication`
- created tab_login for ui and login_controller for logic
- did some research on supabase auth thinking about Torrens Microsoft Integration (https://supabase.com/docs/guides/auth)

#### 🟢 v3.2.0 - `feature/login-authentication`
> Goal: Make it possible for users to register/login on the app via tab and save users on db.
- Created `AuthService` class and integrated it in `main_window`
- Created `LoginController` class, child of AuthService
- Implemented the login, register and logout logic to use in `tab_login.py`

#### 🟢 v3.3.0 - `feature/basic-history-view`
> Goal: Let users retrieve previously saved sessions.
- Update tab "Student Records" to show a list of saved records instead of mock data
- Fetch and repopulate transcript + curriculum tables
- Show timestamp, file summary, match summary
- Main changes:
  - Added `get_processed_data()` method to `DatabaseManager` for loading specific session details
  - Added `fetch_user_history()` to retrieve all sessions tied to the logged-in user
  - Added `get_entry_by_id()` to retrieve session by unique ID (for future deep linking)
  - Added `delete_entry()` for removing obsolete or unwanted sessions (planned feature integration)

#### 🟢 v3.4.0 - `feature/cloud-sync`(Cloud Sync: Fallback and Encryption)
> Goal: Prepare app to run with DB even when offline or in fallback mode.
- Provide fallback to save processed data in CSV if cloud is unavailable
- Abstract DB calls with try/except wrappers
- SyncService created to handle cloud sync logic, but not in use. Studying.
- SyncStatusWidget created to display sync status and progress, but not in use. Studying.

#### 🟢 v3.5.0 - `feature/database-url-secrets`
> Goal: Add .env support for database URL/secrets.
- add dotenv in main.py
- enhance .env.example
- update TTrack.spec and TTrack-macOs.spec 
- create docs/BUILD.md
- make downloaded app authentication work

#### 🟢 v3.6.0 - `feature/login-ux`
> Goal: improve UX with cool buttons and dialogs
- fine tuning for login and logout
- tabs should be hidden when not logged in and login tab disappear when logged in (work on tab_controller.py)

#### 🟢 v3.7.0 - `feature/pitch-deck`
> Goal: Show off project
- fine tune web form: https://forms.gle/zaH4BGeibhDrfVcL8
- schedule in advance (check with Dr. Atif)
- draw a PPT to display on the meeting with a "FOR DUMMIES" version of the TTrack
- story telling:
- from PM to SWE focused on backend
- Data from Torrens & curiosity for process improvement & automation
- draw what I think is current flow (W/O app and compare it with app)

#### 🟢 v3.8.0 - `feature/basic-history-view`
> Goal: improve UX with cool buttons and dialogs
- UX because results_data, summary_data and electives_data json needs to be treated for better displaying
- add "Credit Points" and "Student Name" to Student Records table (when saving, on database and exhibition @ student recordes)
- increase the size of the tables displayed in table results for a height of minimum 50 pixels each
- when clicking LOGGED IN and clicking on "Process Data", user should be sent to Results, not to Student Records

#### 🟢 v3.9.0 - `hotfix/database-url-secrets` 
> Goal: encrypt .env automatically on .exe/app files
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
> Goal: Adjust engine matching with PDF provided by Dr. Atif for Masters in IT
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

#### 🟢 v3.11.0 - `feature/engine-adit`
> Goal: Integrate ADIT course structure to the system 
- [X] create data/courses/adit21.py to be used
- [X] import specific functions at data_processor for testing and easy usage
- [X] Update curriculum .xlsx to be exactly like MSIT course and make it appear on tab input

#### 🟢 v3.11.1 - `feature/engine-version-two`
> Goal: Display hardcoded transcript on sample data table instead of xlsx: 
- [X] create `load_sample_file_hardcoded` on `tab_input.py` to be used at `Connect helper buttons` section ***- line 112***
- [X] create `load_as_model_hardcoded(is_transcript=True)` on `utils.py` ***- line 31***
- [X] create `load_curriculum_and_bank_same_df` at `msit_ad.py`
- [X] create `load_curriculum_and_bank_adit_same_df` at `adit21.py`
- [X] plugged `load_curr_and_bank` at utils.py load_as_model_hardcoded to test
- [X] double check if `load_sample_file_hardcoded` is with expected behaviour
- [X] double check if `load_as_model_hardcoded` at `utils.py` is with expected behaviour

#### 🟢 v3.11.2 - `feature/student-records-display`
> Goal: Update Student Records saving and displaying data
- [X] update "Student Records" tab when nothing's loaded (columns 5... to current existing ones...) 
- [X] update student_records table adding new columns via SQL
- [X] Save Course Name on database 
- [X] Save Student ID on database

#### ⚙️ v3.12.0 - `feature/course-selection`
> Goal: Create button on the interface (input) allowing different courses to be selected
- [X] add selection button to switch between curriculum for ADIT/MSIT 
- [X] map at process data course selected to improve UX
- [X] test saving and processing with different courses for different students

---

### 🔧 In Progress
#### ⚙️ v3.12.0 - `feature/pytest`
> Goal: Adjust pytest coverage to new UI structure and components (Core, Services, Controllers)
- [X] Adjust pytest.ini to remove all deprecation warnings and features
- [X] Add coverage to Core component
- [ ] Add coverage to Services component
- [ ] Add coverage to Controllers component

### 🗂️ Backlog
- N/A

#### Future
- `feature/results-ux`: Completion %: compute both by type and overall (sum credits for ✅ / 160 total)
- `feature/wil-upgrades`: mark ITW601 as “Available soon” until REM502 and total 70 CP reached; mark ITA602 locked until ITW601 is ✅.
- `feature/elective-upgrades`: recommend electives based on current progression or uni directives according to availability throughout year
- `feature/database-persistence`: use SyncService and SyncStatusWidget for local data persistence
- `feature/auto-detect-os-theme`: Auto detect os theme 
- `feature/logic-layer`: Engine: deeper logic like tags, topics or even semantic similarity (based on description) 
- `feature/azure-integration`: Azure integration for easy login/register with Microsoft accounts
- `feature/ai-integration`: AI or Machine Learning to summarize transcript and curriculum and recommend elective subjects, AI chatbot to answer questions about the transcript, curriculum and recommendations 

***refs***
- https:/x/supabase.com/docs/guides/auth/social-login/auth-azure
- https://www.reddit.com/r/Supabase/comments/1ecwowt/how_to_keep_local_db_up_to_date_with_remote/
- https://dev.to/jps27cse/how-to-prevent-your-supabase-project-database-from-being-paused-using-github-actions-3hel
