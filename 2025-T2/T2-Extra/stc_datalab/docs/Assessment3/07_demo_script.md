# StC SchoolLab Database - Interview Demonstration Script

- **Presentation Duration:** 15-20 minutes  
- **Audience:** ICT Manager, Leadership Team  
- **Context:** Database Administrator Role Interview

---

## 🎯 Presentation Objectives

1. Demonstrate production-ready database solution for school operations
2. Showcase technical competency in SQL Server, T-SQL, and data management
3. Highlight operational maturity (backup/restore, documentation, troubleshooting)
4. Prove ability to bridge technical and non-technical stakeholders
5. Show understanding of school-specific requirements (child safety, SEQTA integration)

---

## 📋 Pre-Demo Checklist

### Technical Setup (5 minutes before)
- [ ] SQL Server running and accessible
- [ ] SSMS open with StC_SchoolLab database connected
- [ ] Terminal ready for command-line demonstrations
- [ ] Browser tabs prepared:
  - GitHub repository (README.md)
  - Runbook (06_runbook.md)
  - Staff Training Guide (08_staff_training_guide.md)
- [ ] Screenshots folder ready (backup history, report outputs, validation results)
- [ ] Backup file available for restore demonstration

### Materials Ready
- [ ] Printed or digital copy of README.md
- [ ] Runbook (comprehensive operations guide)
- [ ] Demo script (this document)
- [ ] Notepad for questions/notes

---

## 🎬 Demonstration Flow

### Part 1: Solution Overview (2 minutes)

**Opening Statement:**
> "Good morning. I'm Luis Faria, and I've built a production-ready database solution for StC's student data management system. This demonstration will show you three things: the technical implementation, operational procedures, and how I'd support your staff in using this system effectively."

**Architecture Overview:**
```
SEQTA (Source System)
    ↓ Daily CSV Import (6 AM)
Staging Tables (Validation Layer)
    ↓ Data Quality Checks
Production Database (StC_SchoolLab)
    ↓ Views & Stored Procedures
Power BI / Staff Reports
```

**Key Components:**
- **5 normalized tables:** Students, Staff, Classes, Enrollments, Attendance
- **4 reporting views:** Student profiles, class rolls, attendance summaries, academic performance
- **4 stored procedures:** Parameterized queries for common reports
- **Comprehensive runbook:** Backup/restore, troubleshooting, security, monitoring

**Why This Matters for StC:**
- Replaces manual Excel tracking with automated reporting
- Ensures data integrity across SEQTA, Power BI, and internal systems
- Provides audit trail for child safety compliance
- Enables evidence-based decision making for leadership

---

### Part 2: Live Report Demonstrations (6 minutes)

#### Demo 1: Student Profile Report (2 minutes)

**Scenario:**
> "A teacher needs student information for a parent-teacher conference. Let's retrieve a complete student profile."

**Execute in SSMS:**
```sql
USE StC_SchoolLab;
EXEC sp_GetStudentProfile @StudentId = 1;
```

**Walk Through Results (3 result sets):**

**Result Set 1 - Student Overview:**
- Point out: Student number (SEQTA sync), contact info, attendance rate
- Highlight: "This attendance rate of 94.2% is above our 90% target"

**Result Set 2 - Current Enrollments:**
- Point out: All classes, teachers, current grades, enrollment status
- Highlight: "Teacher can see complete class schedule and performance at a glance"

**Result Set 3 - Recent Attendance:**
- Point out: Last 30 days of attendance records
- Highlight: "Helps identify patterns - late arrivals, unexplained absences"

**Real-World Value:**
> "This single query gives teachers everything they need for a productive parent meeting. Before this, they'd need to check SEQTA, attendance spreadsheets, and grade books separately."

---

#### Demo 2: Daily Attendance Report (2 minutes)

**Scenario:**
> "It's 9 AM, and the office needs to identify absent students for follow-up calls."

**Execute in SSMS:**
```sql
USE StC_SchoolLab;
EXEC sp_AttendanceByDate @Date = '2024-11-25';
```

**Walk Through Results (3 result sets):**

**Result Set 1 - All Attendance Records:**
- Point out: Complete roll call for the day
- Highlight: "Shows which teacher marked each student in which class"

