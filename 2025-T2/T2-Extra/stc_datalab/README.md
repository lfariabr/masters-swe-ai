# Introduction

We're going to build a mini "School Data Platform" on SQL Server, and we'll document it like a real internal deliverable — so I don't just learn SQL, but also present proof.

This is structured as a 3-level assessment simulation `(Level 1 → Level 2 → Level 3)`, matching exactly what the role given calls for: **SQL queries + reporting, data integration/imports, documentation/training, and maintaining systems responsibly**.

## Execution Plan (Dec 2025 - Jan 2026)

| Date | Focus | Deliverables |
|------|-------|-------------|
| **Dec 20-21** | Setup & Schema | SQL Server Express + SSMS installation, DB creation, table structure |
| **Dec 22-23** | Backup & Restore | Full backup/restore procedures, documentation with screenshots |
| **Dec 24-25** | Data Generation | Realistic seed data with edge cases |
| **Dec 26-27** | Reporting Views | Student profiles, class rolls, attendance summaries |
| **Dec 28-29** | Stored Procedures | Parameter-based queries, optimization |
| **Dec 30-31** | Import/Export | CSV handling, staging tables, data validation |
| **Jan 1-2** | Runbook & Documentation | Operational procedures, troubleshooting guide |
| **Jan 3-4** | Demo Preparation | Presentation script, screenshots, talking points |
| **Jan 5** | Final Review | Validate all components, practice demo |

---

## The Mini Project: "StC School Data Lab"

> Goal: Demonstrate I can maintain SQL Server data systems, run reporting, handle imports, and operate safely (backup/restore).

### Context from StC's Environment

Based on insights from L, this project simulates key aspects of StC's actual data environment:

- **On-premise SQL Server** with multiple school management systems
- **Data integration challenges** between systems with limited direct access (like SEQTA)
- **SSIS package simulation** for importing/transforming CSV exports
- **Reporting views** that would feed into Power BI dashboards
- **Documentation** that addresses real operational needs
- **Confidentiality and child safety** considerations for school data

### Key Challenges to Address

- **Legacy Systems**: Many on-premise systems with outdated architecture
- **Limited Documentation**: Previous developer code lacks proper documentation
- **Complex ETL Processes**: Especially for SEQTA data with custom calculations
- **Resource Constraints**: Team of 2 handling workload meant for 3 people
- **System Migration**: Upcoming SharePoint to School Box transition

Repo / Folder Structure (what you’ll build)
```bash
stc-sql-lab/
  README.md
  docs/
    01_setup.md
    02_schema.md
    03_reporting.md
    04_backup_restore.md
    05_import_export.md
    06_runbook.md
    07_demo_script.md
  sql/
    00_create_db.sql
    01_schema.sql
    02_seed_data.sql
    03_views.sql
    04_stored_procedures.sql
    05_indexes.sql
    06_reporting_queries.sql
    07_backup_restore.sql
  data/
    students.csv
    classes.csv
    enrollments.csv
  screenshots/
    ssms_db_created.png
    ssms_backup.png
    ssms_restore.png
    sample_report_output.png
```

---

## LEVEL 1 — Operator Fundamentals Assessment

> Outcome: "He knows the basics. He won't break production."

