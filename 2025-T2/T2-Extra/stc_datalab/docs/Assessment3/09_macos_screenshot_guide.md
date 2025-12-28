# macOS Screenshot Capture Guide - StC SchoolLab Database
**For macOS Users Without SSMS**

This guide provides two methods for capturing demonstration screenshots on macOS:
1. Terminal commands using `sqlcmd`
2. VS Code Database Client extension

---

## Method 1: Terminal Commands with sqlcmd

### Prerequisites
- SQL Server running on macOS (via Docker or native installation)
- `sqlcmd` installed (via Homebrew: `/opt/homebrew/bin/sqlcmd`)
- Terminal access

### Output Formatting Tips
```bash
# For better readability, use these sqlcmd flags:
# -s "|"     : Column separator (pipe for table-like output)
# -W         : Remove trailing spaces
# -h -1      : Remove column headers (use -h 0 to keep them)
# -w 500     : Set line width to 500 characters
```

---

## Screenshot 1: Backup History

### Terminal Command
```bash
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -d msdb -W -s "|" -Q "
SELECT TOP 10
    database_name AS [Database],
    backup_start_date AS [Start Time],
    backup_finish_date AS [Finish Time],
    DATEDIFF(SECOND, backup_start_date, backup_finish_date) AS [Duration (sec)],
    CAST(backup_size / 1024.0 / 1024.0 AS DECIMAL(10,2)) AS [Size (MB)],
    CASE type
        WHEN 'D' THEN 'Full'
        WHEN 'I' THEN 'Differential'
        WHEN 'L' THEN 'Transaction Log'
        ELSE 'Other'
    END AS [Backup Type]
FROM msdb.dbo.backupset
WHERE database_name = 'StC_SchoolLab'
ORDER BY backup_start_date DESC;
"
```

### Expected Output
```
Database|Start Time|Finish Time|Duration (sec)|Size (MB)|Backup Type
StC_SchoolLab|2025-01-29 23:00:00|2025-01-29 23:00:01|1|7.50|Full
StC_SchoolLab|2025-01-29 17:00:00|2025-01-29 17:00:00|0|2.25|Differential
```

### Screenshot Capture
1. Run command in Terminal
2. Capture output with `Cmd + Shift + 4` (select area)
3. Save as `01_backup_history.jpeg`

---

## Screenshot 2: Student Profile Report

### Terminal Command
```bash
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -d StC_SchoolLab -W -s "|" -Q "
EXEC sp_GetStudentProfile @StudentId = 1;
"
```

### Expected Output (3 Result Sets)

**Result Set 1: Student Overview**
```
student_id|student_number|first_name|last_name|year_level|email|phone|total_enrollments|attendance_rate
1|STU001|John|Smith|8|john.smith@student.stc.edu.au|0412345678|5|94.20
```

**Result Set 2: Current Enrollments**
```
class_name|subject|teacher_name|current_grade|status
Math 8A|Mathematics|Ms. Johnson|B+|Active
English 8B|English|Mr. Davis|A|Active
```

**Result Set 3: Recent Attendance**
```
attendance_date|class_name|status
2025-01-28|Math 8A|Present
2025-01-27|Math 8A|Present
```

### Screenshot Capture
1. Run command in Terminal
2. Scroll to see all 3 result sets
3. Capture each result set separately or as one long screenshot
4. Save as `02_student_profile.jpeg`

---

## Screenshot 3: Daily Attendance Report

### Terminal Command
```bash
# First, get the most recent attendance date
ATTENDANCE_DATE=$(/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -d StC_SchoolLab -h -1 -W -Q "SELECT TOP 1 CONVERT(VARCHAR(10), attendance_date, 120) FROM Attendance ORDER BY attendance_date DESC;")

# Then run the attendance report
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -d StC_SchoolLab -W -s "|" -Q "
EXEC sp_AttendanceByDate @Date = '$ATTENDANCE_DATE';
"
```

### Alternative (Hardcoded Date)
```bash
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -d StC_SchoolLab -W -s "|" -Q "
EXEC sp_AttendanceByDate @Date = '2025-11-25';
"
```

