# Level 3: Production Mindset Assessment

**Outcome:** "Safe, documents well, and supports staff."

This level focuses on production-ready practices, including backup and recovery procedures, data validation, operational documentation, staff training, and interview presentation readiness.

## 🎯 Level 3 Overview: Deploy and Maintain a Production System

Demonstrates the ability to implement production-grade practices, including:
- Comprehensive operational documentation (runbook with flowcharts)
- Systematic troubleshooting procedures for real-world scenarios
- Non-technical staff training and support materials
- Interview-ready presentation with live demonstrations
- Data validation, security, and compliance protocols

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

**File Location:** `docs/Assessment3/06_runbook.md` (1,000+ lines, comprehensive operational guide)

**Visual Documentation:**
- 3 Mermaid flowcharts: Backup/Restore decision tree, Disaster Recovery steps, SEQTA/Power BI integration flow
- Color-coded decision paths (emergency: red, success: green, monitoring: yellow)
- End-to-end data pipeline visualization

---

## **Task 2: Troubleshooting Scenarios**

### **What I've Done:**
Documented 5 real-world troubleshooting scenarios with systematic resolution procedures, integrated into the operational runbook (Section 4: Common Incidents & Troubleshooting).

### **Why It Matters:**
School operations depend on reliable data systems. When issues occur during critical periods (morning roll call, parent meetings, semester planning), staff need clear, tested procedures to resolve problems quickly. Systematic troubleshooting reduces downtime and prevents ad-hoc "firefighting" that leads to mistakes.

### **Key Implementation Details:**

**1. Report Numbers Don't Match (Section 4.1):**
- Scenario: Attendance report shows different totals than SEQTA
- Troubleshooting: Date range verification, duplicate detection, status code validation, row count comparison
- Resolution: Document discrepancies, identify root cause (import timing, data transformation), reconcile with source system

**2. Import Failed Halfway (Section 4.2):**
- Scenario: SEQTA CSV import fails mid-process, leaving partial data
- Troubleshooting: Error log review, staging table state verification, rollback partial import, CSV validation
- Prevention: Use transactions for imports, validate CSV structure before import, log progress, keep original files

**3. Duplicate Student Records (Section 4.3):**
- Scenario: Same student appears multiple times with different IDs
- Troubleshooting: Identify duplicates by name/DOB, review related records, merge strategy with foreign key reassignment
- Prevention: Add unique constraint on student_number, implement validation rules
- **Critical Note:** Always backup database before merging records

**4. Performance Issue on Report Query (Section 4.4):**
- Scenario: Report takes >30 seconds to run, staff complaining about slow response
- Troubleshooting: Execution plan analysis, missing index detection, query statistics, optimization techniques
- Performance Targets: Simple lookups <1 sec, aggregated reports <5 sec, complex analytics <30 sec

**5. Missing Data in Power BI Reports (Section 4.5):**
- Scenario: Power BI dashboard shows blank/NULL values for recent data
- Troubleshooting: Verify source data, check view definitions, validate Power BI refresh, trace data lineage
- Common Causes: Scheduled refresh failed, view filter excludes recent data, data type mismatch, permissions issue

**File Location:** Integrated into `docs/Assessment3/06_runbook.md` (Section 4, lines 317-549)

---

## **Task 3: Training Materials for Non-Technical Staff**

### **What I've Done:**
Created a comprehensive staff training guide tailored for teachers, administrators, and leadership - written in plain language with clear processes, templates, and expectations.

### **Why It Matters:**
Database systems are only valuable if staff can use them effectively. Teachers and administrators need student data for parent meetings, roll call, and planning - but they shouldn't need to know SQL or database concepts. Clear training materials reduce support burden, empower staff, and ensure data requests are specific and actionable.

### **Key Implementation Details:**

**1. Quick Reference Guide:**
- 4 report types with typical turnaround times (same day, 1 hour, 1-2 days)
- Clear request process: Email format, subject line template, required information
- Decision matrix: Which report for which purpose

**2. Request Templates:**
- Student Profile: Name, student number, purpose, date range
- Attendance Reports: Date required, year level, purpose
- Enrollment Summaries: Year level, purpose, specific classes
- Custom Exports: Data needed, filters, format, deadline