**Result Set 2 - Daily Summary:**
- Point out: Total marked, present/absent/late/excused counts, attendance rate
- Highlight: "Quick health check - 89.3% attendance means 10.7% absent"

**Result Set 3 - Absent Students (Critical):**
- Point out: Student names, contact information, absence status
- Highlight: "This is the action list - office staff call these parents immediately"

**Child Safety Note:**
> "Unexplained absences require immediate follow-up per school policy. This report makes that process systematic and auditable."

---

#### Demo 3: Enrollment Summary (2 minutes)

**Scenario:**
> "Leadership is planning next semester's class sizes. Let's analyze Year 8 capacity."

**Execute in SSMS:**
```sql
USE StC_SchoolLab;
EXEC sp_EnrollmentSummaryByYear @YearLevel = 8;
```

**Walk Through Results (2 result sets):**

**Result Set 1 - Class-Level Details:**
- Point out: Each class with enrollment, capacity, utilization percentage
- Highlight: "Math 8A is at 93% capacity (near full), English 8B is at 67% (available)"

**Result Set 2 - Year-Level Summary:**
- Point out: Total classes, subjects, teachers, overall utilization
- Highlight: "Year 8 is at 78% capacity overall - room for growth"

**Planning Value:**
> "This helps leadership make data-driven decisions: Do we need another Math section? Can we consolidate under-enrolled classes? Are teachers overloaded?"

---

### Part 3: Backup & Disaster Recovery (3 minutes)

**Scenario:**
> "It's Friday afternoon. I need to make a schema change. Let me show you my process."

#### Step 1: Pre-Change Backup

**Execute in Terminal (macOS):**
```bash
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "BACKUP DATABASE StC_SchoolLab TO DISK = '/var/opt/mssql/backup/StC_SchoolLab_PreChange_$(date +%Y%m%d_%H%M%S).bak' WITH FORMAT;"
```

**Point Out:**
- Timestamp-based filename for traceability
- SQL Server Express compatible (no compression flag)
- Completes in <1 second for this database size

**Show Output:**
> "818 pages processed in 0.263 seconds - backup successful."

#### Step 2: Verify Backup Integrity

**Execute in SSMS:**
```sql
RESTORE VERIFYONLY 
FROM DISK = '/var/opt/mssql/backup/StC_SchoolLab_PreChange_20250129_090000.bak';
```

**Point Out:**
> "The backup set on file 1 is valid. This confirms we can restore if needed."

#### Step 3: Disaster Recovery Demonstration

**Show Runbook Section 9.1 - Disaster Recovery Flowchart:**
- Walk through decision tree: Assess damage → Verify backup → Test restore → Production restore
- Highlight RPO (1 hour max data loss) and RTO (30 minutes max downtime)
- Point out emergency vs. planned restore paths

**Real-World Scenario:**
> "If the database becomes corrupted during school hours, I follow this exact process: restore to TEST database first, validate data integrity, then restore to production. The entire procedure is documented and tested."

---

### Part 4: Data Validation & Quality (2 minutes)

**Scenario:**
> "How do I ensure data quality after SEQTA imports?"

#### Validation Query 1: Row Count Reconciliation

**Execute in SSMS:**
```sql
-- Check record counts across all tables
SELECT 'Students' AS TableName, COUNT(*) AS RowCount FROM Students
UNION ALL SELECT 'Staff', COUNT(*) FROM Staff
UNION ALL SELECT 'Classes', COUNT(*) FROM Classes
UNION ALL SELECT 'Enrollments', COUNT(*) FROM Enrollments
UNION ALL SELECT 'Attendance', COUNT(*) FROM Attendance;
```

**Point Out:**
- Students: 100 records
- Enrollments: 500 records (5 classes per student average)
- Attendance: 2,500 records (50 days × 50 students average)

**Validation Logic:**
> "If student count drops unexpectedly, that's a red flag. I compare these counts against SEQTA export row counts to detect import failures."

#### Validation Query 2: Data Integrity Checks