### Expected Output (3 Result Sets)

**Result Set 1: All Attendance Records**
```
student_name|class_name|teacher_name|status
John Smith|Math 8A|Ms. Johnson|Present
Jane Doe|Math 8A|Ms. Johnson|Absent
```

**Result Set 2: Daily Summary**
```
total_marked|present_count|absent_count|late_count|excused_count|attendance_rate
50|45|3|1|1|90.00
```

**Result Set 3: Absent Students**
```
student_name|student_number|parent_email|parent_phone|status
Jane Doe|STU002|parent@email.com|0423456789|Absent
```

### Screenshot Capture
1. Run command in Terminal
2. Capture all 3 result sets
3. Save as `03_daily_attendance.jpeg`

---

## Screenshot 4: Enrollment Summary Report

### Terminal Command
```bash
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -d StC_SchoolLab -W -s "|" -Q "
EXEC sp_EnrollmentSummaryByYear @YearLevel = 8;
"
```

### Expected Output (2 Result Sets)

**Result Set 1: Class-Level Details**
```
class_name|subject|teacher_name|current_enrollment|max_capacity|utilization_pct|status
Math 8A|Mathematics|Ms. Johnson|28|30|93.33|Near Capacity
English 8B|English|Mr. Davis|20|30|66.67|Available
```

**Result Set 2: Year-Level Summary**
```
year_level|total_classes|total_subjects|total_teachers|total_capacity|total_enrolled|utilization_pct
8|5|5|5|150|117|78.00
```

### Screenshot Capture
1. Run command in Terminal
2. Capture both result sets
3. Save as `04_enrollment_summary.jpeg`

---

## Screenshot 5: Data Validation - Row Count Reconciliation

### Terminal Command
```bash
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -d StC_SchoolLab -W -s "|" -Q "
SELECT 'Students' AS [Table Name], COUNT(*) AS [Row Count] FROM Students
UNION ALL SELECT 'Staff', COUNT(*) FROM Staff
UNION ALL SELECT 'Classes', COUNT(*) FROM Classes
UNION ALL SELECT 'Enrollments', COUNT(*) FROM Enrollments
UNION ALL SELECT 'Attendance', COUNT(*) FROM Attendance
ORDER BY [Table Name];
"
```

### Expected Output
```
Table Name|Row Count
Attendance|2500
Classes|30
Enrollments|500
Staff|20
Students|100
```

### Screenshot Capture
1. Run command in Terminal
2. Capture output
3. Save as `05_row_count_validation.jpeg`

---

## Screenshot 6: Data Validation - Referential Integrity Check

### Terminal Command
```bash
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -d StC_SchoolLab -W -s "|" -Q "
SELECT 'Orphaned Enrollments' AS [Issue], COUNT(*) AS [Count]
FROM Enrollments e
LEFT JOIN Students s ON e.student_id = s.student_id
WHERE s.student_id IS NULL

UNION ALL

SELECT 'Orphaned Attendance (Student)', COUNT(*)
FROM Attendance a
LEFT JOIN Students s ON a.student_id = s.student_id
WHERE s.student_id IS NULL

UNION ALL

SELECT 'Orphaned Attendance (Class)', COUNT(*)
FROM Attendance a
LEFT JOIN Classes c ON a.class_id = c.class_id
WHERE c.class_id IS NULL

UNION ALL

SELECT 'Enrollments without Classes', COUNT(*)
FROM Enrollments e
LEFT JOIN Classes c ON e.class_id = c.class_id
WHERE c.class_id IS NULL;
"
```

### Expected Output (All Should Be 0)
```
Issue|Count
Orphaned Enrollments|0
Orphaned Attendance (Student)|0
Orphaned Attendance (Class)|0
Enrollments without Classes|0
```

### Screenshot Capture
1. Run command in Terminal
2. Capture output showing all zeros
3. Save as `06_referential_integrity.jpeg`

---

## Bonus Screenshots

### Database Health - Space Usage
```bash
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -d StC_SchoolLab -W -s "|" -Q "
EXEC sp_spaceused;
"
```

