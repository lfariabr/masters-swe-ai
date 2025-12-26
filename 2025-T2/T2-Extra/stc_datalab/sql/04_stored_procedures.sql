-- Stored Procedures for StC School Data Lab
-- Level 2 Task 2.3: Operational procedures addressing specific school needs
-- These procedures encapsulate business logic and provide consistent data access patterns

USE StC_SchoolLab;
GO

/* =====================================================================
   Procedure 1: sp_GetStudentProfile
   Purpose: Detailed student lookup for staff access
   Use case: Student information retrieval, parent-teacher meetings, counseling
   Parameters: @StudentId INT
   ===================================================================== */

CREATE OR ALTER PROCEDURE sp_GetStudentProfile
    @StudentId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Validate input
    IF @StudentId IS NULL OR @StudentId <= 0
    BEGIN
        RAISERROR('Invalid StudentId. Must be a positive integer.', 16, 1);
        RETURN;
    END
    
    -- Check if student exists
    IF NOT EXISTS (SELECT 1 FROM Students WHERE student_id = @StudentId)
    BEGIN
        RAISERROR('Student not found with StudentId: %d', 16, 1, @StudentId);
        RETURN;
    END
    
    -- Return comprehensive student profile
    SELECT 
        student_id,
        student_number,
        first_name,
        last_name,
        full_name,
        date_of_birth,
        age,
        address,
        phone,
        email,
        emergency_contact,
        emergency_phone,
        enrollment_year,
        years_enrolled,
        has_medical_info,
        total_enrollments,
        active_enrollments,
        completed_enrollments,
        withdrawn_enrollments,
        total_attendance_records,
        days_present,
        days_absent,
        days_late,
        days_excused,
        attendance_rate_percent,
        created_date,
        updated_date
    FROM vw_StudentProfile
    WHERE student_id = @StudentId;
    
    -- Return current enrollments with class details
    SELECT 
        e.enrollment_id,
        c.class_name,
        sub.subject_name,
        sub.subject_code,
        c.year_level,
        c.semester,
        CONCAT(st.first_name, ' ', st.last_name) AS teacher_name,
        e.enrollment_date,
        e.status AS enrollment_status,
        e.grade,
        c.room,
        c.schedule
    FROM Enrollments e
    INNER JOIN Classes c ON e.class_id = c.class_id
    INNER JOIN Subjects sub ON c.subject_id = sub.subject_id
    INNER JOIN Staff st ON c.staff_id = st.staff_id
    WHERE e.student_id = @StudentId
    ORDER BY e.status DESC, c.class_name;
    
    -- Return recent attendance summary (last 30 days)
    SELECT 
        a.attendance_date,
        c.class_name,
        sub.subject_name,
        a.status,
        a.notes,
        CONCAT(st.first_name, ' ', st.last_name) AS marked_by
    FROM Attendance a
    INNER JOIN Classes c ON a.class_id = c.class_id
    INNER JOIN Subjects sub ON c.subject_id = sub.subject_id
    LEFT JOIN Staff st ON a.marked_by = st.staff_id
    WHERE a.student_id = @StudentId
      AND a.attendance_date >= DATEADD(DAY, -30, GETDATE())
    ORDER BY a.attendance_date DESC, c.class_name;
END;
GO

/* =====================================================================
   Procedure 2: sp_EnrollmentSummaryByYear
   Purpose: Class distribution reports by year level
   Use case: Enrollment planning, capacity management, resource allocation
   Parameters: @YearLevel INT
   ===================================================================== */

