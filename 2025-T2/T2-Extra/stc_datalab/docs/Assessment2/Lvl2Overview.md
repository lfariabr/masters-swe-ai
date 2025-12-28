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

## **Task 4: Import/export simulation**

### **What I've Done:**

### **Why It Matters:**

### **Execution Results:**

---


