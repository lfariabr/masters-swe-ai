**Level 2: Data Integrity & Reliability Assessment**

This level focuses on ensuring data consistency, reliability, and integrity within the SQL Server environment. It builds upon the foundational setup from Level 1 by implementing robust data management practices, backup strategies, and integrity checks.

## 🎯 **Level 2 Overview: He can generate real reports and move data between systems.**
This level demonstrates the ability to maintain data quality, implement backup and recovery procedures, and ensure data can be reliably extracted and moved between systems while maintaining integrity.

---

## **Task 1: Seed Realistic Data** ✅

### **What I've Done:**
Created `sql/02_seed_data.sql` with deterministic data generation using CTEs and table variables to populate:
- **200 students** with varied demographics and quality issues
- **20 staff members** across different roles (teachers, admin, counsellor, ICT, support)
- **12 subjects** covering core curriculum areas (Math, English, Science, Humanities, Arts, Technology)
- **30 classes** with teacher assignments and scheduling
- **500 enrollments** with mixed statuses (Active, Withdrawn, Completed, Pending)
- **800 attendance records** across 10 days for reporting validation

### **Intentional Data Quality Issues (for testing):**
- **NULL values**: Missing phone numbers (9% of students), missing emergency contacts, NULL emails for support staff
- **Casing inconsistencies**: Lowercase first names, uppercase emails, trailing spaces in last names
- **International scenarios**: Singapore/Jakarta addresses for boarding students
- **Duplicate data**: Shared email addresses to test deduplication logic
- **Edge cases**: Withdrawn students with withdrawal dates, incomplete grades ('INC'), inconsistent grade formats ('A ', 'b')
- **Invalid data**: Phone numbers marked as '???', addresses marked as 'Address Pending'

### **Why It Matters:**
Real school data is messy. This simulates actual data quality challenges from systems like SEQTA and Synergetic, proving I can handle imports that need validation, cleaning, and transformation before reporting.

### **Execution Results:**
```bash
# Codespaces Ubuntu
# Reset database first
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -i /workspaces/masters-swe-ai/2025-T2/T2-Extra/stc_datalab/sql/03_reset_data.sql

# Seed the database
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -i /workspaces/masters-swe-ai/2025-T2/T2-Extra/stc_datalab/sql/02_seed_data.sql

# macOs
# Reset database first
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -i /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2025-T2/T2-Extra/stc_datalab/sql/03_reset_data.sql

# Seed the database
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -i /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2025-T2/T2-Extra/stc_datalab/sql/02_seed_data.sql
```

**Output:**
```bash
--- Level 2 Task 2.1: Seeding realistic demo data ---
Subjects inserted: 12
Staff inserted: 20
Students inserted: 200
Classes inserted: 30
Enrollments inserted: 500
Attendance inserted: 800
--- Summary after seeding ---
Subjects total: 12
Staff total: 20
Students total: 200
Classes total: 30
Enrollments total: 500
Attendance total: 800
Seed script completed with intentional nulls, casing issues, and international scenarios for reporting tests.
```

### **Validation Query:**
```bash
# Verify row counts per table (macOS)
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; SELECT 'Students' AS TableName, COUNT(*) AS Total FROM Students UNION ALL SELECT 'Staff', COUNT(*) FROM Staff UNION ALL SELECT 'Classes', COUNT(*) FROM Classes UNION ALL SELECT 'Enrollments', COUNT(*) FROM Enrollments UNION ALL SELECT 'Attendance', COUNT(*) FROM Attendance;"

# Verify row counts per table (Codespaces Ubuntu)
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; SELECT 'Students' AS TableName, COUNT(*) AS Total FROM Students UNION ALL SELECT 'Staff', COUNT(*) FROM Staff UNION ALL SELECT 'Classes', COUNT(*) FROM Classes UNION ALL SELECT 'Enrollments', COUNT(*) FROM Enrollments UNION ALL SELECT 'Attendance', COUNT(*) FROM Attendance;"
```

**Expected Output:**
```bash
TableName    Total
------------ -----------
Students     200
Staff        20
Classes      30
Enrollments  500
Attendance   800
```

---

## **Task 2: Create reporting views**

### **What I've Done:**
Created four essential reporting views that simulate the kind of data access needed at StC:

