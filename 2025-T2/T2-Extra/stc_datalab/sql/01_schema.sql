-- Schema for StC School Data Lab
-- Core tables matching school management systems like Synergetic and SEQTA

USE StC_SchoolLab;
GO

-- Students table (privacy-sensitive fields included)
CREATE TABLE Students (
    student_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    address NVARCHAR(255),
    phone NVARCHAR(20),
    email NVARCHAR(100),
    medical_info NVARCHAR(500), -- Privacy-sensitive: medical conditions, allergies
    emergency_contact NVARCHAR(100),
    emergency_phone NVARCHAR(20),
    enrollment_year INT NOT NULL,
    student_number NVARCHAR(20) UNIQUE NOT NULL, -- Unique identifier like in school systems
    created_date DATETIME2 DEFAULT GETDATE(),
    updated_date DATETIME2 DEFAULT GETDATE()
);
GO

-- Staff table (role-based attributes)
CREATE TABLE Staff (
    staff_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    role NVARCHAR(50) NOT NULL, -- e.g., 'Teacher', 'Principal', 'Admin', 'Support Staff'
    email NVARCHAR(100) UNIQUE,
    phone NVARCHAR(20),
    department NVARCHAR(100),
    hire_date DATE,
    is_active BIT DEFAULT 1,
    created_date DATETIME2 DEFAULT GETDATE(),
    updated_date DATETIME2 DEFAULT GETDATE()
);
GO

-- Subjects table (matching school curriculum)
CREATE TABLE Subjects (
    subject_id INT IDENTITY(1,1) PRIMARY KEY,
    subject_name NVARCHAR(100) NOT NULL,
    subject_code NVARCHAR(20) UNIQUE NOT NULL, -- e.g., 'MATH101', 'ENG202'
    description NVARCHAR(500),
    year_level INT, -- e.g., 7, 8, 9 for secondary
    semester NVARCHAR(20), -- e.g., 'Semester 1', 'Semester 2'
    credits INT DEFAULT 1,
    is_active BIT DEFAULT 1,
    created_date DATETIME2 DEFAULT GETDATE()
);
GO

-- Classes table (with teacher assignments)
CREATE TABLE Classes (
    class_id INT IDENTITY(1,1) PRIMARY KEY,
    subject_id INT NOT NULL,
    staff_id INT NOT NULL, -- Teacher assigned to class
    class_name NVARCHAR(100) NOT NULL, -- e.g., 'Mathematics 8A'
    year_level INT NOT NULL,
    semester NVARCHAR(20) NOT NULL,
    max_students INT DEFAULT 25,
    room NVARCHAR(50),
    schedule NVARCHAR(200), -- e.g., 'Mon 9:00-10:30, Wed 9:00-10:30'
    is_active BIT DEFAULT 1,
    created_date DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);
GO

-- Enrollments table (student-class relationships)
CREATE TABLE Enrollments (
    enrollment_id INT IDENTITY(1,1) PRIMARY KEY,
    student_id INT NOT NULL,
    class_id INT NOT NULL,
    enrollment_date DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    status NVARCHAR(20) DEFAULT 'Active', -- 'Active', 'Withdrawn', 'Completed'
    grade NVARCHAR(5), -- e.g., 'A', 'B+', 'C', NULL for current
    withdrawal_date DATE,
    created_date DATETIME2 DEFAULT GETDATE(),
    updated_date DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (class_id) REFERENCES Classes(class_id),
    UNIQUE (student_id, class_id) -- Prevent duplicate enrollments
);
GO

-- Attendance table (simple tracking like SEQTA)
CREATE TABLE Attendance (
    attendance_id INT IDENTITY(1,1) PRIMARY KEY,
    student_id INT NOT NULL,
    class_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    status NVARCHAR(20) NOT NULL, -- 'Present', 'Absent', 'Late', 'Excused'
    notes NVARCHAR(255), -- e.g., reason for absence
    marked_by INT, -- staff_id who marked attendance
    marked_date DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (class_id) REFERENCES Classes(class_id),
    FOREIGN KEY (marked_by) REFERENCES Staff(staff_id),
    UNIQUE (student_id, class_id, attendance_date) -- One record per student per class per day
);
GO

-- Basic indexes for performance
CREATE INDEX IX_Students_LastName ON Students(last_name);
CREATE INDEX IX_Students_EnrollmentYear ON Students(enrollment_year);
CREATE INDEX IX_Staff_Role ON Staff(role);
CREATE INDEX IX_Classes_SubjectId ON Classes(subject_id);
CREATE INDEX IX_Classes_StaffId ON Classes(staff_id);
CREATE INDEX IX_Enrollments_StudentId ON Enrollments(student_id);
CREATE INDEX IX_Enrollments_ClassId ON Enrollments(class_id);
CREATE INDEX IX_Attendance_StudentId ON Attendance(student_id);
CREATE INDEX IX_Attendance_ClassId ON Attendance(class_id);
CREATE INDEX IX_Attendance_Date ON Attendance(attendance_date);
GO

-- Add updated_date trigger for Students
CREATE TRIGGER TR_Students_UpdateDate
ON Students
AFTER UPDATE
AS
BEGIN
    UPDATE Students
    SET updated_date = GETDATE()
    FROM Students s
    INNER JOIN inserted i ON s.student_id = i.student_id;
END;
GO

-- Add updated_date trigger for Enrollments
CREATE TRIGGER TR_Enrollments_UpdateDate
ON Enrollments
AFTER UPDATE
AS
BEGIN
    UPDATE Enrollments
    SET updated_date = GETDATE()
    FROM Enrollments e
    INNER JOIN inserted i ON e.enrollment_id = i.enrollment_id;
END;
GO