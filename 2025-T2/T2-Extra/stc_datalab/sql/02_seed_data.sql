USE StC_SchoolLab;
GO

SET NOCOUNT ON;

PRINT '--- Level 2 Task 2.1: Seeding realistic demo data ---';
PRINT 'Reminder: run sql/03_reset_data.sql before executing this script to avoid duplicate key errors.';

IF EXISTS (SELECT 1 FROM Enrollments)
    OR EXISTS (SELECT 1 FROM Students)
    OR EXISTS (SELECT 1 FROM Staff)
    OR EXISTS (SELECT 1 FROM Classes)
    OR EXISTS (SELECT 1 FROM Subjects)
    OR EXISTS (SELECT 1 FROM Attendance)
BEGIN
    RAISERROR('Seed script expects empty core tables. Please reset the database first.', 16, 1);
    RETURN;
END;

DECLARE @Inserted INT;

/* --------------------------------------------------------------------- */
/* 1. Subjects                                                           */
/* --------------------------------------------------------------------- */
DECLARE @SubjectSeed TABLE (
    subject_name NVARCHAR(100),
    subject_code NVARCHAR(20),
    description NVARCHAR(500),
    year_level INT,
    semester NVARCHAR(20),
    credits INT,
    is_active BIT
);

INSERT INTO @SubjectSeed VALUES
('Mathematics Foundations', 'MATH7A', 'Lower secondary mathematics with numeracy focus.', 7, 'Semester 1', 5, 1),
('Mathematics Extension', 'MATH8B', 'Problem solving and extension topics.', 8, 'Semester 2', 5, 1),
('English Language & Literature', 'ENG7C', 'Reading circles and persuasive writing.', 7, 'Semester 1', 5, 1),
('English for Global Citizens', 'ENG9G', 'World literature with debating.', 9, 'Semester 2', 5, 1),
('Science Inquiry', 'SCI8D', 'Lab-based investigation program.', 8, 'Semester 1', 5, 1),
('Life Sciences', 'SCI10B', 'Biology, ecology and field work module.', 10, 'Semester 2', 5, 1),
('Humanities & Civics', 'HUM8A', 'Australian history and civics curriculum.', 8, 'Semester 1', 5, 1),
('Economics & Enterprise', 'ECO10E', 'Entrepreneurship challenge coursework.', 10, 'Semester 2', 5, 1),
('Digital Technologies', 'DIG7F', 'Intro to Python and micro:bit projects.', 7, 'Semester 2', 5, 1),
('Media & Communications', 'MED9B', 'Video storytelling and journalism.', 9, 'Semester 1', 5, 1),
('Visual Arts Studio', 'ART8S', 'Studio practice with mixed media.', 8, 'Semester 1', 5, 1),
('Music Ensemble', 'MUS9P', 'Performance program with weekly rehearsals.', 9, 'Semester 2', 5, 0);

INSERT INTO Subjects (subject_name, subject_code, description, year_level, semester, credits, is_active)
SELECT subject_name, subject_code, description, year_level, semester, credits, is_active
FROM @SubjectSeed;

SET @Inserted = @@ROWCOUNT;
PRINT CONCAT('Subjects inserted: ', @Inserted);

/* --------------------------------------------------------------------- */
/* 2. Staff (20 people, mixed roles and quality issues)                   */
/* --------------------------------------------------------------------- */
DECLARE @StaffSeed TABLE (
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    role NVARCHAR(50),
    email NVARCHAR(100),
    phone NVARCHAR(20),
    department NVARCHAR(100),
    hire_date DATE,
    is_active BIT
);