1. View 1: **vw_StudentProfile**
Comprehensive student data aggregating enrollments and attendance:
- Student demographics (name, age, contact info)
- Medical info flag (privacy-masked)
- Enrollment summary (active/completed/withdrawn counts)
- Attendance metrics (days present/absent/late, attendance rate %)

2. View 2: **vw_ClassRoll**
Daily class roll for teachers:
- Class details (name, subject, teacher, room, schedule)
- Student roster with enrollment status
- Per-student attendance summary for the class
- Class capacity metrics (current enrollment, available seats)
- Latest attendance status per student

3. View 3: **vw_AttendanceSummary**
Aggregated metrics for leadership dashboards:
- Date dimensions (day/week/month/year)
- Class-level attendance counts by status
- Attendance and absence rates
- Teacher and marker information
- Trend analysis ready (grouped by date + class)

4. View 4: **vw_AcademicPerformance**
Student performance with effort/grades calculations:
- Final grades with grade point conversion (A=4.0, B+=3.5, etc.)
- Attendance-based effort rating (Outstanding/Good/Satisfactory/Needs Improvement)
- Academic standing indicator (Good Standing/At Risk/Failing)
- Classes attended vs total classes
- Subject credits for GPA calculations

### **Why It Matters:**
Reporting views are the backbone of any data platform. They provide a consistent, secure way to access data for reporting, analysis, and decision-making. This simulates the kind of reporting StC needs for staff and leadership, ensuring I can handle the complexity of real-world data while maintaining data integrity and security.

### **Execution Results:**

```bash
# macOs script to create views
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -i /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2025-T2/T2-Extra/stc_datalab/sql/03_views.sql

# macOs validation query
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; SELECT TOP 10 student_name, final_grade, grade_points, academic_standing, effort_rating FROM vw_AcademicPerformance WHERE final_grade IS NOT NULL ORDER BY student_id, class_id;"

# Codespaces Ubuntu script to create views
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -i /workspaces/masters-swe-ai/2025-T2/T2-Extra/stc_datalab/sql/03_views.sql

# Codespaces Ubuntu validation query
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; SELECT TOP 10 student_name, final_grade, grade_points, academic_standing, effort_rating FROM vw_AcademicPerformance WHERE final_grade IS NOT NULL ORDER BY student_id, class_id;"

# Expected Output:
Changed database context to 'StC_SchoolLab'.
student_name                                                                                          final_grade grade_points academic_standing effort_rating    
----------------------------------------------------------------------------------------------------- ----------- ------------ ----------------- -----------------
Oliver Smith                                                                                          B+                   3.3 Good Standing     Needs Improvement
Oliver Smith                                                                                          B                    3.0 Good Standing     Needs Improvement
Oliver Smith                                                                                          C                    2.0 At Risk           Needs Improvement
Oliver Smith                                                                                          D                    1.0 At Risk           Needs Improvement
Oliver Smith                                                                                          A                    4.0 Good Standing     Needs Improvement
Oliver Smith                                                                                          B+                   3.3 Good Standing     Needs Improvement
Oliver Smith                                                                                          B                    3.0 Good Standing     Needs Improvement
Oliver Smith                                                                                          C                    2.0 At Risk           Needs Improvement
Oliver Smith                                                                                          A                    4.0 Good Standing     Needs Improvement
Oliver Smith                                                                                          A                    4.0 Good Standing     Needs Improvement

(10 rows affected)
```

---

## **Task 3: Stored procedures**

### **What I've Done:**
Created `sql/04_stored_procedures.sql` file with the following stored procedures:

1. Procedure: sp_GetStudentProfile(@StudentId)

**Purpose:** Detailed student lookup for staff access

**Features:**
- Input validation (positive integer, student exists)
- Returns 3 result sets:
  1. Comprehensive student profile from `vw_StudentProfile`
  2. Current enrollments with class/teacher details
  3. Recent attendance (last 30 days)
- Error handling with descriptive messages

**Use Case:** Student information retrieval, parent-teacher meetings, counseling sessions

2. Procedure: sp_EnrollmentSummaryByYear(@YearLevel)

