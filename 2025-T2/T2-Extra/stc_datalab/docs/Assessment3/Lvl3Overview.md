**Level 3: Production Mindset Assessment**

This level focuses on production-ready practices, including backup and recovery procedures, data validation, and operational readiness for real-world deployment.

## 🎯 **Level 3 Overview: He can deploy and maintain a production system.**
This level demonstrates the ability to implement production-grade practices, including backup and recovery procedures, data validation, and operational readiness for real-world deployment.

---

## **Task 1: Operational Runbook

### **What I've Done:**
Created a comprehensive operational runbook that documents all critical procedures, backup and recovery processes, troubleshooting steps, and change management protocols for the student data system.

### **Why It Matters:**
An operational runbook is essential for maintaining system reliability and enabling quick response to incidents. It provides standardized procedures that ensure consistent handling of routine tasks and emergency situations, reducing downtime and human error while facilitating knowledge transfer to new team members.

### **Key Implementation Details:**

```bash
# macOs command to run a full backup of the database
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q "BACKUP DATABASE StC_SchoolLab TO DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full_Test.bak' WITH FORMAT;"

# macOs command to verify a backup file
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q "RESTORE VERIFYONLY FROM DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full_Test.bak';"
```

**1. Backup & Restore Procedures:**
- Full backup and differential backup T-SQL scripts (Express Edition compatible - no compression)
- macOS command-line execution examples with timestamp-based file naming
- SSMS GUI step-by-step instructions with screenshots guidance
- RPO/RTO targets: 1 hour max data loss, 30 minutes max downtime
- Three-stage restore process: verify backup → test restore → production restore
- Post-restore validation checklist (row counts, constraints, permissions)

**2. Key Reports Execution Guide:**
- All 4 stored procedures documented with parameter explanations
- `sp_GetStudentProfile`: Student lookup with 3 result sets (profile, enrollments, attendance)
- `sp_EnrollmentSummaryByYear`: Class capacity planning with utilization metrics
- `sp_AttendanceByDate`: Daily roll call with absence follow-up contacts
- `sp_GetTableDataExport`: Data export for SEQTA/Power BI integration
- Common use cases and capacity status indicators explained

**3. Common Incidents & Troubleshooting:**
- **Report discrepancies:** Date range validation, duplicate detection, status code reconciliation
- **Failed imports:** Error log analysis, staging table rollback, CSV validation steps
- **Duplicate records:** Detection queries, merge strategy with foreign key reassignment
- **Performance issues:** Execution plans, missing index detection, query optimization techniques
- **Missing Power BI data:** Data lineage tracing, refresh validation, permissions checks

**4. Permissions & Security:**
- Least privilege access model by role (ICT Admin, Leadership, Teachers, Admin Staff)
- Child data protection requirements (no direct table access, audit logging, encrypted backups)
- User account creation examples with GRANT/DENY statements
- Audit logging implementation with trigger-based tracking

**5. System Integration Monitoring:**
- SEQTA import health checks (daily 6 AM schedule, row count validation)
- Power BI refresh monitoring (4-hour intervals, NULL value detection)
- Database health queries (space usage, blocking queries, backup history)
- Alert conditions and escalation thresholds

**6. Change Management & Disaster Recovery:**
- 7-step pre-deployment checklist (backup, test, document, notify, schedule, rollback plan, validate)
- Complete database loss recovery procedure (9 steps from assessment to post-mortem)
- Emergency contacts matrix with availability windows
- Document version history tracking

**Validation Results:**
```bash
# Tested backup procedure (Express Edition compatible)
BACKUP DATABASE successfully processed 818 pages in 0.263 seconds (24.284 MB/sec)
The backup set on file 1 is valid.
```

**File Location:** `docs/Assessment3/06_runbook.md` (772 lines, comprehensive operational guide)

## **Task 2: Troubleshooting Scenarios**

### **What I've Done:**

### **Why It Matters:**

### **Key Implementation Details:**

---

## **Task 3: Training Materials**

### **What I've Done:**

### **Why It Matters:**

### **Key Implementation Details:**

---

## **Task 4: Presentation Script**

### **What I've Done:**

### **Why It Matters:**

### **Key Implementation Details:**

---