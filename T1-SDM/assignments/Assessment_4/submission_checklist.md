# Submission's Checklist
- [X] Digital Presentation slides
- [ ] 5 min video recording 
- [ ] README.md to text file
- [ ] Source codes and applicable libraries.
- [ ] Individual Contribution report with:
    1. Tasks you have worked on (task details/date/..)
    2. Problems that you faced while working on these tasks (if any).
    3. Proposed solutions to these problems and the final solution that you have chosen.

## Script
Script Outline:

Slide 1 – Introduction (0:00 – 0:30)

“Hello, we are [Team Name], and this is our project TTrack – Torrens Degree Tracker.”

“TTrack helps students and academic staff automatically match their transcripts with the official curriculum, track progress, and identify missing or elective subjects.”

Slide 2 – Project Goals (0:30 – 1:00)

“Our goal was to save time and increase accuracy in academic progress tracking by automating what is currently a manual process.”

“We aimed to create a desktop application that works on both Windows and macOS, with a user-friendly interface, sample data support, and reusable matching logic.”

Slide 3 – Project Management Process (1:00 – 1:40)

“We followed an agile approach with sprints:

Sprint 1: UI/UX design and mock data integration.

Sprint 2: Database scaffolding and matching engine.

Sprint 3: Cross-platform distribution and polishing.”

“We used GitFlow for version control, maintained coding standards, and implemented QA checks before each milestone.”

Slide 4 – Feature Demonstration (1:40 – 4:30)
(Here, you switch to live demo)

“Here’s TTrack’s main interface, built with PyQt.”

“We can load a student transcript and the prescribed curriculum using these file inputs.”

“The matching engine automatically categorizes subjects as completed or missing, checks prerequisites, and suggests electives.”

“Here is the progress summary dashboard, showing completion percentage by semester and subject type.”

“The results can be exported for record-keeping and future reference.”

Slide 5 – Conclusion (4:30 – 5:00)

“TTrack delivers faster, more accurate progress tracking and reduces administrative workload.”

“We believe this tool can be extended for other degree programs and integrated into institutional systems in the future.”

“Thank you for watching, and we are happy to take any questions.”

## ICR
Name: [Your Name]
Project: TTrack – Torrens Degree Tracker
Date: [Submission Date]

Tasks Worked On (with Dates):

Date	Task Description	Outcome
20/07/2025	Implemented matching engine logic to compare transcripts with curriculum	Matching results correctly display ✅ Done/Missing
25/07/2025	Integrated sample data and file upload module	Users can test app without uploading their own files
28/07/2025	Developed export-to-CSV feature for progress reports	Allows external use of results
03/08/2025	Fixed PyQt layout responsiveness for macOS	UI now consistent across platforms
05/08/2025	Performed QA tests and bug fixes for final demo	No critical bugs remaining

Problems Faced:

PyQt interface behaving differently between Windows and macOS.

CSV parsing errors when file headers had extra spaces.

Version conflicts with certain Python libraries on macOS.

Proposed Solutions:

For UI differences: Adjusted layouts with flexible spacers and tested on both OS.

For CSV errors: Added preprocessing step to strip spaces and normalize headers.

For library issues: Locked dependencies in requirements.txt and used venv for isolation.

Final Chosen Solutions:

Implemented responsive PyQt layouts.

Added data preprocessing before matching logic runs.

Standardized environment setup instructions in README.