**Purpose:** Class distribution reports by year level (7-12)
**Features:**
- Input validation (year level 7-12 for secondary school)
- Returns 2 result sets:
  1. Per-class enrollment metrics (active/completed/withdrawn counts, capacity utilization, enrollment status)
  2. Year-level summary statistics (total classes, subjects, teachers, overall utilization)
- Capacity indicators: Full, Near Capacity, Available, Under-enrolled

**Use Case:** Enrollment planning, capacity management, resource allocation

3. Procedure: sp_AttendanceByDate(@Date)
**Purpose:** Daily attendance tracking for operational reporting

**Features:**
- Returns 3 result sets:
  1. All attendance records for the specified date with student/class/teacher details
  2. Daily summary statistics (total marked, present/absent/late/excused counts, rates)
  3. Students with absences (for follow-up with contact information)
- Includes day of the week for context

**Use Case:** Daily roll call verification, absence follow-up, compliance reporting

4. Procedure: sp_GetTableDataExport(@TableName)

**Purpose:** Export filtered table/view data for system integration (SEQTA, Power BI)

**Features:**
- Dynamic SQL routing based on table/view name
- Optional `@TopN` parameter for limiting rows
- Supported exports: Students, Staff, Classes, Enrollments, Attendance, vw_StudentProfile, Vw_AcademicPerformance
- Returns standard SQL result sets (client tools handle CSV serialization)
- Returns export metadata (table name, timestamp, row count)
- Includes joins for human-readable exports (e.g., teacher names, student names)

**Use Case:** Data export for external systems, reporting tools, backups

### **Why It Matters:**
Stored procedures are a key component of any data platform. They provide a secure, consistent way to access data for reporting, analysis, and decision-making. 

This simulates the kind of stored procedures StC needs for staff and leadership, ensuring I can handle the complexity of real-world data while maintaining data integrity and security.

### **Execution Results:**

```bash
# macOs script to create all procedures
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -i /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2025-T2/T2-Extra/stc_datalab/sql/04_stored_procedures.sql

# macOs test each procedures

# Test sp_GetStudentProfile
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; EXEC sp_GetStudentProfile @StudentId = 1;"

# Test sp_EnrollmentSummaryByYear
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; EXEC sp_EnrollmentSummaryByYear @YearLevel = 8;"

# Test sp_AttendanceByDate (use a date from your seed data)
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; EXEC sp_AttendanceByDate @Date = '2025-01-15';"

# Test sp_GetTableDataExport
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; EXEC sp_GetTableDataExport @TableName = 'STUDENTS', @TopN = 5;"

# Codespaces Ubuntu script to create all procedures
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -i /workspaces/masters-swe-ai/2025-T2/T2-Extra/stc_datalab/sql/04_stored_procedures.sql

# Codespaces Ubuntu test each procedures

# Test sp_GetStudentProfile
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; EXEC sp_GetStudentProfile @StudentId = 1;"

# Test sp_EnrollmentSummaryByYear
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; EXEC sp_EnrollmentSummaryByYear @YearLevel = 8;"

# Test sp_AttendanceByDate (use a date from your seed data)
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; EXEC sp_AttendanceByDate @Date = '2025-01-15';"

# Test sp_GetTableDataExport
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; EXEC sp_GetTableDataExport @TableName = 'STUDENTS', @TopN = 5;"
```

---

## **Task 4: Import/export simulation** ✅

### **What I've Done:**
Created a complete import/export workflow mimicking SEQTA integration with the following components:

**1. CSV Sample Files (`data/` folder):**
- `students_import.csv` - 13 rows with intentional data quality issues
- `classes_import.csv` - 8 class records with teacher assignments  
- `enrollments_import.csv` - 13 enrollment records with duplicates

**Intentional Issues for Testing:**
- Duplicate records (STU2025001 appears twice)
- Invalid phone numbers ('???')
- Missing fields (NULL phones, NULL emergency contacts)
- Casing inconsistencies (lowercase names, UPPERCASE emails)
- Trailing spaces in names
- Pending addresses

**2. Staging Tables (`sql/05_import_export.sql`):**
- `Staging_Students` - Loose constraints, validation flags, error tracking
- `Staging_Classes` - For class imports
- `Staging_Enrollments` - For enrollment imports
- `Import_Log` - Batch tracking with row counts and status