**3. Understanding Report Results:**
- Data dictionary for common columns (plain language explanations)
- Student Profile: 3 result sets explained (overview, enrollments, attendance)
- Attendance Report: Red flags to watch for (attendance <85%, unexplained absences)
- Enrollment Summary: Capacity status indicators (Full, Near Capacity, Available, Under-enrolled)

**4. Privacy & Confidentiality:**
- What we CAN provide: Student data for their classes, aggregated class data, attendance summaries
- What we CANNOT provide: Students not in their care, bulk contact info, sensitive medical notes
- Child Safety Compliance: All requests logged and audited, legitimate educational purpose required

**5. Service Level Agreements:**
- **Urgent (1 hour):** Daily attendance, emergency lookups, critical system issues
- **Standard (same day):** Student profiles, enrollment summaries, routine exports
- **Non-urgent (1-2 days):** Custom reports, large exports, historical data

**6. Tips for Better Reports:**
- Do's: Be specific, provide context, use student numbers, plan ahead
- Don'ts: Request unnecessary data, share credentials, export to personal devices, modify data

**7. Issue Reporting:**
- How to report data discrepancies (with example email template)
- When to request training sessions (15-minute walkthroughs)
- How to suggest improvements (feedback welcome)

**File Location:** `docs/Assessment3/08_staff_training_guide.md` (265 lines, non-technical audience)

---

## **Task 4: Presentation Script for Interview Demo**

### **What I've Done:**
Created a comprehensive 15-20 minute demonstration script with live SQL examples, talking points, anticipated Q&A, and time management guidelines for the Database Administrator role interview.

### **Why It Matters:**
Technical competency alone doesn't land jobs - you need to communicate value clearly, demonstrate operational maturity, and show you understand the business context. This script ensures I cover all critical points systematically while staying within time constraints and handling questions confidently.

### **Key Implementation Details:**

**1. Presentation Structure (7 Parts):**
- **Part 1 (2 min):** Solution overview, architecture diagram, key components, why it matters for StC
- **Part 2 (6 min):** Live report demos - Student Profile, Daily Attendance, Enrollment Summary
- **Part 3 (3 min):** Backup & disaster recovery - Pre-change backup, verification, restore process
- **Part 4 (2 min):** Data validation - Row counts, referential integrity, NULL detection
- **Part 5 (3 min):** Working with staff - Training guide walkthrough, privacy compliance
- **Part 6 (2 min):** System integration - SEQTA/Power BI pipeline, monitoring queries
- **Part 7 (2 min):** Documentation showcase - README, runbook, training guide

**2. Live Demonstration Queries:**
- All SQL queries copy-paste ready for SSMS execution
- Expected outputs documented for each query
- Real-world scenarios tied to school operations
- Talking points for each result set

**3. Backup/Restore Demonstration:**
```bash
# Pre-change backup with timestamp
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "BACKUP DATABASE StC_SchoolLab TO DISK = '/var/opt/mssql/backup/StC_SchoolLab_PreChange_$(date +%Y%m%d_%H%M%S).bak' WITH FORMAT;"

# Verify backup integrity
RESTORE VERIFYONLY FROM DISK = '/var/opt/mssql/backup/StC_SchoolLab_PreChange_20250129_090000.bak';
```

**4. Anticipated Questions & Responses:**
- **Technical:** Concurrent access, query optimization, failed imports, backup strategy
- **Operational:** Support request prioritization, staff training, documentation maintenance, data privacy
- **Behavioral:** Troubleshooting under pressure, handling non-technical requests, staying current

**5. Time Management:**
- Section durations with running totals
- Buffer for questions (4 minutes)
- Flexibility guidance (what to skip if time is short, what to add if time is long)

**6. Success Criteria:**
- Interviewers understand technical implementation
- They see ability to bridge technical/non-technical stakeholders
- They recognize operational maturity
- They can envision me in the role on day one

**7. Red Flags to Avoid:**
- Talking too fast, using jargon without explanation
- Skipping validation steps, dismissing documentation
- Not connecting technical work to school outcomes

**File Location:** `docs/Assessment3/07_demo_script.md` (650+ lines, interview-ready presentation)

---

## **Task 5: Screenshot Capture Queries**

### **What I've Done:**
Created a comprehensive SQL script with 12 screenshot-ready queries for demonstration purposes, complete with expected outputs, capture tips, and presentation order recommendations.

### **Why It Matters:**
Visual evidence is more compelling than verbal descriptions. Screenshots show the system actually works, data is realistic, and procedures are tested - not just theoretical. They also serve as backup if live demos fail during the interview.

