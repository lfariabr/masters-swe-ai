-- Backup and Restore Procedures for StC School Data Lab
-- Demonstrating disaster recovery capabilities

USE master;
GO

-- Full backup of StC_SchoolLab database
BACKUP DATABASE StC_SchoolLab
TO DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full.bak'
WITH FORMAT,
     NAME = 'Full Backup of StC_SchoolLab',
     DESCRIPTION = 'Complete backup created for disaster recovery testing';
GO

-- Verify backup file exists and is readable
RESTORE VERIFYONLY
FROM DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full.bak';
GO

-- Restore to a new database name: StC_SchoolLab_RESTORE
RESTORE DATABASE StC_SchoolLab_RESTORE
FROM DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full.bak'
WITH MOVE 'StC_SchoolLab' TO '/var/opt/mssql/data/StC_SchoolLab_RESTORE.mdf',
     MOVE 'StC_SchoolLab_log' TO '/var/opt/mssql/data/StC_SchoolLab_RESTORE_log.ldf',
     NORECOVERY;  -- Allows for additional differential/log restores if needed
GO

-- Bring the restored database online
RESTORE DATABASE StC_SchoolLab_RESTORE WITH RECOVERY;
GO

-- Verify restore was successful
USE StC_SchoolLab_RESTORE;
GO

SELECT COUNT(*) as StudentsCount FROM Students;
SELECT COUNT(*) as ClassesCount FROM Classes;
SELECT COUNT(*) as AttendanceRecords FROM Attendance;
GO

-- Clean up: Drop the restored database (for demo purposes)
USE master;
GO

DROP DATABASE StC_SchoolLab_RESTORE;
GO