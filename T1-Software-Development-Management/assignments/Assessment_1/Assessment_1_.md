# 📄 SDM404 Assessment 1 – Software Project Proposal and Plan

**Project Name:** TTrack – Degree Tracker  
**Group #** 1  
**Version:** 1.0.0  
**Date Created:** 24 June 2025

---

## Table of Contents

1. Introduction  
2. Project Proposal  
3. Project Management Plan  
4. Bibliography  
5. Contribution Log  
6. Appendices  

---

## 1. Introduction

### 1.1 Document Overview

This Software Project Management Plan (SPMP) outlines the proposal, planning, and execution strategy for the TTrack - Degree Tracker project, developed for Torrens University as part of the SDM404 Software Development Management subject.  

The document defines the project’s scope, objectives, development methodology, technical plan, schedule, budget, and risk management strategies.

### 1.2 Definitions / Glossary

| Term | Definition |
|------|------------|
| SDM404 | Software Development Management subject we are studying |
| SPMP | Software Project Management Plan |
| TTrack | Desktop application for tracking degree progress by comparing academic transcripts with curriculum requirements |
| Transcript | Excel file with completed courses and grades |
| Curriculum | Excel file defining required core, specialization, and elective subjects for a degree |
| GUI | Graphical User Interface |
| PyQt5 | Python library for desktop GUI apps |
| Matching Engine | Logic that compares transcript vs. curriculum |
| Dev | Development |

---

## 2. Project Proposal

### 2.1 Title of the project

TTrack – Degree Tracker

### 2.2 Problem Description

Torrens admin staff and students face a recurring challenge: tracking degree progress and ensuring no critical core or elective subjects are missing. Despite transcripts and course handbooks existing in separate silos, there is no smart, automated way to cross-check course history against degree requirements. The current manual process is error-prone and frustrating, leading to delays and potential graduation issues.

### 2.3 Proposed Solution

TTrack is a desktop application that automates the comparison of academic transcripts with degree curriculum requirements. It parses Excel files containing transcript and curriculum data, validates completed versus pending subjects, and provides a visual summary of academic progress.

The application operates offline, requiring no internet or admin intervention. Benefits include reduced workload for academic advisors, faster degree audits, and enhanced visibility for students into their degree path.

### 2.4 Features of the Product / Application

- Upload & parse transcript and curriculum Excel files (.xlsx)
- Match completed units to core, specialization and elective subjects
- Display subject status as Done, Missing or Invalid
- Provide a visual dashboard summarizing academic progress
- Elective suggestion engine based on unmet credits or required categories

---

## 3. Project Management Plan

### 3.1 Scope of the project

**In Scope:**  
- File upload and parsing for transcript and curriculum Excel files  
- Subject matching logic for core, specialization, and elective categories  
- Status indicators in the UI  
- Elective suggestion engine based on curriculum gaps  
- Visual dashboard with progress summaries

**Out of Scope:**  
- Real-time integration with academic systems  
- Web or mobile versions of the application

### 3.2 Assumptions, Constraints and Risks

**Assumptions:**  
- Transcript and curriculum Excel files follow a consistent structure.  
- Users have basic proficiency with desktop apps.  
- Project can be completed within the 12-week timeline.

**Constraints:**  
- Must finish by Week 12 (July 31, 2025).  
- Limited to 5 team members.  
- Offline-only operation.

**Risks:**  

| Date | Risk Description | Likelihood (1-5) | Impact (1-5) | Owner | Mitigation |
|------|------------------|------------------|-------------|-------|------------|
| 24/06/2025 | Inconsistent Excel file formats | 3 | 5 | Luis | Define strict input format guidelines; implement error handling |
| 24/06/2025 | Team member unavailability | 1 | 3 | All | Cross-train team; maintain documentation |
| 24/06/2025 | UI complexity overwhelms users | 3 | 3 | Rosa | Conduct usability testing; simplify UI |
| 26/06/2025 | Scope creep | 3 | 5 | Nomayer | Freeze scope during Sprint 2 |
| 26/06/2025 | Tech unfamiliarity (Supabase) | 5 | 3 | Victor | Assign learning in Sprint 1; fallback to local DB |
| 26/06/2025 | Data scalability | 1 | 5 | Hussain | Optimize parsing; test large files; caching |

### 3.3 Software Development Process

The team follows Scrum with 2-week sprints. This allows iterative development, rapid feedback, and continuous refinement.

**Process includes:**  
- Backlog management via GitHub
- Bi-weekly Sprint Planning
- Development and integration
- Reviews and Retrospectives

### 3.4 Technical Plan

TTrack may be implemented with either of these stacks:

**Python Stack:**  
- Python 3.10+  
- PyQt5  
- pandas & openpyxl  
- matplotlib  
- SQLite (optional)  
- PyInstaller

**Node.js Stack:**  
- ElectronJS  
- ReactJS  
- Node.js  
- xlsx (npm)  
- Chart.js  
- SQLite or JSON