### Tasks
1. Install & connect -> https://www.youtube.com/watch?v=glxE7w4D8v8
-  SQL Server Express + SSMS (matching StC's on-premise setup)
-  Create DB: StC_SchoolLab
-  Configure basic security (matching school's confidentiality requirements)

2. Create schema (core tables)
- Students (with privacy-sensitive fields like in Synergetic)
- Staff (with role-based attributes)
- Subjects (matching school curriculum structure)
- Classes (with teacher assignments)
- Enrollments (student-class relationships)
- Attendance (simple tracking like SEQTA)

3. Basic SQL competence
- SELECT + WHERE + ORDER BY (for basic student/class queries)
- JOINS (especially LEFT JOIN for preserving all student records)
- GROUP BY aggregates (COUNT/SUM for attendance reporting)
- Basic indexing strategy (for performance)

4. Backup & restore
- Full backup (both GUI and T-SQL methods)
- Restore to a new DB name: StC_SchoolLab_RESTORE
- Document recovery point objectives

### Deliverables
- sql/00_create_db.sql, sql/01_schema.sql
- docs/01_setup.md (step-by-step setup + screenshots)
- docs/04_backup_restore.md (exact steps + screenshots)

### Passing standard
You can explain (out loud, calmly):
- "What is a database vs schema vs table?"
- "When would you do a restore?"
- "Why LEFT JOIN for reporting?"
- "How do you secure sensitive student data?"

---

## LEVEL 2 — Reporting & Data Integration Assessment

> Outcome: "He can generate real reports and move data between systems."

### Tasks
1. Seed realistic data
- 200 students, 20 staff, 30 classes, 500 enrollments (matching StC's scale)
- Include some NULLs and edge cases (missing phone, withdrawn student, international students)
- Add data quality issues that would need cleaning (simulating real-world scenarios)

2. Create reporting views (similar to what feeds Power BI at StC's)
- vw_StudentProfile (comprehensive student data for staff access)
- vw_ClassRoll (attendance tracking for teachers)
- vw_AttendanceSummary (aggregated metrics for leadership)
- vw_AcademicPerformance (simulating the effort/grades calculations)

3. Stored procedures (addressing specific school needs)
- sp_GetStudentProfile(@StudentId) (detailed student lookup)
- sp_EnrollmentSummaryByYear(@YearLevel) (class distribution reports)
- sp_AttendanceByDate(@Date) (daily attendance tracking)
- sp_GenerateCSVExport(@TableName) (for system integration)

4. Import/export simulation (mimicking SEQTA integration)
- Create data/*.csv (formatted like actual school exports)
- Import into staging tables (e.g., Staging_Students)
- Validate row counts, deduplicate, then merge into real tables
- Document error handling for failed imports

### Deliverables
- sql/02_seed_data.sql, sql/03_views.sql, sql/04_stored_procedures.sql
- sql/05_indexes.sql (performance optimization for reporting queries)
- docs/03_reporting.md, docs/05_import_export.md

### Passing standard
You can explain:
- "How I validate imports before trusting reports" (critical for SEQTA data)
- "Why views/stored procedures help non-technical reporting" (for staff access)
- "How I avoid heavy queries impacting the operational system" (performance tuning)
- "How I'd handle the effort/grades calculations"

---

## LEVEL 3 — Production Mindset Assessment

> Outcome: "This guy is safe, documents well, and supports staff."

### Tasks
1. Operational Runbook
Write docs/06_runbook.md like an internal StC ICT doc:
- How to run backups (both GUI and T-SQL methods)
- How to restore in an emergency (with RPO/RTO considerations)
- How to run key reports (with screenshots and parameter explanations)
- Common incidents + what to check first (based on L's "firefighting" scenarios)
- Permissions principles (least privilege, child data protection, staff access levels)
- System integration monitoring (SEQTA imports, data warehouse feeds)

2. Troubleshooting scenarios
Document how you'd handle real StC scenarios:
- Report numbers don't match (e.g., attendance discrepancies between systems)
- Import failed halfway (e.g., SEQTA CSV import failure)
- Duplicate student records (data quality issue resolution)
- Performance issue on a report query (query optimization techniques)
- Missing data in Power BI reports (tracing data lineage)

3. Training material (for non-technical staff)
Write a simple one-pager tailored to teachers and administrators:
- "How to request a report" (process and expectations)
- "What details to include" (clear requirements template)
- "How to interpret columns" (data dictionary for common fields)
- "What we can/can't do (privacy/confidentiality)" (child safety compliance)
- "When to expect results" (SLAs and priorities)

4. Presentation script
Build docs/07_demo_script.md with StC context:
- 2-minute overview of the solution architecture
- 3 reports you'll demo (student profiles, attendance, academic performance)
- Backup/restore proof (disaster recovery demonstration)
- Import validation proof (data quality checks)
- "How I work with staff" (collaboration approach)
- Migration readiness (SharePoint to School Box considerations)

### Deliverables
- docs/06_runbook.md (comprehensive operations guide)
- docs/07_demo_script.md (interview presentation)
- 3 screenshots showing outputs in SSMS (report results, backup history, data validation)

### Passing standard
You can confidently say:
- "I always confirm backups and restore capability before changes."
- "I document assumptions so reports are reproducible."
- "In a school environment, confidentiality and access control are non-negotiable."
- "I can help bridge the gap between technical and non-technical staff."
- "I understand how to maintain data integrity across multiple school systems."

---

## Interview “Showcase Pack” (What I'll bring to the table)

These 3 items (digital or printed):
1. README.md (project overview + what was built)
2. Runbook (this screams maturity)
3. Demo script (so I don’t ramble)

This directly maps to the job’s needs: maintaining databases + SQL reports + integrations + documentation/training.

## StC Systems Context

This project is designed with StC's actual environment in mind:

- **Multiple School Systems**: The school uses approximately 10 different systems including Synergetic (student CRM), SEQTA (attendance/grades), Canvas, and SharePoint
- **Data Warehouse**: Aggregates data from various systems for reporting
- **Power BI**: Used extensively for reporting, though currently not well-organized
- **Integration Challenges**: Some systems like SEQTA don't provide direct database access, requiring CSV exports and SSIS packages
- **On-Premise Infrastructure**: Many systems still run on-premise, with a gradual move toward cloud
- **Migration Projects**: SharePoint being replaced by School Box (cloud-based)
- **Resource Constraints**: Database team currently has 2 people (L and R) handling work for 3
- **Documentation Gaps**: Previous developers left complex queries and SSIS packages with minimal documentation

> See the complete systems architecture diagram in `docs/mermaid.md`