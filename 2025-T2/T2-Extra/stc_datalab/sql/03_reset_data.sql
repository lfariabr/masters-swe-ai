-- Reset script for StC School Lab demo database
-- Deletes all data from child tables upward and reseeds identity columns

USE StC_SchoolLab;
GO

PRINT 'Starting data reset...';

-- Disable foreign key constraints temporarily (optional safety)
ALTER TABLE Attendance NOCHECK CONSTRAINT ALL;
ALTER TABLE Enrollments NOCHECK CONSTRAINT ALL;
ALTER TABLE Classes NOCHECK CONSTRAINT ALL;
ALTER TABLE Subjects NOCHECK CONSTRAINT ALL;
ALTER TABLE Staff NOCHECK CONSTRAINT ALL;
ALTER TABLE Students NOCHECK CONSTRAINT ALL;
GO

-- Delete data respecting dependency order
DELETE FROM Attendance;
DELETE FROM Enrollments;
DELETE FROM Classes;
DELETE FROM Subjects;
DELETE FROM Staff;
DELETE FROM Students;
GO

-- Re-enable constraints
ALTER TABLE Attendance CHECK CONSTRAINT ALL;
ALTER TABLE Enrollments CHECK CONSTRAINT ALL;
ALTER TABLE Classes CHECK CONSTRAINT ALL;
ALTER TABLE Subjects CHECK CONSTRAINT ALL;
ALTER TABLE Staff CHECK CONSTRAINT ALL;
ALTER TABLE Students CHECK CONSTRAINT ALL;
GO

-- Reseed identity columns so demo scripts start at 1 again
DBCC CHECKIDENT ('Attendance', RESEED, 0);
DBCC CHECKIDENT ('Enrollments', RESEED, 0);
DBCC CHECKIDENT ('Classes', RESEED, 0);
DBCC CHECKIDENT ('Subjects', RESEED, 0);
DBCC CHECKIDENT ('Staff', RESEED, 0);
DBCC CHECKIDENT ('Students', RESEED, 0);
GO

PRINT 'All demo data removed and identity values reset.';