INSERT INTO @StaffSeed VALUES
('Isabella', 'Tran', 'Teacher', 'isabella.tran@stc.edu.au', '0401000101', 'Mathematics', '2015-01-19', 1),
('Marcus', 'Nguyen', 'Teacher', 'Marcus.Nguyen@stc.edu.au', NULL, 'English', '2016-03-07', 1),
('Priya', 'Patel', 'Teacher', 'priya.patel@stc.edu.au', '0402002222', 'Science', '2017-05-01', 1),
('Liam', 'Teo', 'Teacher', 'liam.teo@stc.edu.au', 'N/A', 'Humanities', '2013-08-25', 1),
('Sofia', 'Haddad', 'Teacher', 'sofia.haddad@stc.edu.au', '0403000333', 'Languages', '2018-02-12', 1),
('Charlotte', 'Baker', 'Teacher', 'charlotte.baker@stc.edu.au', '0404000444', 'Arts', '2014-11-10', 1),
('Jonah', 'Silva', 'Teacher', 'jonah.silva@stc.edu.au', '0405000555', 'Technology', '2019-07-08', 1),
('Aisha', 'Rahman', 'Teacher', 'Aisha.Rahman@stc.edu.au', '0406000666', 'Mathematics', '2020-01-06', 1),
('Ethan', 'Rodriguez', 'Teacher', 'ethan.rodriquez@stc.edu.au', '0407000777', 'Science', '2012-06-18', 1),
('Maya', 'O''Connor', 'Teacher', 'Maya.OConnor@stc.edu.au', '0408000888', 'Performing Arts', '2011-09-05', 1),
('Daniel', 'Cole', 'Teacher', 'daniel.cole@stc.edu.au', '0409000999', 'English', '2010-02-15', 0),
('Hanna', 'Winters', 'Teacher', 'hanna.winters@stc.edu.au', '0410000100', 'Humanities', '2019-05-20', 1),
('Oliver', 'Costa', 'Teacher', 'oliver.costa@stc.edu.au', '0411000111', 'Science', '2014-03-17', 1),
('Zoe', 'Martinez', 'Teacher', 'zoe.martinez@stc.edu.au', '0412000122', 'Technology', '2018-10-29', 1),
('Henry', 'Kerr', 'Teacher', 'henry.kerr@stc.edu.au', '0413000133', 'Mathematics', '2021-04-12', 1),
('Grace', 'Lam', 'Admin', 'grace.lam@stc.edu.au', '0414000144', 'Registrar', '2016-09-19', 1),
('Noah', 'Browning', 'Counsellor', 'noah.browning@stc.edu.au', NULL, 'Student Services', '2015-07-13', 1),
('Elena', 'Rossi', 'ICT', 'ELENA.ROSSI@STC.EDU.AU', '0415000155', 'ICT', '2013-05-06', 1),
('Callum', 'Wright', 'Support Staff', NULL, NULL, 'Facilities', '2011-02-28', 1),
('Amelie', 'Dubois', 'Teacher', 'amelie.dubois@stc.edu.au', '0416000166', 'Languages', '2022-02-14', 1);

INSERT INTO Staff (first_name, last_name, role, email, phone, department, hire_date, is_active)
SELECT first_name, last_name, role, email, phone, department, hire_date, is_active
FROM @StaffSeed;

SET @Inserted = @@ROWCOUNT;
PRINT CONCAT('Staff inserted: ', @Inserted);

/* --------------------------------------------------------------------- */
/* 3. Students (200 generated rows with deliberate quality issues)        */
/* --------------------------------------------------------------------- */
DECLARE @StudentTarget INT = 200;

DECLARE @FirstNames TABLE (id INT IDENTITY(1,1), first_name NVARCHAR(50));
INSERT INTO @FirstNames VALUES
('Oliver'),('Amelia'),('Noah'),('Mia'),('Ethan'),('Isla'),('Lucas'),('Ava'),('Leo'),('Sienna'),
('Aria'),('Hudson'),('Layla'),('Mason'),('Emily'),('Hugo'),('Zara'),('Ezra'),('Chloe'),('Harper');
DECLARE @FirstNameCount INT = (SELECT COUNT(*) FROM @FirstNames);

DECLARE @LastNames TABLE (id INT IDENTITY(1,1), last_name NVARCHAR(50));
INSERT INTO @LastNames VALUES
('Smith'),('Johnson'),('Williams'),('Brown'),('Jones'),('Garcia'),('Miller'),('Davis'),('Martinez'),('Hernandez'),
('Lopez'),('Wilson'),('Anderson'),('Thomas'),('Taylor'),('Moore'),('Jackson'),('Martin'),('Lee'),('Perez');
DECLARE @LastNameCount INT = (SELECT COUNT(*) FROM @LastNames);

