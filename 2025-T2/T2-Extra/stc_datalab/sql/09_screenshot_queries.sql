-- ============================================================================
-- StC SchoolLab Database - Screenshot Capture Queries
-- ============================================================================
-- Purpose: SQL queries for generating demonstration screenshots
-- Usage: Execute in SSMS, capture results for interview presentation
-- Last Updated: December 29, 2025
-- ============================================================================

USE StC_SchoolLab;
GO

-- ============================================================================
-- SCREENSHOT 1: Backup History
-- ============================================================================
-- Shows: Backup frequency, duration, size, type
-- Demonstrates: Operational maturity, backup procedures
-- ============================================================================

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
    END AS [Backup Type],
    physical_device_name AS [Backup File]
FROM msdb.dbo.backupset bs
INNER JOIN msdb.dbo.backupmediafamily bmf ON bs.media_set_id = bmf.media_set_id
WHERE database_name = 'StC_SchoolLab'
ORDER BY backup_start_date DESC;

-- Expected Output:
-- - Daily full backups (11 PM)
-- - Differential backups (every 6 hours)
-- - Backup duration <1 second
-- - Backup size 6-8 MB typical

-- ============================================================================
-- SCREENSHOT 2: Student Profile Report (3 Result Sets)
-- ============================================================================
-- Shows: Complete student information for parent-teacher conferences
-- Demonstrates: Stored procedure functionality, data integration
-- ============================================================================

EXEC sp_GetStudentProfile @StudentId = 1;

-- Expected Output:
-- Result Set 1: Student Overview
--   - Student number, name, year level, contact info
--   - Total enrollments, attendance rate
--
-- Result Set 2: Current Enrollments
--   - Class name, subject, teacher, grade, status
--   - Shows all classes student is enrolled in
--
-- Result Set 3: Recent Attendance
--   - Last 30 days of attendance records
--   - Date, class, status (Present/Absent/Late/Excused)

-- ============================================================================
-- SCREENSHOT 3: Daily Attendance Report (3 Result Sets)
-- ============================================================================
-- Shows: Roll call verification and absence follow-up
-- Demonstrates: Child safety compliance, operational reporting
-- ============================================================================

-- Use a date that has attendance data
DECLARE @AttendanceDate DATE = (SELECT TOP 1 attendance_date FROM Attendance ORDER BY attendance_date DESC);

EXEC sp_AttendanceByDate @Date = @AttendanceDate;

-- Expected Output:
-- Result Set 1: All Attendance Records
--   - Student name, class, teacher, status
--   - Complete roll call for the day
--
-- Result Set 2: Daily Summary
--   - Total marked, present/absent/late/excused counts
--   - Attendance rate percentage
--
-- Result Set 3: Absent Students (Critical)
--   - Student names, contact information
--   - Action list for office staff follow-up

-- ============================================================================
-- SCREENSHOT 4: Enrollment Summary Report (2 Result Sets)
-- ============================================================================
-- Shows: Class capacity planning and resource allocation
-- Demonstrates: Leadership decision support, data-driven planning
-- ============================================================================

EXEC sp_EnrollmentSummaryByYear @YearLevel = 8;

-- Expected Output:
-- Result Set 1: Class-Level Details
--   - Each class with enrollment, capacity, utilization %
--   - Status indicators (Full, Near Capacity, Available, Under-enrolled)
--
-- Result Set 2: Year-Level Summary
--   - Total classes, subjects, teachers
--   - Overall capacity utilization percentage

-- ============================================================================
-- SCREENSHOT 5: Data Validation - Row Count Reconciliation
-- ============================================================================
-- Shows: Data quality checks, referential integrity
-- Demonstrates: Systematic validation, operational rigor
-- ============================================================================

SELECT 'Students' AS [Table Name], COUNT(*) AS [Row Count] FROM Students
UNION ALL SELECT 'Staff', COUNT(*) FROM Staff
UNION ALL SELECT 'Classes', COUNT(*) FROM Classes
UNION ALL SELECT 'Enrollments', COUNT(*) FROM Enrollments
UNION ALL SELECT 'Attendance', COUNT(*) FROM Attendance
ORDER BY [Table Name];

-- Expected Output:
-- Students: 100 records
-- Staff: 20 records
-- Classes: 30 records
-- Enrollments: 500 records (5 classes per student average)
-- Attendance: 2,500 records (50 days × 50 students average)

-- ============================================================================
-- SCREENSHOT 6: Data Validation - Referential Integrity Check
-- ============================================================================
-- Shows: No orphaned records, foreign key integrity
-- Demonstrates: Data quality assurance
-- ============================================================================

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

-- Expected Output:
-- All counts should be 0 (no orphaned records)
-- Demonstrates referential integrity is maintained

-- ============================================================================
-- SCREENSHOT 7: Data Validation - NULL Value Detection
-- ============================================================================
-- Shows: Critical fields are populated, data completeness
-- Demonstrates: Data quality monitoring
-- ============================================================================

SELECT 
    COUNT(*) AS [Total Students],
    SUM(CASE WHEN first_name IS NULL THEN 1 ELSE 0 END) AS [Missing First Name],
    SUM(CASE WHEN last_name IS NULL THEN 1 ELSE 0 END) AS [Missing Last Name],
    SUM(CASE WHEN student_number IS NULL THEN 1 ELSE 0 END) AS [Missing Student Number],
    SUM(CASE WHEN enrollment_year IS NULL THEN 1 ELSE 0 END) AS [Missing Enrollment Year],
    SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) AS [Missing Email]
