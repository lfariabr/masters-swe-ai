# Level 1 Task 4: Backup & Restore

## Overview
This task demonstrates backup and restore procedures critical for production database maintenance. Shows both T-SQL methods for full backup and restore to a new database name, with verification steps.

## Step-by-Step Commands

### 1. Create Backup Directory in Container
```bash
docker exec sqlserver mkdir -p /var/opt/mssql/backup
```
**Purpose**: Creates directory for backup files inside the SQL Server container.
- Ensures backup location exists
- Follows SQL Server default backup path conventions

### 2. Execute Backup and Restore Script
```bash
# Codespaces Ubuntu
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -i /workspaces/masters-swe-ai/2025-T2/T2-Extra/stc_datalab/sql/07_backup_restore.sql

# macOs 
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -i /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2025-T2/T2-Extra/stc_datalab/sql/07_backup_restore.sql
```
**Purpose**: Performs full backup and restore demonstration.
- Creates backup file: StC_SchoolLab_Full.bak
- Verifies backup integrity
- Restores to new database: StC_SchoolLab_RESTORE
- Validates restored data
- Cleans up test database

## Backup Process Details

### Full Database Backup
```sql
BACKUP DATABASE StC_SchoolLab
TO DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full.bak'
WITH FORMAT,
     NAME = 'Full Backup of StC_SchoolLab',
     DESCRIPTION = 'Complete backup created for disaster recovery testing';
```
**Purpose**: Creates complete database backup.
- FORMAT: Overwrites existing backup files
- NAME/DESCRIPTION: Metadata for backup identification
- Location: Inside container at /var/opt/mssql/backup/

### Backup Verification
```sql
RESTORE VERIFYONLY
FROM DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full.bak';
```
**Purpose**: Validates backup file without restoring.
- Checks file integrity
- Confirms backup is readable
- Quick validation before actual restore

## Restore Process Details

### Restore to New Database
```sql
RESTORE DATABASE StC_SchoolLab_RESTORE
FROM DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full.bak'
WITH MOVE 'StC_SchoolLab' TO '/var/opt/mssql/data/StC_SchoolLab_RESTORE.mdf',
     MOVE 'StC_SchoolLab_log' TO '/var/opt/mssql/data/StC_SchoolLab_RESTORE_log.ldf',
     NORECOVERY;
```
**Purpose**: Restores backup to a new database name.
- MOVE: Relocates files to prevent conflicts
- NORECOVERY: Keeps database in restoring state
- New name: StC_SchoolLab_RESTORE (matches requirement)

### Complete the Restore
```sql
RESTORE DATABASE StC_SchoolLab_RESTORE WITH RECOVERY;
```
**Purpose**: Brings restored database online.
- RECOVERY: Makes database accessible
- Completes the restore process

## Verification Steps

### Data Integrity Check
```sql
USE StC_SchoolLab_RESTORE;
SELECT COUNT(*) as StudentsCount FROM Students;
SELECT COUNT(*) as ClassesCount FROM Classes;
SELECT COUNT(*) as AttendanceRecords FROM Attendance;
```
**Purpose**: Validates all data was restored correctly.
- Compares record counts with original
- Ensures no data loss during backup/restore

## Performance Results
- **Backup Size**: 610 pages (~4.8MB)
- **Backup Time**: < 0.1 seconds (48 MB/sec)
- **Restore Time**: < 0.3 seconds (64 MB/sec)
- **Data Verification**: All records intact

## Production Considerations
- **RPO (Recovery Point Objective)**: 1 hour maximum data loss
- **RTO (Recovery Time Objective)**: 4 hours maximum downtime
- **Backup Frequency**: Daily full + hourly logs in production
- **Storage**: Multiple locations with redundancy
- **Testing**: Monthly restore tests required

## Emergency Restore Checklist
1. Assess damage extent
2. Stop application connections
3. Identify last good backup
4. Test restore in non-production
5. Execute production restore
6. Verify data integrity
7. Update application connections
8. Document incident

## Notes
- Backup file stored inside container (/var/opt/mssql/backup/)
- Restore uses MOVE to create new physical files
- NORECOVERY/RECOVERY pattern allows for additional restores
- Verification ensures data integrity
- Process matches production disaster recovery procedures