DECLARE @Street TABLE (id INT IDENTITY(1,1), street NVARCHAR(100));
INSERT INTO @Street VALUES
('Federation Ave'),('Kauri Street'),('Harbour View Rd'),('Laneway 9'),('Greenway Blvd'),('Pacific Parade'),
('Sunset Loop'),('Banksia Crescent'),('Seaview Terrace'),('Northern Ridge');
DECLARE @StreetCount INT = (SELECT COUNT(*) FROM @Street);

;WITH NumberedStudents AS (
    SELECT TOP (@StudentTarget)
        ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n
    FROM sys.all_objects AS so1
    CROSS JOIN sys.all_objects AS so2
)
INSERT INTO Students (
    first_name,
    last_name,
    date_of_birth,
    address,
    phone,
    email,
    medical_info,
    emergency_contact,
    emergency_phone,
    enrollment_year,
    student_number,
    created_date,
    updated_date
)
SELECT
    CASE WHEN n % 22 = 0 THEN LOWER(fn.first_name) ELSE fn.first_name END AS first_name,
    CASE WHEN n % 60 = 0 THEN ln.last_name + '  ' ELSE ln.last_name END AS last_name,
    DATEFROMPARTS(2007 - (n % 5), ((n % 12) + 1), ((n % 27) + 1)) AS date_of_birth,
    CASE 
        WHEN n % 14 = 0 THEN 'International Boarding, Singapore'
        WHEN n % 9 = 0 THEN 'Address Pending'
        ELSE CONCAT(
            100 + (n % 200), ' ', st.street,
            CASE WHEN n % 17 = 0 THEN ', Jakarta, ID' ELSE ', Sydney NSW' END)
    END AS address,
    CASE 
        WHEN n % 9 = 0 THEN NULL
        WHEN n % 33 = 0 THEN '???'
        ELSE CONCAT('04', RIGHT('00000000' + CAST(n * 73 AS VARCHAR(8)), 8))
    END AS phone,
    CASE
        WHEN n % 45 = 0 THEN 'duplicate.email@students.stc.edu.au'
        WHEN n % 18 = 0 THEN UPPER(fn.first_name + '.' + ln.last_name + '@students.stc.edu.au')
        ELSE LOWER(fn.first_name + '.' + ln.last_name + CAST( (n % 5) + 1 AS NVARCHAR(1)) + '@students.stc.edu.au')
    END AS email,
    CASE
        WHEN n % 6 = 0 THEN 'Allergy: Nuts'
        WHEN n % 11 = 0 THEN 'Asthma'
        WHEN n % 15 = 0 THEN 'Requires epi-pen'
        ELSE NULL
    END AS medical_info,
    CASE WHEN n % 40 = 0 THEN NULL ELSE CONCAT('Parent ', fn.first_name, ' ', ln.last_name) END AS emergency_contact,
    CASE
        WHEN n % 17 = 0 THEN NULL
        ELSE CONCAT('02', RIGHT('00000000' + CAST(n * 41 AS VARCHAR(8)), 8))
    END AS emergency_phone,
    2018 + (n % 6) AS enrollment_year,
    CONCAT('STC', RIGHT('0000' + CAST(n AS VARCHAR(4)), 4)) AS student_number,
    DATEADD(DAY, -n, SYSDATETIME()),
    DATEADD(DAY, -n, SYSDATETIME())
FROM NumberedStudents ns
CROSS APPLY (
    SELECT first_name FROM @FirstNames WHERE id = ((ns.n - 1) % @FirstNameCount) + 1
) fn
CROSS APPLY (
    SELECT last_name FROM @LastNames WHERE id = ((ns.n - 1) % @LastNameCount) + 1
) ln
CROSS APPLY (
    SELECT street FROM @Street WHERE id = ((ns.n - 1) % @StreetCount) + 1
) st;

SET @Inserted = @@ROWCOUNT;
PRINT CONCAT('Students inserted: ', @Inserted);