FROM Students;

-- Expected Output:
-- Total Students: 200
-- All "Missing" columns should be 0
-- Critical fields must never be NULL
-- Note: Students table has enrollment_year, not year_level (year_level is in Classes table)

-- ============================================================================
-- SCREENSHOT 8: System Integration - SEQTA Import Monitoring
-- ============================================================================
-- Shows: Last import timestamp, data freshness
-- Demonstrates: Integration monitoring, data pipeline health
-- ============================================================================

SELECT 
    'Students' AS [Import Source],
    MAX(created_date) AS [Last Import],
    COUNT(*) AS [Total Records],
    DATEDIFF(HOUR, MAX(created_date), GETDATE()) AS [Hours Since Import]
FROM Students

UNION ALL

SELECT 
    'Staff',
    MAX(created_date),
    COUNT(*),
    DATEDIFF(HOUR, MAX(created_date), GETDATE())
FROM Staff

UNION ALL

SELECT 
    'Classes',
    MAX(created_date),
    COUNT(*),
    DATEDIFF(HOUR, MAX(created_date), GETDATE())
FROM Classes;

-- Expected Output:
-- Last Import should be within 24 hours (daily 6 AM schedule)
-- If Hours Since Import > 24, investigate import failure

-- ============================================================================
-- SCREENSHOT 9: Database Health - Space Usage
-- ============================================================================
-- Shows: Database size, growth trends
-- Demonstrates: Capacity planning, resource monitoring
-- ============================================================================

EXEC sp_spaceused;

-- Expected Output:
-- Database size: 10-20 MB typical for this dataset
-- Unallocated space: Shows room for growth

-- ============================================================================
-- SCREENSHOT 10: Performance Monitoring - View Execution
-- ============================================================================
-- Shows: Reporting views are accessible and performant
-- Demonstrates: System health, query optimization
-- ============================================================================

-- Enable execution time statistics
SET STATISTICS TIME ON;
SET STATISTICS IO ON;

-- Test view performance
SELECT TOP 10 * FROM vw_StudentProfile;

SET STATISTICS TIME OFF;
SET STATISTICS IO OFF;

-- Expected Output:
-- Execution time: <1 second
-- Logical reads: Minimal (optimized queries)
-- Shows view is performant and accessible

-- ============================================================================
-- SCREENSHOT 11: Security - User Permissions Audit
-- ============================================================================
-- Shows: Least-privilege access model, role-based security
-- Demonstrates: Child data protection, compliance
-- ============================================================================

SELECT 
    dp.name AS [User/Role],
    dp.type_desc AS [Type],
    p.permission_name AS [Permission],
    p.state_desc AS [State],
    OBJECT_NAME(p.major_id) AS [Object]
FROM sys.database_permissions p
INNER JOIN sys.database_principals dp ON p.grantee_principal_id = dp.principal_id
WHERE dp.type IN ('S', 'U', 'R') -- SQL users, Windows users, Roles
ORDER BY dp.name, p.permission_name;

-- Expected Output:
-- Shows granular permissions by user/role
-- Demonstrates least-privilege access model

-- ============================================================================
-- SCREENSHOT 12: Backup Verification
-- ============================================================================
-- Shows: Backup integrity validation
-- Demonstrates: Disaster recovery readiness
-- ============================================================================

-- Get most recent backup file
DECLARE @BackupFile NVARCHAR(500);

SELECT TOP 1 @BackupFile = physical_device_name
FROM msdb.dbo.backupset bs
INNER JOIN msdb.dbo.backupmediafamily bmf ON bs.media_set_id = bmf.media_set_id
WHERE database_name = 'StC_SchoolLab'
ORDER BY backup_start_date DESC;

-- Verify backup integrity
RESTORE VERIFYONLY 
FROM DISK = @BackupFile;

-- Expected Output:
-- "The backup set on file 1 is valid."
-- Demonstrates backup can be restored if needed

-- ============================================================================
-- BONUS SCREENSHOT: Data Export Functionality
-- ============================================================================
-- Shows: SEQTA integration, Power BI data feed
-- Demonstrates: System integration capabilities
-- ============================================================================

EXEC sp_GetTableDataExport @TableName = 'STUDENTS', @TopN = 10;

-- Expected Output:
-- Result Set 1: Top 10 students with all fields
-- Result Set 2: Export metadata (table name, timestamp, row count)

-- ============================================================================
-- SCREENSHOT CAPTURE TIPS
-- ============================================================================
-- 1. Use SSMS "Results to Grid" mode for clean formatting
-- 2. Adjust column widths for readability before capturing
-- 3. Include query text in screenshot (shows what was executed)
-- 4. Capture full result sets (scroll if needed)
-- 5. Use consistent SSMS theme (light or dark) across all screenshots
-- 6. Save as PNG or JPG with high resolution (1920x1080 minimum)
-- 7. Annotate screenshots if needed (highlight key metrics)
-- 8. Name files descriptively: "01_backup_history.png", "02_student_profile.png"
-- ============================================================================

-- ============================================================================
-- PRESENTATION ORDER (RECOMMENDED)
-- ============================================================================
-- 1. Student Profile Report (shows core functionality)
-- 2. Daily Attendance Report (shows child safety compliance)
-- 3. Enrollment Summary Report (shows leadership decision support)
-- 4. Backup History (shows operational maturity)
-- 5. Data Validation - Row Counts (shows data quality)
-- 6. Data Validation - Referential Integrity (shows technical rigor)
-- ============================================================================