CREATE OR ALTER PROCEDURE sp_EnrollmentSummaryByYear
    @YearLevel INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Validate input
    IF @YearLevel IS NULL OR @YearLevel < 7 OR @YearLevel > 12
    BEGIN
        RAISERROR('Invalid YearLevel. Must be between 7 and 12 (secondary school).', 16, 1);
        RETURN;
    END
    
    -- Return enrollment summary by class for the specified year level
    SELECT 
        c.class_id,
        c.class_name,
        sub.subject_name,
        sub.subject_code,
        c.year_level,
        c.semester,
        CONCAT(st.first_name, ' ', st.last_name) AS teacher_name,
        st.department,
        c.max_students,
        c.room,
        -- Enrollment counts
        COUNT(DISTINCT CASE WHEN e.status = 'Active' THEN e.student_id END) AS active_students,
        COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.student_id END) AS completed_students,
        COUNT(DISTINCT CASE WHEN e.status = 'Withdrawn' THEN e.student_id END) AS withdrawn_students,
        COUNT(DISTINCT e.student_id) AS total_students,
        c.max_students - COUNT(DISTINCT CASE WHEN e.status = 'Active' THEN e.student_id END) AS available_seats,
        -- Capacity utilization
        CAST(ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.status = 'Active' THEN e.student_id END) / NULLIF(c.max_students, 0), 2) AS DECIMAL(5,2)) AS capacity_utilization_percent,
        -- Status indicator
        CASE 
            WHEN COUNT(DISTINCT CASE WHEN e.status = 'Active' THEN e.student_id END) >= c.max_students THEN 'Full'
            WHEN COUNT(DISTINCT CASE WHEN e.status = 'Active' THEN e.student_id END) >= c.max_students * 0.9 THEN 'Near Capacity'
            WHEN COUNT(DISTINCT CASE WHEN e.status = 'Active' THEN e.student_id END) < c.max_students * 0.5 THEN 'Under-enrolled'
            ELSE 'Available'
        END AS enrollment_status
    FROM Classes c
    INNER JOIN Subjects sub ON c.subject_id = sub.subject_id
    INNER JOIN Staff st ON c.staff_id = st.staff_id
    LEFT JOIN Enrollments e ON c.class_id = e.class_id
    WHERE c.year_level = @YearLevel
      AND c.is_active = 1
    GROUP BY 
        c.class_id, c.class_name, sub.subject_name, sub.subject_code,
        c.year_level, c.semester, st.first_name, st.last_name, st.department,
        c.max_students, c.room
    ORDER BY c.semester, sub.subject_name, c.class_name;
    
    -- Return year-level summary statistics
    SELECT 
        @YearLevel AS year_level,
        COUNT(DISTINCT c.class_id) AS total_classes,
        COUNT(DISTINCT c.subject_id) AS unique_subjects,
        COUNT(DISTINCT c.staff_id) AS teachers_assigned,
        SUM(c.max_students) AS total_capacity,
        COUNT(DISTINCT CASE WHEN e.status = 'Active' THEN e.student_id END) AS total_active_students,
        SUM(c.max_students) - COUNT(DISTINCT CASE WHEN e.status = 'Active' THEN e.student_id END) AS total_available_seats,
        CAST(ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.status = 'Active' THEN e.student_id END) / NULLIF(SUM(c.max_students), 0), 2) AS DECIMAL(5,2)) AS overall_utilization_percent
    FROM Classes c
    LEFT JOIN Enrollments e ON c.class_id = e.class_id
    WHERE c.year_level = @YearLevel
      AND c.is_active = 1;
END;
GO

/* =====================================================================
   Procedure 3: sp_AttendanceByDate
   Purpose: Daily attendance tracking for operational reporting
   Use case: Daily roll call verification, absence follow-up, compliance reporting
   Parameters: @Date DATE
   ===================================================================== */

