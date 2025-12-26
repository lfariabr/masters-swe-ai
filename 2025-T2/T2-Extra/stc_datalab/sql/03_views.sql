-- Reporting Views for StC School Data Lab
-- Level 2 Task 2.2: Power BI-style reporting views for staff access
-- These views abstract complex joins and provide clean interfaces for reporting tools

USE StC_SchoolLab;
GO

/* =====================================================================
   View 1: vw_StudentProfile
   Purpose: Comprehensive student data for staff access
   Use case: Student lookup, parent communication, enrollment verification
   ===================================================================== */

CREATE OR ALTER VIEW vw_StudentProfile AS
WITH EnrollmentSummary AS (
    SELECT 
        student_id,
        COUNT(*) AS total_enrollments,
        SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) AS active_enrollments,
        SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed_enrollments,
        SUM(CASE WHEN status = 'Withdrawn' THEN 1 ELSE 0 END) AS withdrawn_enrollments
    FROM Enrollments
    GROUP BY student_id
),
AttendanceSummary AS (
    SELECT 
        student_id,
        COUNT(*) AS total_attendance_records,
        SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS days_present,
        SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) AS days_absent,
        SUM(CASE WHEN status = 'Late' THEN 1 ELSE 0 END) AS days_late,
        SUM(CASE WHEN status = 'Excused' THEN 1 ELSE 0 END) AS days_excused
    FROM Attendance
    GROUP BY student_id
)
SELECT 
    s.student_id,
    s.student_number,
    s.first_name,
    s.last_name,
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    s.date_of_birth,
    DATEDIFF(YEAR, s.date_of_birth, GETDATE()) - 
        CASE WHEN DATEADD(YEAR, DATEDIFF(YEAR, s.date_of_birth, GETDATE()), s.date_of_birth) > GETDATE() 
        THEN 1 ELSE 0 END AS age,
    s.address,
    s.phone,
    s.email,
    s.emergency_contact,
    s.emergency_phone,
    s.enrollment_year,
    YEAR(GETDATE()) - s.enrollment_year AS years_enrolled,
    -- Privacy-sensitive field (masked for general reports)
    CASE 
        WHEN s.medical_info IS NOT NULL THEN 'Yes - See Registrar'
        ELSE 'No'
    END AS has_medical_info,
    -- Enrollment summary
    ISNULL(e.total_enrollments, 0) AS total_enrollments,
    ISNULL(e.active_enrollments, 0) AS active_enrollments,
    ISNULL(e.completed_enrollments, 0) AS completed_enrollments,
    ISNULL(e.withdrawn_enrollments, 0) AS withdrawn_enrollments,
    -- Attendance summary
    ISNULL(a.total_attendance_records, 0) AS total_attendance_records,
    ISNULL(a.days_present, 0) AS days_present,
    ISNULL(a.days_absent, 0) AS days_absent,
    ISNULL(a.days_late, 0) AS days_late,
    ISNULL(a.days_excused, 0) AS days_excused,
    -- Attendance rate calculation
    CASE 
        WHEN a.total_attendance_records > 0 
        THEN CAST(ROUND(100.0 * a.days_present / a.total_attendance_records, 2) AS DECIMAL(5,2))
        ELSE NULL 
    END AS attendance_rate_percent,
    s.created_date,
    s.updated_date
FROM Students s
LEFT JOIN EnrollmentSummary e ON s.student_id = e.student_id
LEFT JOIN AttendanceSummary a ON s.student_id = a.student_id;
GO

/* =====================================================================
   View 2: vw_ClassRoll
   Purpose: Attendance tracking for teachers (daily class roll)
   Use case: Teachers marking attendance, viewing class lists
   ===================================================================== */

CREATE OR ALTER VIEW vw_ClassRoll AS
SELECT 
    c.class_id,
    c.class_name,
    sub.subject_name,
    sub.subject_code,
    c.year_level,
    c.semester,
    c.room,
    c.schedule,
    -- Teacher information
    CONCAT(st.first_name, ' ', st.last_name) AS teacher_name,
    st.email AS teacher_email,
    st.department AS teacher_department,
    -- Student information
    s.student_id,
    s.student_number,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    s.email AS student_email,
    -- Enrollment details
    e.enrollment_id,
    e.enrollment_date,
    e.status AS enrollment_status,
    e.grade AS current_grade,
    -- Class capacity metrics
    c.max_students,
    COUNT(e.enrollment_id) OVER (PARTITION BY c.class_id) AS current_enrollment_count,
    c.max_students - COUNT(e.enrollment_id) OVER (PARTITION BY c.class_id) AS available_seats,
    -- Student attendance summary for this class
    COUNT(a.attendance_id) AS total_attendance_records,
    SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS times_present,
    SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) AS times_absent,
    SUM(CASE WHEN a.status = 'Late' THEN 1 ELSE 0 END) AS times_late,
    -- Latest attendance status (optimized with OUTER APPLY)
    last_att.status AS last_attendance_status,
    last_att.attendance_date AS last_attendance_date