### **Key Screenshot Queries:**

**1. Backup History:**
- Shows backup frequency, duration, size, type
- Demonstrates operational maturity and backup procedures

**2. Student Profile Report (3 Result Sets):**
- Complete student information for parent-teacher conferences
- Shows stored procedure functionality and data integration

**3. Daily Attendance Report (3 Result Sets):**
- Roll call verification and absence follow-up
- Demonstrates child safety compliance and operational reporting

**4. Enrollment Summary Report (2 Result Sets):**
- Class capacity planning and resource allocation
- Shows leadership decision support and data-driven planning

**5. Data Validation - Row Count Reconciliation:**
- Data quality checks and referential integrity
- Demonstrates systematic validation and operational rigor

**6. Data Validation - Referential Integrity Check:**
- No orphaned records, foreign key integrity maintained
- Shows data quality assurance

**7. Data Validation - NULL Value Detection:**
- Critical fields populated, data completeness verified
- Demonstrates data quality monitoring

**8. System Integration - SEQTA Import Monitoring:**
- Last import timestamp, data freshness
- Shows integration monitoring and data pipeline health

**9. Database Health - Space Usage:**
- Database size, growth trends
- Demonstrates capacity planning and resource monitoring

**10. Performance Monitoring - View Execution:**
- Reporting views accessible and performant
- Shows system health and query optimization

**11. Security - User Permissions Audit:**
- Least-privilege access model, role-based security
- Demonstrates child data protection and compliance

**12. Backup Verification:**
- Backup integrity validation with RESTORE VERIFYONLY
- Shows disaster recovery readiness

**Screenshot Capture Tips:**
- Use SSMS "Results to Grid" mode for clean formatting
- Adjust column widths for readability before capturing
- Include query text in screenshot (shows what was executed)
- Use consistent SSMS theme across all screenshots
- Save as PNG/JPG with high resolution (1920x1080 minimum)
- Name files descriptively: "01_backup_history.png", "02_student_profile.png"

**Recommended Presentation Order:**
1. Student Profile Report (core functionality)
2. Daily Attendance Report (child safety compliance)
3. Enrollment Summary Report (leadership decision support)
4. Backup History (operational maturity)
5. Data Validation - Row Counts (data quality)
6. Data Validation - Referential Integrity (technical rigor)

**File Location:** `docs/Assessment3/09_screenshot_queries.sql` (350+ lines, 12 demonstration queries)

---

## **Assessment 3 Summary: Production Mindset Complete**

### **Deliverables Completed:**
1. ✅ **Operational Runbook** (`06_runbook.md`) - 1,000+ lines with 3 Mermaid flowcharts
2. ✅ **Troubleshooting Scenarios** - 5 real-world scenarios integrated into runbook
3. ✅ **Staff Training Guide** (`08_staff_training_guide.md`) - 265 lines, non-technical audience
4. ✅ **Presentation Script** (`07_demo_script.md`) - 650+ lines, interview-ready demo
5. ✅ **Screenshot Queries** (`09_screenshot_queries.sql`) - 12 demonstration queries

### **What This Demonstrates:**
- **Operational Maturity:** Backup/restore procedures, disaster recovery, monitoring
- **Technical Competency:** SQL Server, T-SQL, query optimization, data validation
- **Stakeholder Communication:** Training materials, documentation, presentation skills
- **Production Readiness:** Security, compliance, change management, knowledge transfer
- **School Context Understanding:** Child safety, SEQTA integration, staff support

### **Interview "Showcase Pack":**
1. **README.md** - Project overview, problem statement, solution architecture
2. **Runbook** - Comprehensive operations guide with flowcharts
3. **Demo Script** - Structured presentation with live examples
4. **Training Guide** - Non-technical staff support documentation
5. **Screenshots** - Visual evidence of working system

### **Passing Standards Met:**
1. ✅ "I always confirm backups and restore capability before changes."
2. ✅ "I document assumptions so reports are reproducible."
3. ✅ "In a school environment, confidentiality and access control are non-negotiable."
4. ✅ "I can help bridge the gap between technical and non-technical staff."
5. ✅ "I understand how to maintain data integrity across multiple school systems."

**Status:** Assessment 3 complete and interview-ready. All documentation production-grade and ready for presentation.