CREATE OR ALTER PROCEDURE sp_AttendanceByDate
    @Date DATE
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Validate input
    IF @Date IS NULL
    BEGIN
        RAISERROR('Date parameter is required.', 16, 1);
        RETURN;
    END
    
    -- Return attendance records for the specified date
    SELECT 
        a.attendance_id,
        a.attendance_date,
        DATENAME(WEEKDAY, a.attendance_date) AS day_of_week,
        -- Student information
        s.student_id,
        s.student_number,
        CONCAT(s.first_name, ' ', s.last_name) AS student_name,
        s.enrollment_year,
        -- Class information
        c.class_id,
        c.class_name,
        sub.subject_name,
        c.year_level,
        c.semester,
        c.room,
        CONCAT(teacher.first_name, ' ', teacher.last_name) AS teacher_name,
        -- Attendance details
        a.status,
        a.notes,
        CONCAT(marker.first_name, ' ', marker.last_name) AS marked_by,
        a.marked_date
    FROM Attendance a
    INNER JOIN Students s ON a.student_id = s.student_id
    INNER JOIN Classes c ON a.class_id = c.class_id
    INNER JOIN Subjects sub ON c.subject_id = sub.subject_id
    INNER JOIN Staff teacher ON c.staff_id = teacher.staff_id
    LEFT JOIN Staff marker ON a.marked_by = marker.staff_id
    WHERE a.attendance_date = @Date
    ORDER BY c.class_name, s.last_name, s.first_name;
    
    -- Return daily summary statistics
    SELECT 
        @Date AS attendance_date,
        DATENAME(WEEKDAY, @Date) AS day_of_week,
        COUNT(DISTINCT a.student_id) AS total_students_marked,
        COUNT(DISTINCT a.class_id) AS classes_with_attendance,
        SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS total_present,
        SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) AS total_absent,
        SUM(CASE WHEN a.status = 'Late' THEN 1 ELSE 0 END) AS total_late,
        SUM(CASE WHEN a.status = 'Excused' THEN 1 ELSE 0 END) AS total_excused,
        CAST(ROUND(100.0 * SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS DECIMAL(5,2)) AS attendance_rate_percent,
        CAST(ROUND(100.0 * SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS DECIMAL(5,2)) AS absence_rate_percent
    FROM Attendance a
    WHERE a.attendance_date = @Date;
    
    -- Return students with concerning attendance patterns (absent or multiple absences)
    SELECT 
        s.student_id,
        s.student_number,
        CONCAT(s.first_name, ' ', s.last_name) AS student_name,
        s.phone,
        s.emergency_contact,
        s.emergency_phone,
        COUNT(CASE WHEN a.status = 'Absent' THEN 1 END) AS absent_count_today,
        STRING_AGG(c.class_name, ', ') AS absent_from_classes
    FROM Students s
    INNER JOIN Attendance a ON s.student_id = a.student_id
    INNER JOIN Classes c ON a.class_id = c.class_id
    WHERE a.attendance_date = @Date
      AND a.status = 'Absent'
    GROUP BY s.student_id, s.student_number, s.first_name, s.last_name, s.phone, s.emergency_contact, s.emergency_phone
    ORDER BY absent_count_today DESC, s.last_name;
END;
GO

/* =====================================================================
   Procedure 4: sp_GetTableDataExport
   Purpose: Export filtered table/view data for system integration (SEQTA, Power BI)
   Use case: Data export for external systems, reporting tools, backups
   Parameters: @TableName NVARCHAR(100), @TopN INT (optional)
   Note: Returns standard SQL result sets; client tools handle CSV serialization
   ===================================================================== */

CREATE OR ALTER PROCEDURE sp_GetTableDataExport
    @TableName NVARCHAR(100),
    @TopN INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Validate input
    IF @TableName IS NULL OR LTRIM(RTRIM(@TableName)) = ''
    BEGIN
        RAISERROR('TableName parameter is required.', 16, 1);
        RETURN;
    END
    
    -- Normalize table name
    SET @TableName = UPPER(LTRIM(RTRIM(@TableName)));
    
    -- Dynamic SQL for CSV export based on table/view name
    DECLARE @SQL NVARCHAR(MAX);
    DECLARE @TopClause NVARCHAR(20) = '';
    
    IF @TopN IS NOT NULL AND @TopN > 0
        SET @TopClause = 'TOP ' + CAST(@TopN AS NVARCHAR(10)) + ' ';
    
    -- Route to appropriate table/view
    IF @TableName = 'STUDENTS'
    BEGIN
        SET @SQL = '
        SELECT ' + @TopClause + '
            student_id,
            student_number,
            first_name,
            last_name,
            date_of_birth,
            address,
            phone,
            email,
            emergency_contact,
            emergency_phone,
            enrollment_year,
            created_date
        FROM Students
        ORDER BY student_id;';
    END
    ELSE IF @TableName = 'STAFF'
    BEGIN
        SET @SQL = '
        SELECT ' + @TopClause + '
            staff_id,
            first_name,
            last_name,
            role,
            email,
            phone,
            department,
            hire_date,
            is_active
        FROM Staff
        ORDER BY staff_id;';
    END
    ELSE IF @TableName = 'CLASSES'
    BEGIN
        SET @SQL = '
        SELECT ' + @TopClause + '
            c.class_id,
            c.class_name,
            s.subject_name,
            s.subject_code,
            c.year_level,
            c.semester,
            CONCAT(st.first_name, '' '', st.last_name) AS teacher_name,
            c.max_students,
            c.room,
            c.schedule,
            c.is_active
        FROM Classes c
        INNER JOIN Subjects s ON c.subject_id = s.subject_id
        INNER JOIN Staff st ON c.staff_id = st.staff_id
        ORDER BY c.class_id;';
    END
    ELSE IF @TableName = 'ENROLLMENTS'
    BEGIN
        SET @SQL = '
        SELECT ' + @TopClause + '
            e.enrollment_id,
            e.student_id,
            s.student_number,
            CONCAT(s.first_name, '' '', s.last_name) AS student_name,
            e.class_id,
            c.class_name,
            e.enrollment_date,
            e.status,
            e.grade,
            e.withdrawal_date
        FROM Enrollments e
        INNER JOIN Students s ON e.student_id = s.student_id
        INNER JOIN Classes c ON e.class_id = c.class_id
        ORDER BY e.enrollment_id;';
    END
    ELSE IF @TableName = 'ATTENDANCE'
    BEGIN
        SET @SQL = '
        SELECT ' + @TopClause + '
            a.attendance_id,
            a.student_id,
            s.student_number,
            CONCAT(s.first_name, '' '', s.last_name) AS student_name,
            a.class_id,
            c.class_name,
            a.attendance_date,
            a.status,
            a.notes,
            a.marked_date
        FROM Attendance a
        INNER JOIN Students s ON a.student_id = s.student_id
        INNER JOIN Classes c ON a.class_id = c.class_id
        ORDER BY a.attendance_date DESC, a.attendance_id;';
    END
    ELSE IF @TableName = 'VW_STUDENTPROFILE'
    BEGIN
        SET @SQL = '
        SELECT ' + @TopClause + '
            student_id,
            student_number,
            full_name,
            age,
            phone,
            email,
            enrollment_year,
            total_enrollments,
            active_enrollments,
            attendance_rate_percent
        FROM vw_StudentProfile
        ORDER BY student_id;';
    END
    ELSE IF @TableName = 'VW_ACADEMICPERFORMANCE'
    BEGIN
        SET @SQL = '
        SELECT ' + @TopClause + '
            student_id,
            student_number,
            student_name,
            class_name,
            subject_name,
            year_level,
            semester,
            final_grade,
            grade_points,
            effort_rating,
            academic_standing,
            attendance_rate_percent
        FROM vw_AcademicPerformance
        ORDER BY student_id, class_id;';
    END
    ELSE
    BEGIN
        RAISERROR('Invalid TableName. Supported: STUDENTS, STAFF, CLASSES, ENROLLMENTS, ATTENDANCE, VW_STUDENTPROFILE, VW_ACADEMICPERFORMANCE', 16, 1);
        RETURN;
    END
    
    -- Execute dynamic SQL and capture row count
    DECLARE @RowsExported INT;
    EXEC sp_executesql @SQL;
    SET @RowsExported = @@ROWCOUNT;
    
    -- Return export metadata
    SELECT 
        @TableName AS exported_table,
        GETDATE() AS export_timestamp,
        @RowsExported AS rows_exported;
END;
GO

-- Verification queries (commented out for production)
-- EXEC sp_GetStudentProfile @StudentId = 1;
-- EXEC sp_EnrollmentSummaryByYear @YearLevel = 8;
-- EXEC sp_AttendanceByDate @Date = '2025-01-15';
-- EXEC sp_GetTableDataExport @TableName = 'STUDENTS', @TopN = 10;

PRINT 'All 4 stored procedures created successfully.';
PRINT 'Procedures: sp_GetStudentProfile, sp_EnrollmentSummaryByYear, sp_AttendanceByDate, sp_GetTableDataExport';