FROM Classes c
INNER JOIN Subjects sub ON c.subject_id = sub.subject_id
INNER JOIN Staff st ON c.staff_id = st.staff_id
LEFT JOIN Enrollments e ON c.class_id = e.class_id AND e.status IN ('Active', 'Completed')
LEFT JOIN Students s ON e.student_id = s.student_id
LEFT JOIN Attendance a ON s.student_id = a.student_id AND c.class_id = a.class_id
OUTER APPLY (
    SELECT TOP 1 a2.status, a2.attendance_date
    FROM Attendance a2
    WHERE a2.student_id = s.student_id 
      AND a2.class_id = c.class_id
    ORDER BY a2.attendance_date DESC
) last_att
WHERE c.is_active = 1
GROUP BY 
    c.class_id, c.class_name, sub.subject_name, sub.subject_code,
    c.year_level, c.semester, c.room, c.schedule, c.max_students,
    st.first_name, st.last_name, st.email, st.department,
    s.student_id, s.student_number, s.first_name, s.last_name, s.email,
    e.enrollment_id, e.enrollment_date, e.status, e.grade,
    last_att.status, last_att.attendance_date;
GO

/* =====================================================================
   View 3: vw_AttendanceSummary
   Purpose: Aggregated attendance metrics for leadership reporting
   Use case: Principal/leadership dashboards, trend analysis
   ===================================================================== */

CREATE OR ALTER VIEW vw_AttendanceSummary AS
SELECT 
    -- Date dimensions
    a.attendance_date,
    DATENAME(WEEKDAY, a.attendance_date) AS day_of_week,
    DATEPART(WEEK, a.attendance_date) AS week_number,
    DATEPART(MONTH, a.attendance_date) AS month_number,
    DATENAME(MONTH, a.attendance_date) AS month_name,
    DATEPART(YEAR, a.attendance_date) AS year,
    -- Class dimensions
    c.class_id,
    c.class_name,
    sub.subject_name,
    c.year_level,
    c.semester,
    CONCAT(st.first_name, ' ', st.last_name) AS teacher_name,
    -- Attendance metrics
    COUNT(DISTINCT a.student_id) AS total_students_marked,
    SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS count_present,
    SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) AS count_absent,
    SUM(CASE WHEN a.status = 'Late' THEN 1 ELSE 0 END) AS count_late,
    SUM(CASE WHEN a.status = 'Excused' THEN 1 ELSE 0 END) AS count_excused,
    -- Attendance rate (using DISTINCT counts to prevent inflation)
    CASE 
        WHEN COUNT(DISTINCT a.student_id) > 0 
        THEN CAST(ROUND(100.0 * COUNT(DISTINCT CASE WHEN a.status = 'Present' THEN a.student_id END) / COUNT(DISTINCT a.student_id), 2) AS DECIMAL(5,2))
        ELSE 0 
    END AS attendance_rate_percent,
    -- Absence rate (using DISTINCT counts to prevent inflation)
    CASE 
        WHEN COUNT(DISTINCT a.student_id) > 0 
        THEN CAST(ROUND(100.0 * COUNT(DISTINCT CASE WHEN a.status = 'Absent' THEN a.student_id END) / COUNT(DISTINCT a.student_id), 2) AS DECIMAL(5,2))
        ELSE 0 
    END AS absence_rate_percent,
    -- Marked by
    CONCAT(marker.first_name, ' ', marker.last_name) AS marked_by_name,
    MAX(a.marked_date) AS last_marked_timestamp
FROM Attendance a
INNER JOIN Classes c ON a.class_id = c.class_id
INNER JOIN Subjects sub ON c.subject_id = sub.subject_id
INNER JOIN Staff st ON c.staff_id = st.staff_id
LEFT JOIN Staff marker ON a.marked_by = marker.staff_id
GROUP BY 
    a.attendance_date, c.class_id, c.class_name, sub.subject_name,
    c.year_level, c.semester, st.first_name, st.last_name,
    marker.first_name, marker.last_name;
GO

/* =====================================================================
   View 4: vw_AcademicPerformance
   Purpose: Student academic performance with effort/grades calculations
   Use case: Report cards, academic intervention, parent-teacher conferences
   ===================================================================== */