### SEQTA Import Monitoring
```bash
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -d StC_SchoolLab -W -s "|" -Q "
SELECT 
    'Students' AS [Import Source],
    MAX(created_date) AS [Last Import],
    COUNT(*) AS [Total Records],
    DATEDIFF(HOUR, MAX(created_date), GETDATE()) AS [Hours Since Import]
FROM Students
UNION ALL
SELECT 'Staff', MAX(created_date), COUNT(*), DATEDIFF(HOUR, MAX(created_date), GETDATE()) FROM Staff
UNION ALL
SELECT 'Classes', MAX(created_date), COUNT(*), DATEDIFF(HOUR, MAX(created_date), GETDATE()) FROM Classes;
"
```

## Screenshot
- Saved as `07_bonus_seqta_monitoring_db_health.jpeg`

---

## Method 2: VS Code Database Client Extension

### Step 1: Install Database Client Extension

1. Open VS Code
2. Go to Extensions (`Cmd + Shift + X`)
3. Search for "Database Client" by Weijan Chen
4. Click **Install**

### Step 2: Connect to SQL Server

1. Click the **Database** icon in the left sidebar (or `Cmd + Shift + P` → "Database: Connect")
2. Select **SQL Server**
3. Enter connection details:
   - **Host:** `localhost`
   - **Port:** `1433` (default)
   - **Username:** `sa`
   - **Password:** `StC_SchoolLab2025!`
   - **Database:** `StC_SchoolLab` (optional, can select later)
4. Click **Connect**

### Step 3: Create Query File

1. Right-click on `StC_SchoolLab` database in the sidebar
2. Select **New Query**
3. A new SQL file will open

### Step 4: Run Queries for Screenshots

#### Screenshot 1: Backup History

**Query:**
```sql
USE msdb;
GO

SELECT TOP 10
    database_name AS [Database],
    backup_start_date AS [Start Time],
    backup_finish_date AS [Finish Time],
    DATEDIFF(SECOND, backup_start_date, backup_finish_date) AS [Duration (sec)],
    CAST(backup_size / 1024.0 / 1024.0 AS DECIMAL(10,2)) AS [Size (MB)],
    CASE type
        WHEN 'D' THEN 'Full'
        WHEN 'I' THEN 'Differential'
        WHEN 'L' THEN 'Transaction Log'
        ELSE 'Other'
    END AS [Backup Type]
FROM msdb.dbo.backupset
WHERE database_name = 'StC_SchoolLab'
ORDER BY backup_start_date DESC;
```

**How to Execute:**
1. Paste query into the SQL file
2. Click **Run** button (▶️) or press `Cmd + Enter`
3. Results appear in the bottom panel
4. Capture screenshot with `Cmd + Shift + 4`

#### Screenshot 2: Student Profile Report

**Query:**
```sql
USE StC_SchoolLab;
GO

EXEC sp_GetStudentProfile @StudentId = 1;
```

**How to Execute:**
1. Paste query into the SQL file
2. Click **Run** button (▶️)
3. Results show 3 tabs (one for each result set)
4. Capture each tab separately or switch between them
5. Save as `02_student_profile_set1.jpeg`, `02_student_profile_set2.jpeg`, `02_student_profile_set3.jpeg`

#### Screenshot 3: Daily Attendance Report

**Query:**
```sql
USE StC_SchoolLab;
GO

-- Get most recent attendance date
DECLARE @AttendanceDate DATE = (SELECT TOP 1 attendance_date FROM Attendance ORDER BY attendance_date DESC);

EXEC sp_AttendanceByDate @Date = @AttendanceDate;
```

**Alternative (Hardcoded Date):**
```sql
USE StC_SchoolLab;
GO

EXEC sp_AttendanceByDate @Date = '2025-11-25';
```

**How to Execute:**
1. Paste query into the SQL file
2. Click **Run** button (▶️)
3. Results show 3 tabs (one for each result set)
4. Capture each tab or all together

#### Screenshot 4: Enrollment Summary Report

**Query:**
```sql
USE StC_SchoolLab;
GO

EXEC sp_EnrollmentSummaryByYear @YearLevel = 8;
```

