## 🎯 **StC School Data Lab – Interview Flash Cards**

### **📌 PROJECT OVERVIEW**

**Q:  What is this project? **  
**A:** A 3-level SQL Server simulation for a school data platform.  It demonstrates: 
- SQL Server setup, schema design, and data operations
- Reporting views (for Power BI), stored procedures, and import/export workflows
- Backup/restore capabilities and operational documentation  
**Goal:** Prove I can maintain on-premise SQL systems, run reports, handle data imports, and document safely.

---

### **📌 LEVEL 1 – OPERATOR FUNDAMENTALS**

**Q: What does Level 1 cover?**  
**A:**  
✅ **Install & Connect**: SQL Server Express + SSMS  
✅ **Schema**:  6 core tables (Students, Staff, Subjects, Classes, Enrollments, Attendance)  
✅ **SQL Basics**: SELECT, WHERE, ORDER BY, JOINS (especially LEFT JOIN), GROUP BY, indexing  
✅ **Backup & Restore**: Full backup + restore to StC_SchoolLab_RESTORE 

**Q: Database vs Schema vs Table? **  
**A:**  
- **Database**: Container for all data (e.g., StC_SchoolLab)  
- **Schema**: Logical namespace to organize objects (e.g., core, academic, reporting)  
- **Table**: Stores actual structured data (e.g., Students with StudentId, FirstName, LastName)

**Q: When to restore a database?**  
**A:** Data corruption, hardware failure, accidental deletion → recover to a previous state. 

**Q: Why LEFT JOIN for reporting?**  
**A:** Preserves all records from left table (e.g., all students), even if no matching records on right (e.g., no enrollments yet). Critical for comprehensive reports.

---

### **📌 LEVEL 2 – REPORTING & DATA INTEGRATION**

**Q: What does Level 2 cover?**  
**A:**  
✅ **Seed Data**: 200 students, 20 staff, 30 classes, 500 enrollments with edge cases (NULLs, withdrawn students, internationals)  
✅ **Reporting Views**: vw_StudentProfile, vw_ClassRoll, vw_AttendanceSummary, vw_AcademicPerformance  
✅ **Stored Procedures**: sp_GetStudentProfile, sp_EnrollmentSummaryByYear, sp_AttendanceByDate, sp_GetTableDataExport  
✅ **Import/Export**: CSV → Staging tables → Validation → Merge into production (SEQTA-style)

**Q: How do you validate imports?**  
**A:**  
1. **Land CSVs in staging tables** (never direct to production)  
2. **Validate**:  Row counts, duplicates, required fields, known-bad placeholders (??? , Address Pending)  
3. **Mark valid records** (is_valid = 1)  
4. **Merge**: Transaction-safe, only valid records promoted to production  
5. **Log everything**: Import_Log table tracks batch status, errors, row counts

**Q: Why views and stored procedures? **  
**A:**  
- **Views**:  Standardize joins/aggregations → consistent reports, no logic duplication  
- **Stored Procedures**: Safe parameterized access → reduce ad-hoc query risk, support least-privilege security  
- **Benefit**: Non-technical staff get "report-ready" interfaces without direct table access

**Q: How to avoid heavy queries impacting operations?**  
**A:**  
- **Index** high-traffic keys (student/class IDs, dates)  
- **Use views/procs** for reporting logic  
- **Staging/ETL patterns** so validation doesn't lock production  
- **Schedule heavy exports off-peak**, monitor slow queries with execution plans

---

### **📌 LEVEL 3 – PRODUCTION MINDSET**

**Q: What does Level 3 cover?**  
**A:**  
✅ **Operational Runbook**: Backup/restore, key reports, incidents, permissions, monitoring  
✅ **Troubleshooting Scenarios**: Report discrepancies, import failures, duplicates, performance, missing data  
✅ **Training Material**: One-pager for teachers/admin (how to request reports, interpret columns, privacy)  
✅ **Demo Script**: 2-min architecture overview, 3 reports demo, backup proof, import validation, collaboration approach

**Q: Key principles for school data? **  
**A:**  
1. **Confirm backups** before changes  
2. **Document assumptions** for reproducibility  
3. **Confidentiality and access control** are non-negotiable (child safety)  
4. **Bridge technical ↔ non-technical staff**  
5. **Maintain data integrity** across multiple school systems

---

### **📌 REAL-WORLD CONTEXT (StC Environment)**

**Q: What systems does StC use?**  
**A:**  
- **On-premise SQL Server** with ~10 school systems  
- **Synergetic** (student CRM), **SEQTA** (attendance/grades – limited DB access, CSV exports only), **Canvas**, **SharePoint**  
- **Data Warehouse** → aggregates for **Power BI** reports  
- **SSIS packages** for ETL (poorly documented)  
- **Migration**:  SharePoint → School Box (cloud)

**Q: Key challenges at StC?**  
**A:**  
- **Legacy systems** with outdated architecture  
- **Limited documentation** (previous dev code lacks clarity)  
- **Complex ETL** (SEQTA calculations)  
- **Resource constraints** (2-person team, workload for 3)  
- **System migrations** in progress

---

### **📌 KEY SQL FILES**

| File | Purpose |
|------|---------|
| 00_create_db.sql | Create database + basic user security |
| 01_schema.sql | Define 6 core tables with relationships |
| 02_seed_data.sql | Insert realistic demo data (200 students, etc.) |
| 03_views.sql | Reporting views (StudentProfile, ClassRoll, Attendance) |
| 04_stored_procedures.sql | Operational procedures (GetStudentProfile, etc.) |
| 05_import_export.sql | Staging tables + import validation + merge logic |
| 07_backup_restore.sql | Full backup + restore procedures |

---

### **📌 DATA QUALITY EXAMPLES (from CSVs)**

**Edge Cases in students_import.csv:**
- Missing phone:  olivia (STU2025003)  
- Missing emergency contact: Noah (STU2025004)  
- Invalid phone (??? ): Ava (STU2025005)  
- Case inconsistency: William (WILLIAM.THOMAS@...  all caps email)  
- Address pending: Isabella (STU2025009)  
- International students: Mia (Singapore), Benjamin (Jakarta)  
- **Duplicate**:  Emma Johnson appears twice (STU2025001)

**Why this matters:**  
Shows you understand real-world data quality issues and validate imports before trusting reports.

---

### **📌 TALKING POINTS FOR INTERVIEW**

1. **"I built a production-style SQL Server lab that simulates StC's environment"**  
   → Shows initiative, understanding of on-premise systems

2. **"I implemented staging/validation patterns like SEQTA imports"**  
   → Directly relevant to their CSV integration challenges

3. **"I created reporting views that feed Power BI, with stored procs for staff access"**  
   → Matches their actual workflow

4. **"I documented everything:  runbooks, troubleshooting, training for non-technical staff"**  
   → Addresses their documentation gap pain point

5. **"I understand confidentiality and access control for child data"**  
   → Critical for school environment