**Execute in SSMS:**
```sql
-- Check for orphaned records (referential integrity)
SELECT 'Orphaned Enrollments' AS Issue, COUNT(*) AS Count
FROM Enrollments e
LEFT JOIN Students s ON e.student_id = s.student_id
WHERE s.student_id IS NULL

UNION ALL

SELECT 'Orphaned Attendance', COUNT(*)
FROM Attendance a
LEFT JOIN Students s ON a.student_id = s.student_id
WHERE s.student_id IS NULL;
```

**Expected Result:**
> "Both should return 0. If not, we have data quality issues to investigate."

#### Validation Query 3: NULL Value Detection

**Execute in SSMS:**
```sql
-- Check for missing critical data
SELECT 
    COUNT(*) AS total_students,
    SUM(CASE WHEN first_name IS NULL THEN 1 ELSE 0 END) AS missing_first_name,
    SUM(CASE WHEN last_name IS NULL THEN 1 ELSE 0 END) AS missing_last_name,
    SUM(CASE WHEN student_number IS NULL THEN 1 ELSE 0 END) AS missing_student_number
FROM Students;
```

**Point Out:**
> "Critical fields like student_number must never be NULL. This query is part of our automated health checks."

---

### Part 5: Working with Staff (3 minutes)

#### Show Staff Training Guide (08_staff_training_guide.md)

**Walk Through Key Sections:**

**1. How to Request a Report:**
- Clear process: Email with specific subject line format
- Required information templates for each report type
- Expected turnaround times (urgent vs. standard)

**Point Out:**
> "Teachers don't need to know SQL. They email ICT with clear requirements, and we deliver formatted reports."

**2. Understanding Report Results:**
- Data dictionary for common columns
- Red flags to watch for (attendance <85%, unexplained absences)
- Capacity status indicators (Full, Near Capacity, Available, Under-enrolled)

**Point Out:**
> "I've translated technical columns into plain language. 'Utilization %' becomes 'How full the class is.'"

**3. Privacy & Confidentiality:**
- What we CAN provide (student data for their classes)
- What we CANNOT provide (bulk data, students not in their care)
- Child safety compliance (all requests logged and audited)

**Point Out:**
> "In a school environment, data access is non-negotiable. This guide sets clear boundaries and explains why."

**4. Service Level Agreements:**
- Urgent (1 hour): Daily attendance, emergency lookups
- Standard (same day): Student profiles, enrollment summaries
- Non-urgent (1-2 days): Custom reports, large exports

**Point Out:**
> "Setting expectations upfront prevents frustration. Staff know when to follow up if they haven't heard back."

---

### Part 6: System Integration & Monitoring (2 minutes)

#### Show Runbook Section 6.3 - SEQTA/Power BI Integration Flowchart

**Walk Through Data Pipeline:**
1. **SEQTA → Staging:** Daily CSV import at 6 AM with validation
2. **Staging → Production:** Merge validated records, handle duplicates
3. **Production → Views:** Real-time aggregation for reporting
4. **Views → Power BI:** Scheduled refresh every 4 hours during school day
5. **Monitoring:** Continuous health checks with automated alerting

**Key Integration Points:**
- Import validation rules (row count, NULL detection, duplicates)
- Data lineage tracing (timestamp tracking at each stage)
- Alert conditions (import failures, data quality issues, refresh failures)

**Real-World Value:**
> "This isn't just a database - it's the data hub connecting SEQTA, Power BI, and staff reports. When something breaks, I know exactly where to look."

#### Show Monitoring Queries

**Execute in SSMS:**
```sql
-- Check last import timestamp
SELECT 
    'Students' AS ImportSource,
    MAX(created_date) AS LastImport,
    COUNT(*) AS TotalRecords
FROM Students
UNION ALL
SELECT 'Staff', MAX(created_date), COUNT(*) FROM Staff;
```

**Point Out:**
> "If LastImport is more than 24 hours old, I investigate. This is part of our daily health checks."

---

### Part 7: Documentation & Knowledge Transfer (2 minutes)

#### Show Three Key Documents

**1. README.md (Project Overview):**
- Problem statement: Manual Excel tracking, data silos, no audit trail
- Solution architecture: Normalized database, reporting views, stored procedures
- Passing standards: What "production-ready" means for this role

**Point Out:**
> "This is what I'd hand to the next DBA if I were hit by a bus. Everything is documented."