**How to Execute:**
1. Paste query into the SQL file
2. Click **Run** button (▶️)
3. Results show 2 tabs (one for each result set)
4. Capture both tabs

#### Screenshot 5: Data Validation - Row Count Reconciliation

**Query:**
```sql
USE StC_SchoolLab;
GO

SELECT 'Students' AS [Table Name], COUNT(*) AS [Row Count] FROM Students
UNION ALL SELECT 'Staff', COUNT(*) FROM Staff
UNION ALL SELECT 'Classes', COUNT(*) FROM Classes
UNION ALL SELECT 'Enrollments', COUNT(*) FROM Enrollments
UNION ALL SELECT 'Attendance', COUNT(*) FROM Attendance
ORDER BY [Table Name];
```

**How to Execute:**
1. Paste query into the SQL file
2. Click **Run** button (▶️)
3. Results show single table with row counts
4. Capture screenshot

#### Screenshot 6: Data Validation - Referential Integrity Check

**Query:**
```sql
USE StC_SchoolLab;
GO

SELECT 'Orphaned Enrollments' AS [Issue], COUNT(*) AS [Count]
FROM Enrollments e
LEFT JOIN Students s ON e.student_id = s.student_id
WHERE s.student_id IS NULL

UNION ALL

SELECT 'Orphaned Attendance (Student)', COUNT(*)
FROM Attendance a
LEFT JOIN Students s ON a.student_id = s.student_id
WHERE s.student_id IS NULL

UNION ALL

SELECT 'Orphaned Attendance (Class)', COUNT(*)
FROM Attendance a
LEFT JOIN Classes c ON a.class_id = c.class_id
WHERE c.class_id IS NULL

UNION ALL

SELECT 'Enrollments without Classes', COUNT(*)
FROM Enrollments e
LEFT JOIN Classes c ON e.class_id = c.class_id
WHERE c.class_id IS NULL;
```

**How to Execute:**
1. Paste query into the SQL file
2. Click **Run** button (▶️)
3. Results should show all counts as 0
4. Capture screenshot

---

## VS Code Database Client Tips

### Viewing Results
- Results appear in the **Output** panel at the bottom
- Multiple result sets show as separate tabs
- Click tabs to switch between result sets
- Right-click results → **Export** to save as CSV/JSON

### Formatting Results
- Right-click in results panel → **Format Document** for better readability
- Adjust column widths by dragging column headers
- Sort results by clicking column headers

### Saving Queries
1. Save query file as `screenshot_queries.sql` in your project
2. Reuse queries for future screenshots
3. Add comments to organize queries

### Keyboard Shortcuts
- `Cmd + Enter`: Run query
- `Cmd + Shift + E`: Execute selected text only
- `Cmd + K, Cmd + C`: Comment selected lines
- `Cmd + K, Cmd + U`: Uncomment selected lines

---

## Screenshot Organization

### Recommended File Naming
```
01_backup_history.jpeg
02_student_profile_overview.jpeg
02_student_profile_enrollments.jpeg
02_student_profile_attendance.jpeg
03_daily_attendance_records.jpeg
03_daily_attendance_summary.jpeg
03_daily_attendance_absent.jpeg
04_enrollment_summary_classes.jpeg
04_enrollment_summary_year.jpeg
05_row_count_validation.jpeg
06_referential_integrity.jpeg
```

### Screenshot Folder Structure
```
docs/Assessment3/screenshots/
├── 01_backup_history.jpeg
├── 02_student_profile_overview.jpeg
├── 02_student_profile_enrollments.jpeg
├── 02_student_profile_attendance.jpeg
├── 03_daily_attendance_records.jpeg
├── 03_daily_attendance_summary.jpeg
├── 03_daily_attendance_absent.jpeg
├── 04_enrollment_summary_classes.jpeg
├── 04_enrollment_summary_year.jpeg
├── 05_row_count_validation.jpeg
└── 06_referential_integrity.jpeg
```

---

## Troubleshooting

### Issue: sqlcmd not found
**Solution:**
```bash
# Install sqlcmd via Homebrew
brew install sqlcmd

# Or use full path
/opt/homebrew/bin/sqlcmd --version
```