**3. Validation Stored Procedure (`sp_ValidateStagingStudents`):**
- Required field checks (student_number, first_name, last_name, DOB)
- Invalid data detection ('???' phones, 'Pending' addresses)
- Duplicate detection within batch
- Normalize emails to lowercase for consistency
- Trailing whitespace cleanup
- Returns validation summary and invalid records for review

**4. Merge Stored Procedure (`sp_MergeStagingStudents`):**
- Inserts new records (not in production)
- Optional update of existing records (@ForceUpdate = 1)
- Transaction-safe with rollback on error
- Updates Import_Log with merge counts
- Returns summary of inserted/updated/skipped rows

**5. Export Stored Procedure (`sp_ExportStudentData`):**
- Three export formats: FULL, BASIC, ATTENDANCE
- Filters by year level and active status
- Returns export metadata (format, row count, timestamp)
- Ready for Power BI or external system consumption

### **Why It Matters:**
This simulates how StC handles SEQTA CSV imports:
- **Real data is messy**: Schools receive exports with duplicates, missing fields, casing issues
- **Staging before production**: Never import directly to production tables
- **Validation first**: Catch errors before they corrupt reporting
- **Audit trail**: Import_Log tracks what was imported, when, and what failed
- **Rollback capability**: Transactions ensure partial imports don't leave bad data
- **Export for integration**: Power BI and external systems need clean, consistent data

### **Execution Results:**

```bash
# Codespaces Ubuntu - Run the import/export script
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -i /workspaces/masters-swe-ai/2025-T2/T2-Extra/stc_datalab/sql/05_import_export.sql

# macOS - Run the import/export script
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -i /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2025-T2/T2-Extra/stc_datalab/sql/05_import_export.sql
```

**Expected Output:**
```
--- Creating Staging Tables ---
Staging tables created successfully.
...
=====================================================
DEMO: Simulated Import Workflow
=====================================================
Created batch: IMPORT_20251228_120000
Rows imported to staging: 13
--- Running Validation ---

total_rows  valid_rows  invalid_rows  duplicate_rows
----------- ----------- ------------- --------------
13          10          3             1

--- Staging Data After Validation ---
staging_id  student_number  first_name  last_name  is_valid  validation_errors
----------  --------------  ----------  ---------  --------  ------------------
1           STU2025001      Emma        Johnson    1         NULL
2           STU2025002      Liam        Williams   1         NULL
3           STU2025003      olivia      Brown      1         Warning: lowercase first name detected
4           STU2025004      Noah        Taylor     1         NULL
5           STU2025005      Ava         Anderson   0         Invalid phone number
6           STU2025006      William     Thomas     1         Fixed: trailing space; Fixed: email lowercased
7           STU2025007      Sophia      Jackson    1         NULL
8           STU2025008      James       White      1         NULL
9           STU2025009      Isabella    Harris     0         Address pending - needs update
10          STU2025010      Oliver      Martin     1         NULL
11          STU2025011      Mia         Garcia     1         NULL
12          STU2025012      Benjamin    Lee        1         NULL
13          STU2025001      Emma        Johnson    0         Duplicate student_number in batch

Note: name casing is only *flagged* (warning) rather than auto-corrected, to avoid breaking real-world names like McDonald, O'Brien, van der Berg, and hyphenated surnames.

To intentionally clear a nullable field during merge (e.g., address/phone/email/emergency fields), set the staging value to the sentinel string `CLEAR`.
```

### **Testing the Merge:**
```bash
# After validation, merge valid records to production
# Codespaces Ubuntu
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; EXEC sp_MergeStagingStudents @ImportBatch = 'IMPORT_20251228_120000';"

# Test export procedure (FULL format)
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; EXEC sp_ExportStudentData @Format = 'BASIC', @ActiveOnly = 1;"

# Test export for attendance (Year 8)
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; EXEC sp_ExportStudentData @Format = 'ATTENDANCE', @YearLevel = 8;"
```

### **Files Created:**
- `data/students_import.csv` - Sample student import file
- `data/classes_import.csv` - Sample class import file
- `data/enrollments_import.csv` - Sample enrollment import file
- `sql/05_import_export.sql` - Staging tables, validation, merge, export procedures

---