CREATE OR ALTER VIEW vw_AcademicPerformance AS
SELECT 
    -- Student information
    s.student_id,
    s.student_number,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    s.enrollment_year,
    -- Class information
    c.class_id,
    c.class_name,
    sub.subject_name,
    sub.subject_code,
    c.year_level,
    c.semester,
    CONCAT(st.first_name, ' ', st.last_name) AS teacher_name,
    -- Enrollment details
    e.enrollment_date,
    e.status AS enrollment_status,
    e.grade AS final_grade,
    e.withdrawal_date,
    -- Grade point calculation (explicit mapping for all grade variants)
    CASE 
        WHEN e.grade IN ('A+', 'A') THEN 4.0
        WHEN e.grade = 'A-' THEN 3.7
        WHEN e.grade = 'B+' THEN 3.3
        WHEN e.grade = 'B' THEN 3.0
        WHEN e.grade = 'B-' THEN 2.7
        WHEN e.grade = 'C+' THEN 2.3
        WHEN e.grade = 'C' THEN 2.0
        WHEN e.grade = 'C-' THEN 1.7
        WHEN e.grade = 'D+' THEN 1.3
        WHEN e.grade = 'D' THEN 1.0
        WHEN e.grade = 'D-' THEN 0.7
        WHEN e.grade = 'F' THEN 0.0
        WHEN e.grade = 'INC' THEN NULL
        ELSE NULL
    END AS grade_points,
    -- Attendance-based effort indicator
    COUNT(a.attendance_id) AS total_classes,
    SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS classes_attended,
    SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) AS classes_absent,
    SUM(CASE WHEN a.status = 'Late' THEN 1 ELSE 0 END) AS classes_late,
    -- Attendance rate as effort proxy
    CASE 
        WHEN COUNT(a.attendance_id) > 0 
        THEN CAST(ROUND(100.0 * SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) / COUNT(a.attendance_id), 2) AS DECIMAL(5,2))
        ELSE NULL 
    END AS attendance_rate_percent,
    -- Effort rating based on attendance (StC-style: Outstanding, Good, Satisfactory, Needs Improvement)
    CASE 
        WHEN COUNT(a.attendance_id) = 0 THEN 'Not Assessed'
        WHEN CAST(100.0 * SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) / COUNT(a.attendance_id) AS DECIMAL(5,2)) >= 95 THEN 'Outstanding'
        WHEN CAST(100.0 * SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) / COUNT(a.attendance_id) AS DECIMAL(5,2)) >= 85 THEN 'Good'
        WHEN CAST(100.0 * SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) / COUNT(a.attendance_id) AS DECIMAL(5,2)) >= 70 THEN 'Satisfactory'
        ELSE 'Needs Improvement'
    END AS effort_rating,
    -- Academic standing indicator (covers all grade variants)
    CASE 
        WHEN e.status = 'Withdrawn' THEN 'Withdrawn'
        WHEN e.grade IS NULL THEN 'In Progress'
        WHEN e.grade = 'INC' THEN 'Incomplete'
        WHEN e.grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B-') THEN 'Good Standing'
        WHEN e.grade IN ('C+', 'C', 'C-', 'D+', 'D', 'D-') THEN 'At Risk'
        WHEN e.grade = 'F' THEN 'Failing'
        ELSE 'Unknown'
    END AS academic_standing,
    -- Subject credits
    sub.credits,
    -- Timestamps
    e.created_date AS enrollment_created,
    e.updated_date AS enrollment_updated
FROM Students s
INNER JOIN Enrollments e ON s.student_id = e.student_id
INNER JOIN Classes c ON e.class_id = c.class_id
INNER JOIN Subjects sub ON c.subject_id = sub.subject_id
INNER JOIN Staff st ON c.staff_id = st.staff_id
LEFT JOIN Attendance a ON s.student_id = a.student_id AND c.class_id = a.class_id
GROUP BY 
    s.student_id, s.student_number, s.first_name, s.last_name, s.enrollment_year,
    c.class_id, c.class_name, sub.subject_name, sub.subject_code, c.year_level, c.semester,
    st.first_name, st.last_name, e.enrollment_date, e.status, e.grade, e.withdrawal_date,
    sub.credits, e.created_date, e.updated_date;
GO

-- Verification queries (commented out for production)
-- SELECT TOP 5 * FROM vw_StudentProfile ORDER BY student_id;
-- SELECT TOP 5 * FROM vw_ClassRoll WHERE class_id = 1 ORDER BY student_name;
-- SELECT TOP 5 * FROM vw_AttendanceSummary ORDER BY attendance_date DESC, class_id;
-- SELECT TOP 5 * FROM vw_AcademicPerformance WHERE enrollment_status = 'Active' ORDER BY student_id, class_id;

PRINT 'All 4 reporting views created successfully.';
PRINT 'Views: vw_StudentProfile, vw_ClassRoll, vw_AttendanceSummary, vw_AcademicPerformance';
