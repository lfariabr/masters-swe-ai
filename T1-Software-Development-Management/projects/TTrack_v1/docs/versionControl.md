# Exec Project
```
cd T1-Software-Development-Management/projects/TTrack_v1
source venv/bin/activate
python main.py
```

# projects version control

## TTrack_v1

### done
v1.0.0 - app with PyQt5 + gui + pandas
v1.1.0 - app with light/dark mode support
v1.2.0 - transcript x curriculum
-- created 2 templates, one for transcript and one for curriculum 
-- exhibit them on homepage using pandas
v1.3.0 - feature/ttracker_v3
-- explore possibilities of processing data and matching (engine) 
-- refactor for modularity with ui and resolvers directories
-- adds two new tabs (input and results)
-- display processed result on results tab matching transcript with curriculum
-- dig deeper into the database (fixed names of subjects)
-- created tab_results2.py matching layout ["feat(sdm_study): v1.3.0 Engine properly matches transcript x curriculum. Adds new tab_results2 with layout]
v1.4.0 - feature/ttracker_v4
-- dig deeper into the engine.py and add a TODO there
-- make current logic makes sense, as it is key before having results page2 work

### in progress

-- make new page work tab_results2 exhibit processed data, instead of fallback

### backlog

- fix dark mode button text color
- setup more pages (homepage with intro, about)
- integrate with database so see history (mongodb 500MB / postgresql - @supabase 500MB)