/* --------------------------------------------------------------------- */
/* 4. Classes (30 rows referencing staff + subjects)                      */
/* --------------------------------------------------------------------- */
DECLARE @ClassTarget INT = 30;
DECLARE @SubjectCount INT = (SELECT COUNT(*) FROM Subjects);
DECLARE @TeacherCount INT = (SELECT COUNT(*) FROM Staff WHERE role = 'Teacher');

;WITH SubjectCycle AS (
    SELECT subject_id,
           year_level,
           semester,
           subject_name,
           ROW_NUMBER() OVER (ORDER BY subject_id) AS rn
    FROM Subjects
),
TeacherCycle AS (
    SELECT staff_id,
           ROW_NUMBER() OVER (ORDER BY staff_id) AS rn
    FROM Staff
    WHERE role = 'Teacher'
),
ClassSeq AS (
    SELECT TOP (@ClassTarget) ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS rn
    FROM sys.all_objects
)
INSERT INTO Classes (
    subject_id,
    staff_id,
    class_name,
    year_level,
    semester,
    max_students,
    room,
    schedule,
    is_active,
    created_date
)
SELECT
    sc.subject_id,
    tc.staff_id,
    CONCAT(sc.subject_name, ' ', CHAR(64 + ((cs.rn - 1) % 4) + 1)) AS class_name,
    sc.year_level,
    CASE WHEN cs.rn % 2 = 0 THEN 'Semester 2' ELSE 'Semester 1' END,
    22 + (cs.rn % 6) * 2,
    CASE WHEN cs.rn % 10 = 0 THEN NULL ELSE CONCAT('Room ', 100 + cs.rn) END,
    CASE
        WHEN cs.rn % 3 = 0 THEN 'Mon 09:00 / Wed 11:00'
        WHEN cs.rn % 3 = 1 THEN 'Tue 10:15 / Thu 12:15'
        ELSE 'Fri 08:30 / Fri 11:30'
    END,
    CASE WHEN cs.rn % 11 = 0 THEN 0 ELSE 1 END,
    SYSDATETIME()
FROM ClassSeq cs
JOIN SubjectCycle sc ON sc.rn = ((cs.rn - 1) % @SubjectCount) + 1
JOIN TeacherCycle tc ON tc.rn = ((cs.rn - 1) % @TeacherCount) + 1;

SET @Inserted = @@ROWCOUNT;
PRINT CONCAT('Classes inserted: ', @Inserted);

/* --------------------------------------------------------------------- */
/* 5. Enrollments (500 rows, varied statuses & grades)                    */
/* --------------------------------------------------------------------- */
DECLARE @EnrollmentTarget INT = 500;
DECLARE @StudentCount INT = (SELECT COUNT(*) FROM Students);
DECLARE @ClassCount INT = (SELECT COUNT(*) FROM Classes);

;WITH StudentCycle AS (
    SELECT student_id,
           ROW_NUMBER() OVER (ORDER BY student_id) AS student_rn
    FROM Students
),
ClassCycle AS (
    SELECT class_id,
           ROW_NUMBER() OVER (ORDER BY class_id) AS class_rn
    FROM Classes
),
UniquePairs AS (
    SELECT TOP (@EnrollmentTarget)
        s.student_id,
        c.class_id,
        ROW_NUMBER() OVER (ORDER BY s.student_rn, c.class_rn) AS n
    FROM StudentCycle s
    CROSS JOIN ClassCycle c
)
INSERT INTO Enrollments (
    student_id,
    class_id,
    enrollment_date,
    status,
    grade,
    withdrawal_date,
    created_date,
    updated_date
)
SELECT
    up.student_id,
    up.class_id,
    DATEADD(DAY, -((up.n * 2) % 730), CAST('2024-12-01' AS DATE)) AS enrollment_date,
    CASE
        WHEN up.n % 23 = 0 THEN 'Withdrawn'
        WHEN up.n % 37 = 0 THEN 'Completed'
        WHEN up.n % 41 = 0 THEN 'Pending'
        ELSE 'Active'
    END AS status,
    CASE
        WHEN up.n % 9 = 0 THEN NULL
        WHEN up.n % 11 = 0 THEN 'A '
        WHEN up.n % 13 = 0 THEN 'b'
        WHEN up.n % 17 = 0 THEN 'INC'
        ELSE CHOOSE((up.n % 5) + 1, 'A', 'B+', 'B', 'C', 'D')
    END AS grade,
    CASE WHEN up.n % 23 = 0 THEN DATEADD(DAY, 7, DATEADD(DAY, -((up.n * 2) % 730), CAST('2024-12-01' AS DATE))) END AS withdrawal_date,
    DATEADD(HOUR, -up.n, SYSDATETIME()),
    DATEADD(HOUR, -up.n, SYSDATETIME())
