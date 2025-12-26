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
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -i /workspaces/stc_datalab/sql/03_reset_data.sql

# Seed the database
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -i /workspaces/stc_datalab/sql/02_seed_data.sql

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
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
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
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -i /workspaces/stc_datalab/sql/03_views.sql

# Codespaces Ubuntu validation query
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
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