Testing via Pytest (Python) or Jest (Node.js). Usability testing planned in Sprint 4.

### 3.5 Quality Management Plan

Quality ensured through:

- Code standards and reviews (GitHub PRs)
- Automated unit tests (Pytest/Jest)
- Usability testing with peers
- Documentation in code and external documents

### 3.6 Project Schedule

| Sprint | Tasks | Owner | Start | End |
|--------|-------|-------|-------|-----|
| Sprint 1 | UI structure, upload workflow | Rosa | 17/06 | 23/06 |
| Sprint 2 | Excel parsing, table view | Victor | 24/06 | 30/06 |
| Sprint 3 | Subject matching engine | Luis | 01/07 | 14/07 |
| Sprint 4 | Dashboard, electives logic | Hussain | 15/07 | 25/07 |
| Sprint 5 | Testing, polish, delivery | All | 26/07 | 31/07 |

### 3.7 Project Budget Estimates

| Role | Hours | Rate (AUD) | Cost (AUD) |
|------|-------|------------|------------|
| Project Manager | 30 | 45 | 2,100 |
| Frontend Dev | 40 | 40 | 2,400 |
| Backend Dev | 45 | 40 | 2,700 |
| DBM | 35 | 42 | 1,575 |
| Fullstack Dev | 40 | 42 | 2,400 |
| **Total** | **180** | - | **11,175** |

### 3.8 Resource Allocation Plan

| Team Member | Role | Main Tasks | Tools |
|-------------|------|------------|-------|
| Luis Faria | Full-Stack Dev + PM | Architecture, UI, Engine | Python, PyQt5, pandas |
| Hussain Jameel | Full-Stack Dev (Alt) | ElectronJS prototype, dashboard | NodeJS, React, Electron |
| Rosa Galvis | UI/UX Designer | Wireframes, themes | Figma, PyQt5 |
| Victor Dorantes | DB & Backend | Supabase, schema | PostgreSQL, Supabase |
| Nomayer Hossain | QA / Stakeholder Liaison | Testing, communication | Excel, QA test plans |

---

## 4. Bibliography

- Ahmad, M. O., Markkula, J., Oivo, M. (2013). Factors affecting software maintainability. Journal of Systems and Software.
- Cobb, C. G. (2015). The Project Manager’s Guide to Mastering Agile. Wiley.
- Ewusi-Mensah, K. (2003). Software Development Failures. MIT Press.
- Heath, F. (2021). The Professional Scrum Master Guide. Packt Publishing.
- Schwaber, K., & Sutherland, J. (2020). The Scrum Guide.
- Stephens, R. (2015). Beginning Software Engineering. Wrox Press.

---

## 5. Contribution Log

### Luis Faria

**Tasks Performed:** Led architecture, file parsing logic, PyQt5 UI, and matching engine.  
**Challenges:** Handling inconsistent data formats, balancing UI simplicity with feature-rich information.  
**Lessons Learned:** Applied Agile practices, enhanced skills in version control, GUI design, and team collaboration.

### Nomayer Hossain

**Tasks Performed:** Created QA Test Log, executed manual testing.  
**Challenges:** Inconsistent stakeholder file formats.  
**Lessons Learned:** Importance of early feedback and clear stakeholder communication.

### Hussain Jameel

**Tasks Performed:** Developed ElectronJS prototype, focused on dynamic dashboards.  
**Challenges:** Cross-platform testing, evaluating tech alternatives like Tauri, NW.js.  
**Lessons Learned:** Research-driven decision-making, managing platform-specific builds.

### Rosa Galvis

**Tasks Performed:** Created wireframes, UI themes, dark mode designs.  
**Challenges:** Balancing aesthetics and functionality.  
**Lessons Learned:** Translating designs to PyQt5, effective collaboration with developers.

### Victor Dorantes

**Tasks Performed:** Designed DB schema, implemented Excel parsing.  
**Challenges:** Normalizing inconsistent Excel data, handling non-ASCII characters.  
**Lessons Learned:** Importance of data validation and Python deployment for apps.

---

## 6. Appendices

### 6.1 Sample Transcript and Curriculum

- Academic Transcript [.xlsx file](https://docs.google.com/spreadsheets/d/1UU8IYJF7eGxBe_l2ygdObkcxZae4irP6B74AdtAK9wQ)
- Course Curriculum [.xlsx file](https://docs.google.com/spreadsheets/d/1PdzsKB8ocSxMn3XVQ3HaaTXIEkeVMTqS9BSKoZNrOkc)

### 6.2 Screenshots

- **Figure A6:** UI Input Tab – displays file upload and data preview.
- **Figure A7:** UI Results Tab – shows matched subjects and progress indicators.
- **Figure A8:** GitHub Issue Board – visualizes sprint progress and task management.

GitHub Repository: [TTrack Project on GitHub](https://github.com/lfariabr/masters-swe-ai/tree/master/T1-Software-Development-Management/projects/TTrack_v1)

---
