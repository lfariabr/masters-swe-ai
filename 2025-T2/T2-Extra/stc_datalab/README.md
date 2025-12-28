# Introduction

We're going to build a mini "School Data Platform" on SQL Server, and we'll document it like a real internal deliverable — so I don't just learn SQL, but also present proof.

This is structured as a 3-level assessment simulation `(Level 1 → Level 2 → Level 3)`, matching exactly what the role given calls for: **SQL queries + reporting, data integration/imports, documentation/training, and maintaining systems responsibly**.

## Execution Plan (Dec 2025 - Jan 2026)

| Date | Focus | Deliverables | Status |
|------|-------|-------------|----|
| **Dec 20-21** | Setup & Schema | SQL Server Express + SSMS installation, DB creation, table structure | ✅ |
| **Dec 22-23** | Backup & Restore | Full backup/restore procedures, documentation with screenshots | ✅ |
| **Dec 24-25** | Data Generation | Realistic seed data with edge cases | ✅ |
| **Dec 26-27** | Reporting Views | Student profiles, class rolls, attendance summaries | ✅ |
| **Dec 28-29** | Stored Procedures | Parameter-based queries, optimization | ✅ |
| **Dec 30-31** | Import/Export | CSV handling, staging tables, data validation | ✅ |
| **Jan 1-2** | Runbook & Documentation | Operational procedures, troubleshooting guide | ✅ |
| **Jan 3-4** | Demo Preparation | Presentation script, screenshots, talking points | ✅ |
| **Jan 5** | Final Review | Validate all components, practice demo | ⏱️ |