### Issue: Connection refused
**Solution:**
```bash
# Check if SQL Server is running
docker ps  # If using Docker

# Test connection
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q "SELECT @@VERSION;"
```

### Issue: Database Client extension not connecting
**Solution:**
1. Verify SQL Server is running
2. Check firewall settings (allow port 1433)
3. Try connection string: `localhost,1433`
4. Enable "Trust Server Certificate" in connection settings

### Issue: Results truncated in Terminal
**Solution:**
```bash
# Increase line width
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -d StC_SchoolLab -w 1000 -Q "YOUR_QUERY"

# Or export to file
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -d StC_SchoolLab -Q "YOUR_QUERY" -o output.txt
```

---

## Quick Reference: All Terminal Commands

Create a shell script for easy execution:

```bash
#!/bin/bash
# screenshot_queries.sh

# Configuration
SERVER="localhost"
USER="sa"
PASSWORD="StC_SchoolLab2025!"
DATABASE="StC_SchoolLab"
SQLCMD="/opt/homebrew/bin/sqlcmd"

echo "=== Screenshot 1: Backup History ==="
$SQLCMD -S $SERVER -U $USER -P $PASSWORD -C -d msdb -W -s "|" -Q "
SELECT TOP 10 database_name, backup_start_date, backup_finish_date, 
DATEDIFF(SECOND, backup_start_date, backup_finish_date) AS duration_sec,
CAST(backup_size / 1024.0 / 1024.0 AS DECIMAL(10,2)) AS size_mb,
CASE type WHEN 'D' THEN 'Full' WHEN 'I' THEN 'Differential' ELSE 'Other' END AS backup_type
FROM msdb.dbo.backupset WHERE database_name = 'StC_SchoolLab' ORDER BY backup_start_date DESC;
"

echo -e "\n=== Screenshot 2: Student Profile ==="
$SQLCMD -S $SERVER -U $USER -P $PASSWORD -C -d $DATABASE -W -s "|" -Q "EXEC sp_GetStudentProfile @StudentId = 1;"

echo -e "\n=== Screenshot 3: Daily Attendance ==="
$SQLCMD -S $SERVER -U $USER -P $PASSWORD -C -d $DATABASE -W -s "|" -Q "EXEC sp_AttendanceByDate @Date = '2025-01-15';"

echo -e "\n=== Screenshot 4: Enrollment Summary ==="
$SQLCMD -S $SERVER -U $USER -P $PASSWORD -C -d $DATABASE -W -s "|" -Q "EXEC sp_EnrollmentSummaryByYear @YearLevel = 8;"

echo -e "\n=== Screenshot 5: Row Count Validation ==="
$SQLCMD -S $SERVER -U $USER -P $PASSWORD -C -d $DATABASE -W -s "|" -Q "
SELECT 'Students' AS [Table], COUNT(*) AS [Count] FROM Students
UNION ALL SELECT 'Staff', COUNT(*) FROM Staff
UNION ALL SELECT 'Classes', COUNT(*) FROM Classes
UNION ALL SELECT 'Enrollments', COUNT(*) FROM Enrollments
UNION ALL SELECT 'Attendance', COUNT(*) FROM Attendance;
"

echo -e "\n=== Screenshot 6: Referential Integrity ==="
$SQLCMD -S $SERVER -U $USER -P $PASSWORD -C -d $DATABASE -W -s "|" -Q "
SELECT 'Orphaned Enrollments' AS [Issue], COUNT(*) AS [Count]
FROM Enrollments e LEFT JOIN Students s ON e.student_id = s.student_id WHERE s.student_id IS NULL
UNION ALL
SELECT 'Orphaned Attendance', COUNT(*) FROM Attendance a LEFT JOIN Students s ON a.student_id = s.student_id WHERE s.student_id IS NULL;
"
```

**Usage:**
```bash
chmod +x screenshot_queries.sh
./screenshot_queries.sh > screenshot_output.txt
```

---

**Last Updated:** December 29, 2025  
**Version:** 1.0 (macOS Compatible)
