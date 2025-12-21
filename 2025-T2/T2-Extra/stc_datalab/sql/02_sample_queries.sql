-- Basic SQL Competence Demonstration
-- Sample queries for Level 1 Task 3

USE StC_SchoolLab;
GO

-- First, insert some sample data for demonstration
INSERT INTO Staff (first_name, last_name, role, email) VALUES
('John', 'Smith', 'Teacher', 'john.smith@school.edu'),
('Sarah', 'Johnson', 'Principal', 'sarah.johnson@school.edu'),
('Mike', 'Brown', 'Teacher', 'mike.brown@school.edu');
GO

INSERT INTO Subjects (subject_name, subject_code, year_level, semester) VALUES
('Mathematics', 'MATH101', 8, 'Semester 1'),
('English', 'ENG101', 8, 'Semester 1'),
('Science', 'SCI101', 8, 'Semester 1');
GO

INSERT INTO Classes (subject_id, staff_id, class_name, year_level, semester) VALUES
(1, 1, 'Mathematics 8A', 8, 'Semester 1'),
(2, 3, 'English 8B', 8, 'Semester 1'),
(3, 1, 'Science 8A', 8, 'Semester 1');
GO

INSERT INTO Students (first_name, last_name, date_of_birth, student_number, enrollment_year) VALUES
('Alice', 'Williams', '2010-05-15', 'STU001', 2025),
('Bob', 'Jones', '2010-08-22', 'STU002', 2025),
('Charlie', 'Davis', '2010-03-10', 'STU003', 2025),
('Diana', 'Miller', '2010-11-30', 'STU004', 2025);
GO

INSERT INTO Enrollments (student_id, class_id) VALUES
(1, 1), (1, 2), (1, 3),
(2, 1), (2, 2),
(3, 2), (3, 3),
(4, 1), (4, 3);
GO

INSERT INTO Attendance (student_id, class_id, attendance_date, status, marked_by) VALUES
(1, 1, '2025-12-20', 'Present', 1),
(1, 2, '2025-12-20', 'Present', 3),
(2, 1, '2025-12-20', 'Late', 1),
(2, 2, '2025-12-20', 'Absent', 3),
(3, 2, '2025-12-20', 'Present', 3),
(4, 1, '2025-12-20', 'Present', 1);
GO

-- Basic SQL Competence Queries

-- 1. SELECT + WHERE + ORDER BY (basic student/class queries)
-- Get all students in year 8, ordered by last name
SELECT student_id, first_name, last_name, enrollment_year
FROM Students
WHERE enrollment_year = 2025
ORDER BY last_name;
GO

-- 2. JOINS (especially LEFT JOIN for preserving all student records)
-- Get all students and their enrolled classes (LEFT JOIN to show students even if not enrolled)
SELECT s.first_name, s.last_name, c.class_name, e.enrollment_date
FROM Students s
LEFT JOIN Enrollments e ON s.student_id = e.student_id
LEFT JOIN Classes c ON e.class_id = c.class_id
ORDER BY s.last_name, c.class_name;
GO

-- 3. GROUP BY aggregates (COUNT/SUM for attendance reporting)
-- Count attendance by status for today
SELECT status, COUNT(*) as count
FROM Attendance
WHERE attendance_date = '2025-12-20'
GROUP BY status
ORDER BY count DESC;
GO

-- 4. More complex query: Student attendance summary
SELECT s.first_name, s.last_name,
       COUNT(a.attendance_id) as total_days,
       SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_days,
       SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) as absent_days,
       CAST(SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.attendance_id) AS DECIMAL(5,2)) as attendance_percentage
FROM Students s
LEFT JOIN Attendance a ON s.student_id = a.student_id
GROUP BY s.student_id, s.first_name, s.last_name
ORDER BY attendance_percentage DESC;
GO

-- 5. Class enrollment summary
SELECT c.class_name, st.first_name + ' ' + st.last_name as teacher,
       COUNT(e.student_id) as enrolled_students
FROM Classes c
JOIN Staff st ON c.staff_id = st.staff_id
LEFT JOIN Enrollments e ON c.class_id = e.class_id
GROUP BY c.class_id, c.class_name, st.first_name, st.last_name
ORDER BY enrolled_students DESC;
GO