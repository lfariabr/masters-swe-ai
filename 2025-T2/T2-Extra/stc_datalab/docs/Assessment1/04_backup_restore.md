# Backup & Restore Documentation

## Overview
This document demonstrates backup and restore procedures for the StC_SchoolLab database, matching production disaster recovery requirements. The procedures use both T-SQL methods as would be used in production environments.

## Recovery Point Objectives (RPO)
- **RPO**: 1 hour (maximum data loss acceptable)
- **RTO**: 4 hours (maximum time to restore service)
- **Backup Frequency**: Daily full backups, hourly transaction log backups in production

## Backup Procedures

### Full Database Backup (T-SQL Method)
```sql
USE master;
GO

BACKUP DATABASE StC_SchoolLab
TO DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full.bak'
WITH FORMAT,
     NAME = 'Full Backup of StC_SchoolLab',
     DESCRIPTION = 'Complete backup created for disaster recovery testing';
GO
```

**Steps:**
1. Switch to master database context
2. Execute BACKUP DATABASE command
3. Specify backup file location (in container: `/var/opt/mssql/backup/`)
4. Use FORMAT to overwrite existing files
5. Include descriptive name and description

### Verification
```sql
RESTORE VERIFYONLY
FROM DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full.bak';
GO
```
This command verifies the backup file is readable and valid without performing the actual restore.

## Restore Procedures

### Restore to New Database Name
```sql
USE master;
GO

RESTORE DATABASE StC_SchoolLab_RESTORE
FROM DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full.bak'
WITH MOVE 'StC_SchoolLab' TO '/var/opt/mssql/data/StC_SchoolLab_RESTORE.mdf',
     MOVE 'StC_SchoolLab_log' TO '/var/opt/mssql/data/StC_SchoolLab_RESTORE_log.ldf',
     NORECOVERY;
GO

RESTORE DATABASE StC_SchoolLab_RESTORE WITH RECOVERY;
GO
```

**Steps:**
1. Switch to master database context
2. Execute RESTORE DATABASE with new name
3. Use MOVE to specify new file locations (prevents conflicts)
4. NORECOVERY keeps database in restoring state
5. RECOVERY brings database online

### Verification After Restore
```sql
USE StC_SchoolLab_RESTORE;
GO

SELECT COUNT(*) as StudentsCount FROM Students;
SELECT COUNT(*) as ClassesCount FROM Classes;
SELECT COUNT(*) as AttendanceRecords FROM Attendance;
GO
```

## Emergency Restore Checklist

### Scenario: Production Database Corruption
1. **Assess Damage**: Determine extent of data loss
2. **Stop Applications**: Prevent further data modification
3. **Identify Last Good Backup**: Check backup history
4. **Test Restore**: Always restore to test environment first
5. **Execute Restore**: Use production restore procedures
6. **Verify Data Integrity**: Run validation queries
7. **Update Applications**: Point to restored database
8. **Document Incident**: Record for post-mortem analysis

### T-SQL Commands for Emergency Restore
```sql
-- Stop all connections to database
ALTER DATABASE StC_SchoolLab SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
GO

-- Restore from backup
RESTORE DATABASE StC_SchoolLab
FROM DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full.bak'
WITH REPLACE;
GO

-- Allow multi-user access
ALTER DATABASE StC_SchoolLab SET MULTI_USER;
GO
```

## Best Practices
- **Test Regularly**: Perform restore tests monthly
- **Multiple Copies**: Store backups in multiple locations
- **Encryption**: Use encrypted backups for sensitive data
- **Compression**: Enable backup compression to save space
- **Monitoring**: Monitor backup success/failure
- **Documentation**: Keep detailed restore procedures current

## Production Considerations
- **Backup Storage**: Use dedicated backup storage with redundancy
- **Automation**: Schedule backups using SQL Server Agent jobs
- **Retention**: Implement backup retention policies
- **Security**: Secure backup files with appropriate permissions
- **Offsite Copies**: Maintain offsite backup copies for disaster recovery

## Test Results
- **Backup Size**: 610 pages (~4.8MB)
- **Backup Time**: < 0.1 seconds
- **Restore Time**: < 0.3 seconds
- **Data Verification**: All tables and records intact after restore

This demonstrates the ability to safely backup and restore SQL Server databases, critical for maintaining data integrity in school environments.