> [Complete changelog with 30+ commits](https://github.com/search?q=repo%3Alfariabr%2Fmasters-swe-ai++stc+OR+%28stc%29+OR+std+OR+%28std%29&type=commits&s=committer-date&o=desc)

---

## StC School Data Lab (Operational Simulation)

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

> Outcome: "Know the basics. Won't break production."
[Change history](https://github.com/lfariabr/masters-swe-ai/issues/91)

### Tasks
1. ✅ Install & connect -> https://www.youtube.com/watch?v=glxE7w4D8v8
-  SQL Server Express + SSMS (matching StC's on-premise setup)
-  Create DB: StC_SchoolLab
-  Configure basic security (matching school's confidentiality requirements)

2. ✅ Create schema (core tables)
- Students (with privacy-sensitive fields like in Synergetic)
- Staff (with role-based attributes)
- Subjects (matching school curriculum structure)
- Classes (with teacher assignments)
- Enrollments (student-class relationships)
- Attendance (simple tracking like SEQTA)

3. ✅ Basic SQL competence
- SELECT + WHERE + ORDER BY (for basic student/class queries)
- JOINS (especially LEFT JOIN for preserving all student records)
- GROUP BY aggregates (COUNT/SUM for attendance reporting)
- Basic indexing strategy (for performance)

4. ✅ Backup & restore
- Full backup (both GUI and T-SQL methods)
- Restore to a new DB name: StC_SchoolLab_RESTORE
- Document recovery point objectives

### Deliverables
- ✅ sql/00_create_db.sql, sql/01_schema.sql
- ✅ docs/Lvl1Task1.X.md (step-by-step setup and execution + screenshots)

### Passing standard
I can explain (out loud, calmly):
1. "What is a database vs schema vs table?"
- **R:** Database: the container for all data and objects for an application. 
- Schema: a logical namespace used to organise objects and manage permissions. 
- Table: stores the actual structured data.

Examples:
```bash
# Database: StC_SchoolLab 
- contains: students, staff, classes, attendance, etc

# Schema: 
- core: Core operational data (students, staff)
- academic: Classes, subjects, attendance
- reporting: Views used in powerBi

# Table: specific register or list
- core.Students: StudentId, StudentNumber, FirstName, LastName...
```

2. "When would you do a restore?"
- **R:** When there is data corruption, hardware failure, or accidental deletion to recover a previous state

3. "Why LEFT JOIN for reporting?"
- **R:** LEFT JOIN ensures all records from the left table (e.g., students) are included in the report, even if there are no matching records in the right table (e.g., enrollments), which is essential for complete reporting.

4. "How do you secure sensitive student data?"
- **R:** By implementing appropriate access controls, encryption, and data masking techniques to protect privacy-sensitive information.

---

## LEVEL 2 — Reporting & Data Integration Assessment

> Outcome: "Can generate real reports and move data between systems."
[Change history](https://github.com/lfariabr/masters-swe-ai/issues/92)

### Tasks
1. ✅ Seed realistic data
- 200 students, 20 staff, 30 classes, 500 enrollments (matching StC's scale)
- Include some NULLs and edge cases (missing phone, withdrawn student, international students)
- Add data quality issues that would need cleaning (simulating real-world scenarios)

2. ✅ Create reporting views (similar to what feeds Power BI at StC's)
- vw_StudentProfile (comprehensive student data for staff access)
- vw_ClassRoll (attendance tracking for teachers)
- vw_AttendanceSummary (aggregated metrics for leadership)
- vw_AcademicPerformance (simulating the effort/grades calculations)

3. ✅ Stored procedures (addressing specific school needs)
- sp_GetStudentProfile(@StudentId) (detailed student lookup)
- sp_EnrollmentSummaryByYear(@YearLevel) (class distribution reports)
- sp_AttendanceByDate(@Date) (daily attendance tracking)
- sp_GetTableDataExport(@TableName) (for system integration)

4. ✅ Import/export simulation (mimicking SEQTA integration)
- Create data/*.csv (formatted like actual school exports)
- Import into staging tables (e.g., Staging_Students)
- Validate row counts, deduplicate, then merge into real tables
- Document error handling for failed imports

### Deliverables
- ✅ sql/02_seed_data.sql, sql/03_views.sql, sql/04_stored_procedures.sql
- ✅ docs/Lvl2Task2.X.md (step-by-step execution + screenshots)

### Passing standard
I can explain:
1. "How I validate imports before trusting reports" (critical for SEQTA data)
- **R:** I never import CSVs straight into production tables. I land them in staging first, then validate before merge:
  - Row counts (imported vs valid vs invalid) tracked in `Import_Log`
  - Duplicate detection (e.g., repeated `student_number` within the batch)
  - Field validation (required fields, known-bad placeholders like `???`, pending addresses)
  - Non-destructive normalization where safe (emails lowercased for consistency; name casing only flagged to avoid corrupting names like McDonald/O’Brien)
  - Only records marked `is_valid = 1` are eligible for merge; merge is transaction-safe and supports explicit clears via the sentinel value `CLEAR`.

2. "Why views/stored procedures help non-technical reporting" (for staff access)
- **R:** Views and stored procedures give staff consistent “report-ready” interfaces:
  - Views standardise joins/aggregations (e.g., student profile, class roll, attendance summaries) so reports don’t re-implement logic differently in every query.
  - Stored procedures provide safe, parameterised access patterns (e.g., “get student profile by ID”, “attendance by date”) and reduce ad‑hoc query risk.
  - This supports least-privilege access: staff/tools can be granted access to views/procs without direct table access.

3. "How I avoid heavy queries impacting the operational system" (performance tuning)
- **R:** I reduce operational impact by design:
  - Index the high-traffic join/filter keys (student/class IDs, attendance date) and keep reporting logic in views/procs.
  - Prefer set-based queries, avoid row-by-row patterns, and keep filters sargable where possible.
  - Use staging/ETL patterns so validation and transformation work doesn’t lock production tables.
  - Operationally: schedule heavier exports/refreshes off-peak and monitor slow queries (then tune with execution plans if needed).

4. "How I'd handle the effort/grades calculations"
- **R:** I treat effort/grades as explicit business rules:
  - Implement once in a view/procedure (e.g., grade → points mapping + attendance-informed effort rating) so every report uses the same logic.
  - Validate with test slices (known students/classes) and reconcile outputs against expected examples.
  - Document assumptions/edge cases (missing grades, ‘INC’, mixed grade formats) and keep the mapping table/rules easy to update when policy changes.

---

## LEVEL 3 — Production Mindset Assessment

> Outcome: "Safe, documents well, and supports staff."
[Change history](https://github.com/lfariabr/masters-swe-ai/issues/93)

### Tasks
1. ✅ Operational Runbook
Write docs/06_runbook.md like an internal StC ICT doc:
- How to run backups (both GUI and T-SQL methods)
- How to restore in an emergency (with RPO/RTO considerations)
- How to run key reports (with screenshots and parameter explanations)
- Common incidents + what to check first (based on L's "firefighting" scenarios)
- Permissions principles (least privilege, child data protection, staff access levels)
- System integration monitoring (SEQTA imports, data warehouse feeds)

2. ✅ Troubleshooting scenarios
Document how you'd handle real StC scenarios:
- Report numbers don't match (e.g., attendance discrepancies between systems)
- Import failed halfway (e.g., SEQTA CSV import failure)
- Duplicate student records (data quality issue resolution)
- Performance issue on a report query (query optimization techniques)
- Missing data in Power BI reports (tracing data lineage)

3. ✅ Training material (for non-technical staff)
Write a simple one-pager tailored to teachers and administrators:
- "How to request a report" (process and expectations)
- "What details to include" (clear requirements template)
- "How to interpret columns" (data dictionary for common fields)
- "What we can/can't do (privacy/confidentiality)" (child safety compliance)
- "When to expect results" (SLAs and priorities)

4. ✅ Presentation script
Build docs/07_demo_script.md with StC context:
- 2-minute overview of the solution architecture
- 3 reports you'll demo (student profiles, attendance, academic performance)
- Backup/restore proof (disaster recovery demonstration)
- Import validation proof (data quality checks)
- "How I work with staff" (collaboration approach)
- Migration readiness (SharePoint to School Box considerations)

### Deliverables
- ✅ docs/06_runbook.md (comprehensive operations guide)
- ✅ docs/07_demo_script.md (interview presentation)
- ✅ 3 screenshots showing outputs in SSMS (report results, backup history, data validation)

### Passing standard
I can confidently say:
1. "I always confirm backups and restore capability before changes."
2. "I document assumptions so reports are reproducible."
3. "In a school environment, confidentiality and access control are non-negotiable."
4. "I can help bridge the gap between technical and non-technical staff."
5. "I understand how to maintain data integrity across multiple school systems."
---

## Interview "Showcase Pack"

These 3 items (digital or printed):
1. README.md (project overview + what was built)
2. Runbook (this screams maturity)
3. Demo script (so I don't ramble)

This directly maps to the job's needs: maintaining databases + SQL reports + integrations + documentation/training.

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