FROM UniquePairs up;

SET @Inserted = @@ROWCOUNT;
PRINT CONCAT('Enrollments inserted: ', @Inserted);

/* --------------------------------------------------------------------- */
/* 6. Attendance (800 rows across 10 days for first 80 enrollments)       */
/* --------------------------------------------------------------------- */
;WITH AttendanceDates AS (
    SELECT TOP (10)
        ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS rn,
        DATEADD(DAY, -ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) + 1, CAST('2024-11-25' AS DATE)) AS attendance_date
    FROM sys.all_objects
),
StudentClass AS (
    SELECT TOP (80)
        e.student_id,
        e.class_id,
        ROW_NUMBER() OVER (ORDER BY e.enrollment_id) AS rn
    FROM Enrollments e
    WHERE e.status <> 'Withdrawn'
),
TeacherLookup AS (
    SELECT class_id, staff_id
    FROM Classes
)
INSERT INTO Attendance (
    student_id,
    class_id,
    attendance_date,
    status,
    notes,
    marked_by,
    marked_date
)
SELECT
    sc.student_id,
    sc.class_id,
    d.attendance_date,
    CASE
        WHEN (sc.rn + d.rn) % 11 = 0 THEN 'Absent'
        WHEN (sc.rn + d.rn) % 7 = 0 THEN 'Late'
        WHEN (sc.rn + d.rn) % 5 = 0 THEN 'Excused'
        ELSE 'Present'
    END AS status,
    CASE
        WHEN (sc.rn + d.rn) % 11 = 0 THEN 'Illness reported'
        WHEN (sc.rn + d.rn) % 7 = 0 THEN 'Bus delay / traffic'
        WHEN (sc.rn + d.rn) % 5 = 0 THEN 'Music tour pull-out'
        WHEN (sc.rn + d.rn) % 13 = 0 THEN 'Marked from SEQTA CSV'
        ELSE NULL
    END AS notes,
    tl.staff_id,
    SYSDATETIME()
FROM StudentClass sc
CROSS JOIN AttendanceDates d
JOIN TeacherLookup tl ON tl.class_id = sc.class_id;

SET @Inserted = @@ROWCOUNT;
PRINT CONCAT('Attendance inserted: ', @Inserted);

/* --------------------------------------------------------------------- */
/* Summary counts                                                         */
/* --------------------------------------------------------------------- */
PRINT '--- Summary after seeding ---';

DECLARE @SubjectTotal INT = (SELECT COUNT(*) FROM Subjects);
DECLARE @StaffTotal INT = (SELECT COUNT(*) FROM Staff);
DECLARE @StudentTotal INT = (SELECT COUNT(*) FROM Students);
DECLARE @ClassTotal INT = (SELECT COUNT(*) FROM Classes);
DECLARE @EnrollmentTotal INT = (SELECT COUNT(*) FROM Enrollments);
DECLARE @AttendanceTotal INT = (SELECT COUNT(*) FROM Attendance);

PRINT CONCAT('Subjects total: ', @SubjectTotal);
PRINT CONCAT('Staff total: ', @StaffTotal);
PRINT CONCAT('Students total: ', @StudentTotal);
PRINT CONCAT('Classes total: ', @ClassTotal);
PRINT CONCAT('Enrollments total: ', @EnrollmentTotal);
PRINT CONCAT('Attendance total: ', @AttendanceTotal);

PRINT 'Seed script completed with intentional nulls, casing issues, and international scenarios for reporting tests.';