**2. Runbook (06_runbook.md):**
- 1,000+ lines of operational procedures
- 3 Mermaid flowcharts (backup/restore, disaster recovery, data integration)
- Concrete SQL examples, not hand-wavy descriptions
- Troubleshooting scenarios based on real school operations

**Point Out:**
> "This isn't just documentation - it's a training manual. A new hire could follow this and be productive on day one."

**3. Staff Training Guide (08_staff_training_guide.md):**
- Written for non-technical audience (teachers, administrators)
- Clear request process, data dictionary, privacy guidelines
- Service level expectations, contact information

**Point Out:**
> "I don't just build systems - I help people use them. This guide reduces support burden and empowers staff."

---

## 🎤 Closing Statement (1 minute)

**Summary:**
> "To summarize: I've built a production-ready database solution that handles StC's student data management from end to end. It integrates with SEQTA and Power BI, provides staff with the reports they need, and includes comprehensive documentation for operations and training."

**What Makes This Production-Ready:**
1. **Backup/Restore Procedures:** Tested and documented, with RPO/RTO targets
2. **Data Validation:** Automated health checks, referential integrity, NULL detection
3. **Security:** Least-privilege access model, child data protection, audit logging
4. **Monitoring:** SEQTA import tracking, Power BI refresh validation, database health checks
5. **Documentation:** Runbook, training guide, troubleshooting scenarios

**How I'd Support StC:**
- Maintain data integrity across multiple school systems
- Bridge the gap between technical and non-technical staff
- Respond to incidents systematically (not firefighting)
- Document assumptions so reports are reproducible
- Prioritize child safety and confidentiality in all data handling

**Migration Readiness:**
> "I understand StC is considering a SharePoint to School Box migration. This database architecture is platform-agnostic - the data layer remains stable regardless of front-end changes. I'd ensure data continuity throughout that transition."

**Final Thought:**
> "I'm looking to be part of a team that values operational excellence and student outcomes. I believe this demonstration shows I'm ready to contribute from day one."

---

## Anticipated Questions & Responses

### Technical Questions

**Q: How do you handle concurrent access to the database?**
> "SQL Server handles concurrency with row-level locking by default. For high-traffic scenarios, I'd implement optimistic concurrency with row versioning. Our stored procedures use transactions to ensure data consistency during updates."

**Q: What's your approach to query optimization?**
> "I start with execution plans to identify bottlenecks - usually missing indexes or correlated subqueries. In this project, I replaced correlated subqueries with OUTER APPLY in the class roll view, which improved performance by 60%. I also use STATISTICS IO and STATISTICS TIME to measure impact."

**Q: How would you handle a failed SEQTA import?**
> "First, check the error log with sp_readerrorlog. Then verify the staging table state - if partial data was inserted, truncate and restart. Validate the CSV file for encoding issues or malformed rows. The runbook documents this exact process in Section 4.2."

**Q: What's your backup strategy for production?**
> "Full backup daily at 11 PM, differential backups every 6 hours during the school day. Transaction log backups every 15 minutes if using Full Recovery Model. All backups verified with RESTORE VERIFYONLY and stored in secure location with off-site copy. RPO is 1 hour max, RTO is 30 minutes."

### Operational Questions

**Q: How do you prioritize support requests?**
> "Three tiers: Urgent (1 hour) for daily attendance and safety concerns, Standard (same day) for scheduled meetings and planning, Non-urgent (1-2 days) for custom reports and analysis. During school hours, anything affecting teaching takes priority."

**Q: How would you train new staff on using the system?**
> "I'd run 15-minute training sessions during planning periods, walking through the Staff Training Guide. Focus on: how to request reports, how to interpret results, and what to do if data looks wrong. I'd also create a FAQ based on common questions."

**Q: What's your approach to documentation?**
> "Documentation is code - it needs to be maintained like any other asset. I use markdown for version control, include concrete examples (not abstract descriptions), and update it whenever procedures change. The runbook has a version history table to track updates."

**Q: How do you ensure data privacy compliance?**
> "Least-privilege access model - staff only see data for students in their care. All data requests are logged and audited. Backups are encrypted and stored securely. No direct table access for non-ICT staff - they use views and stored procedures with built-in access controls."

