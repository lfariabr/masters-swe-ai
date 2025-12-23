# Level 1 Task 3: Basic SQL Competence

## Overview
This task demonstrates fundamental SQL skills required for database operations: SELECT with WHERE/ORDER BY, JOINs (especially LEFT JOIN), and GROUP BY aggregates. These are essential for basic student/class queries and attendance reporting.

## Step-by-Step Commands

### 1. Execute Sample Data and Queries Script
```bash
# Codespaces Ubuntu
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -i /workspaces/masters-swe-ai/2025-T2/T2-Extra/stc_datalab/sql/02_sample_queries.sql

# macOs 
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -i /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2025-T2/T2-Extra/stc_datalab/sql/02_sample_queries.sql
```
**Purpose**: Inserts sample data and runs demonstration queries.
- Inserts: 3 staff, 3 subjects, 3 classes, 4 students, 9 enrollments, 6 attendance records
- Runs 5 different query types to show SQL competence

## Query Demonstrations

### SELECT + WHERE + ORDER BY
```sql
SELECT student_id, first_name, last_name, enrollment_year
FROM Students
WHERE enrollment_year = 2025
ORDER BY last_name;
```
**Purpose**: Basic filtering and sorting for student queries.
- Filters by enrollment year
- Orders alphabetically by last name
- Shows all 2025 students

### LEFT JOIN for Complete Records
```sql
SELECT s.first_name, s.last_name, c.class_name, e.enrollment_date
FROM Students s
LEFT JOIN Enrollments e ON s.student_id = e.student_id
LEFT JOIN Classes c ON e.class_id = c.class_id
ORDER BY s.last_name, c.class_name;
```
**Purpose**: Preserves all student records even if not enrolled.
- LEFT JOIN ensures all students appear
- Shows enrollment relationships
- Critical for reporting (students without classes still show)

### GROUP BY Aggregates
```sql
SELECT status, COUNT(*) as count
FROM Attendance
WHERE attendance_date = '2025-12-20'
GROUP BY status
ORDER BY count DESC;
```
**Purpose**: Attendance summary reporting.
- Groups by attendance status
- Counts occurrences
- Orders by frequency

### Complex Aggregation: Attendance Percentage
```sql
SELECT s.first_name, s.last_name,
       COUNT(a.attendance_id) as total_days,
       SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_days,
       CAST(SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.attendance_id) AS DECIMAL(5,2)) as attendance_percentage
FROM Students s
LEFT JOIN Attendance a ON s.student_id = a.student_id
GROUP BY s.student_id, s.first_name, s.last_name
ORDER BY attendance_percentage DESC;
```
**Purpose**: Student attendance percentage calculation.
- Uses CASE for conditional counting
- Calculates percentage with decimal precision
- LEFT JOIN includes students with no attendance records

### Class Enrollment Summary
```sql
SELECT c.class_name, st.first_name + ' ' + st.last_name as teacher,
       COUNT(e.student_id) as enrolled_students
FROM Classes c
JOIN Staff st ON c.staff_id = st.staff_id
LEFT JOIN Enrollments e ON c.class_id = e.class_id
GROUP BY c.class_id, c.class_name, st.first_name, st.last_name
ORDER BY enrolled_students DESC;
```
**Purpose**: Class capacity and teacher assignment reporting.
- Multi-table JOIN
- String concatenation for teacher names
- Counts enrolled students per class

## SQL Concepts Demonstrated
- **Basic Filtering**: WHERE clauses for specific criteria
- **Sorting**: ORDER BY for predictable results
- **Relationships**: JOINs between related tables
- **Data Preservation**: LEFT JOIN for complete datasets
- **Aggregation**: GROUP BY with COUNT, SUM
- **Conditional Logic**: CASE statements for status counting
- **Type Conversion**: CAST for percentage calculations
- **String Operations**: Concatenation for full names

## Notes
- All queries use proper table aliases for readability
- WHERE clauses filter relevant data (e.g., current date)
- ORDER BY ensures consistent, useful output
- LEFT JOINs prevent missing records in reports
- Aggregations provide summary insights
- Queries match real school reporting needs
- Useful commands:

### Load sample data 
```bash
# Codespaces Ubuntu
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -i /workspaces/masters-swe-ai/2025-T2/T2-Extra/stc_datalab/sql/02_sample_queries.sql

# Macos 
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -i /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2025-T2/T2-Extra/stc_datalab/sql/02_sample_queries.sql
```

### Reset data

Created `sql/03_reset_data.sql` with ordered deletes and identity reseeds so the demo DB can be cleared safely before re-running seed scripts

```bash
# Codespaces Ubuntu
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -i /workspaces/masters-swe-ai/2025-T2/T2-Extra/stc_datalab/sql/03_reset_data.sql

# Macos 
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -i /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2025-T2/T2-Extra/stc_datalab/sql/03_reset_data.sql
```

### Preview some data: 
```bash
# Codespaces Ubuntu
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -Q "USE StC_SchoolLab; SELECT TOP 3 student_id, first_name, last_name, enrollment_year FROM Students; SELECT TOP 3 class_id, class_name, year_level FROM Classes; SELECT TOP 3 staff_id, first_name, last_name, role FROM Staff;"
# MacOs
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -Q "USE StC_SchoolLab;
      SELECT TOP 3 student_id, first_name, last_name, enrollment_year FROM Students;
      SELECT TOP 3 class_id, class_name, year_level FROM Classes;
      SELECT TOP 3 staff_id, first_name, last_name, role FROM Staff;"
```