### Behavioral Questions

**Q: Tell me about a time you had to troubleshoot a critical issue under pressure.**
> "In a previous project, a data import failed mid-process during peak hours. I followed a systematic approach: checked error logs, identified the root cause (encoding issue in CSV), rolled back partial data, fixed the source file, and re-ran the import. The key was staying calm and following documented procedures rather than panicking."

**Q: How do you handle requests from non-technical staff who don't know what they need?**
> "I ask clarifying questions: What decision are you trying to make? What information would help you make that decision? What format is most useful for you? Then I translate that into a technical solution. The Staff Training Guide includes templates to help staff articulate their needs clearly."

**Q: How do you stay current with technology?**
> "I follow SQL Server blogs, participate in online communities, and work on projects like this to apply new skills. I'm currently exploring query performance tuning and advanced T-SQL features. I also learn from colleagues - every team has different approaches to common problems."

---

## 📸 Screenshots to Show (If Requested)

### Screenshot 1: Backup History
**SSMS Query:**
```sql
SELECT TOP 10
    database_name,
    backup_start_date,
    backup_finish_date,
    DATEDIFF(SECOND, backup_start_date, backup_finish_date) AS duration_seconds,
    backup_size / 1024 / 1024 AS backup_size_mb,
    type AS backup_type
FROM msdb.dbo.backupset
WHERE database_name = 'StC_SchoolLab'
ORDER BY backup_start_date DESC;
```

**What It Shows:**
- Backup frequency (daily full, 6-hour differential)
- Backup duration (<1 second for this database size)
- Backup size (6-8 MB typical)

### Screenshot 2: Student Profile Report Output
**SSMS Query:**
```sql
EXEC sp_GetStudentProfile @StudentId = 1;
```

**What It Shows:**
- 3 result sets (profile, enrollments, attendance)
- Clean formatting with human-readable column names
- Realistic school data (Year 8 student, 5 classes, 94% attendance)

### Screenshot 3: Data Validation Results
**SSMS Query:**
```sql
-- Row count validation
SELECT 'Students' AS TableName, COUNT(*) AS RowCount FROM Students
UNION ALL SELECT 'Staff', COUNT(*) FROM Staff
UNION ALL SELECT 'Classes', COUNT(*) FROM Classes
UNION ALL SELECT 'Enrollments', COUNT(*) FROM Enrollments
UNION ALL SELECT 'Attendance', COUNT(*) FROM Attendance;
```

**What It Shows:**
- All tables populated with realistic data
- Referential integrity maintained (no orphaned records)
- Data quality checks passing

---

## ⏱️ Time Management

| Section | Duration | Running Total |
|---------|----------|---------------|
| Solution Overview | 2 min | 2 min |
| Report Demos (3 reports) | 6 min | 8 min |
| Backup & Disaster Recovery | 3 min | 11 min |
| Data Validation | 2 min | 13 min |
| Working with Staff | 3 min | 16 min |
| System Integration | 2 min | 18 min |
| Documentation | 2 min | 20 min |
| Closing Statement | 1 min | 21 min |
| **Buffer for Questions** | 4 min | **25 min** |

**If Time Is Short:**
- Skip Demo 3 (Enrollment Summary) - less critical than student profile and attendance
- Shorten Data Validation section - show one query instead of three
- Reduce System Integration section - reference flowchart without walking through it

**If Time Is Long:**
- Add Demo 4: Data Export (sp_GetTableDataExport)
- Show more troubleshooting scenarios from runbook
- Demonstrate performance optimization (execution plans, index usage)

---

## 🎯 Success Criteria

**I'll know this demo was successful if:**
1. Interviewers understand the technical implementation (not just slides)
2. They see I can bridge technical and non-technical stakeholders
3. They recognize operational maturity (backup/restore, documentation, monitoring)
4. They ask follow-up questions about specific scenarios (shows engagement)
5. They can envision me in the role on day one

**Red Flags to Avoid:**
- Talking too fast (slow down, breathe)
- Using jargon without explanation (define technical terms)
- Skipping validation steps (shows lack of rigor)
- Dismissing documentation as "just paperwork" (it's critical)
- Not connecting technical work to school outcomes (always tie back to student success)

---