# Learning SQL Server the Hard Way: 16 Days of Real-World Database Work

#sql #sqlserver #database #dataengineering #portfolio
**From "I've never used SQL Server" to "Here's my 1,000-line operational runbook": How I turned a job opportunity into a portfolio-building sprint.**

> *Hard work is my preferred language and I try to speak it fluently.*

---

## 🎯 The Opportunity 
### When "I Don't Know SQL Server" Becomes a Challenge

A friend reached out with an intriguing proposition: *"Do you work with Microsoft SQL Server? We're desperate to fill a school data administrator role."*

My honest answer? **No—but I know databases.**

My background spans PostgreSQL, MySQL, MongoDB, and GraphQL. I've built ETL pipelines, optimized queries, designed schemas, and managed production data systems. The fundamentals are universal: normalization, indexing, backup strategies, referential integrity, stored procedures.

SQL Server syntax? Just a dialect I hadn't learned yet.

But here's the thing about job opportunities in unfamiliar territory: **saying "I can learn it" isn't enough.** Hiring managers hear that every day. What they want is proof.

### The Real Challenge

> **Can I go from zero SQL Server experience to interview-ready in two weeks, with portfolio-quality deliverables to prove it?**

This wasn't just about learning T-SQL syntax. The role required:
- Managing school data systems (student records, attendance, class scheduling)
- Running reports for leadership and teaching staff
- Integrating data from legacy systems like SEQTA and Synergetic
- Maintaining backup/recovery procedures
- Documenting operations for non-technical staff
- Operating responsibly with child-safety-sensitive data

**The approach:** Treat it like a master's assignment. I've spent months tackling academic projects with a disciplined workflow: *Receive Brief → Research → Design → Build → Document → Present → NEXT.* Why not leverage that momentum?

This is where strategic use of LLMs came into play. Instead of aimlessly "learning SQL Server," I needed a structured challenge that would simulate real-world job responsibilities.

### The Prompt That Launched the Project

The prompt:

> *"I need to demonstrate enterprise-level SQL Server skills for a school data administrator role. Create a comprehensive 3-level assessment covering: (1) database fundamentals and backup/restore, (2) reporting and data integration, (3) operational documentation and training. Structure it like an internal deliverable with real-world scenarios matching school systems like SEQTA and Synergetic."*

---

## The Problem

Build a "School Data Platform" on SQL Server, documented like an internal deliverable. *Do the deed and show the proof*.

The structure emerged as a 3-level assessment simulation `(Level 1 → Level 2 → Level 3)`, matching exactly what the role calls for:

| Assessment Level | Focus Area | Real-World Equivalent |
|-----------------|------------|----------------------|
| **Level 1** | Database Fundamentals | "Won't break production" |
| **Level 2** | Data Integration & Reporting | "Can generate reports and move data between systems" |
| **Level 3** | Production Operations | "Documents well, trains staff, operates safely" |

📦 [StC DataLab Repo](https://github.com/lfariabr/stc-datalab)

---

## Execution Plan (Dec 2025 - Jan 2026)

| Date | Focus | Deliverables | Status |
|------|-------|-------------|----|
| **Dec 20-21** | Setup & Schema | SQL Server Express + SSMS installation, DB creation, table structure | ✅ |
| **Dec 22-23** | Backup & Restore | Full backup/restore procedures, documentation with screenshots | ✅ |
| **Dec 24-25** | Data Generation | Realistic seed data with edge cases | ✅ |
| **Dec 26-27** | Reporting Views | Student profiles, class rolls, attendance summaries | ✅ |
| **Dec 28-29** | Stored Procedures | Parameter-based queries, optimization | ✅ |
| **Dec 30-31** | Import/Export | CSV handling, staging tables, data validation | ✅ |
| **Jan 1-2** | Runbook & Documentation | Operational procedures, troubleshooting guide | ✅ |
| **Jan 3-4** | Demo Preparation | Presentation script, screenshots, talking points | ✅ |
| **Jan 5** | Final Review | Validate all components, practice demo | ✅ |

> [Complete changelog with 30+ commits](https://github.com/search?q=repo%3Alfariabr%2Fmasters-swe-ai++stc+OR+%28stc%29+OR+std+OR+%28std%29&type=commits&s=committer-date&o=desc)

---

## 🤖 The Solution
### Building an Enterprise Data Infrastructure

What started as "learn SQL Server syntax" evolved into a complete operational simulation. Here's what I built:

### System Architecture

![Mermaid Diagram with Data Flow](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/szt4gnqj361vgjgkydvl.png)

[See it in full size](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-Extra/stc_datalab/screenshots/ArchitectureOverview.jpeg)

### **Database Architecture**

The foundation is a normalized relational database representing a school's core operational data:

**Core Tables (6):**
- **Students** (200 records) — Privacy-sensitive fields including medical info, emergency contacts, and boarding status
- **Staff** (20 records) — Role-based attributes (Teacher, Principal, ICT, Admin, Counselor)
- **Subjects** (12 records) — Curriculum structure covering Math, English, Science, Humanities, Arts, Technology
- **Classes** (30 records) — Teacher assignments, room scheduling, year level groupings
- **Enrollments** (500 records) — Student-class relationships with status tracking (Active, Withdrawn, Completed, Pending)
- **Attendance** (800 records) — Daily tracking with status codes (Present, Absent, Late, Excused) across 10 days

**Design Principles:**
```sql
-- Example: Students table with constraints
CREATE TABLE Students (
    student_id INT IDENTITY(1,1) PRIMARY KEY,
    student_number NVARCHAR(20) UNIQUE NOT NULL,
    first_name NVARCHAR(50) NOT NULL,
    medical_info NVARCHAR(500), -- Privacy sensitive
    emergency_contact NVARCHAR(100),
    enrollment_year INT NOT NULL,
    INDEX idx_enrollment_year (enrollment_year),
    INDEX idx_student_number (student_number)
);
```

### **Operational Features**

**1. Reporting Views (4 core views)**
- `vw_StudentProfile` — Complete student records with emergency contacts
- `vw_ClassRoll` — Daily attendance with class lists and teacher assignments
- `vw_AttendanceDaily` — Roll call summaries with absence follow-up contacts
- `vw_EnrollmentSummary` — Class capacity planning with utilization metrics

**2. Stored Procedures (4 parameterized)**
- `sp_GetStudentProfile` — Multi-result set with profile + enrollments + attendance
- `sp_EnrollmentSummaryByYear` — Year-level filtering with capacity indicators
- `sp_AttendanceByDate` — Date range queries for specific time periods
- `sp_GetTableDataExport` — Generic data export for Power BI integration

**3. Data Integration Pipeline**
- CSV import staging tables with validation rules
- Referential integrity checks before production load
- Error logging and rollback procedures
- Export functionality for SEQTA/Power BI sync

**4. Backup & Recovery**
- Full backup T-SQL scripts (SQL Server Express compatible)
- Differential backup procedures
- Three-stage restore validation (verify → test → production)
- RPO: 1 hour | RTO: 30 minutes

### **How It Works in Practice**

**Scenario 1: Morning Roll Call**
```sql
-- Teacher logs in at 8:45 AM, needs today's class roll
EXEC sp_AttendanceByDate 
    @StartDate = '2025-01-22', 
    @EndDate = '2025-01-22';
-- Returns: Student list with attendance status, emergency contacts for absences
```

**Scenario 2: Semester Planning**
```sql
-- Leadership needs Year 7 enrollment metrics for 2026 planning
EXEC sp_EnrollmentSummaryByYear @EnrollmentYear = 2026;
-- Returns: Class utilization, capacity warnings, subject distribution
```

**Scenario 3: System Integration**
```sql
-- SEQTA export runs daily at 6 AM, imports new attendance data
-- 1. Load CSV into staging table
-- 2. Validate referential integrity (all student_ids exist)
-- 3. Merge into production Attendance table
-- 4. Log success/failures for monitoring
```

### **Data Quality by Design**

Intentional edge cases throughout the seed data:
- **NULL values** — Missing phone numbers (9%), NULL emergency contacts
- **Casing inconsistencies** — Lowercase first names, uppercase emails, trailing spaces
- **International scenarios** — Singapore/Jakarta addresses for boarding students
- **Duplicate data** — Shared email addresses to test deduplication logic
- **Invalid formats** — Phone numbers marked as '???', incomplete grades ('INC')

This messy data simulates real school system exports (SEQTA, Synergetic) where cleaning and validation are critical.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Database** | SQL Server 2022 Express | On-premise simulation (macOS via Docker) |
| **Management** | SSMS + sqlcmd CLI | GUI and scripted operations |
| **Data Generation** | T-SQL CTEs + temp tables | Deterministic seed data with edge cases |
| **Backup** | Native SQL Server backups | Full/differential with RPO/RTO targets |
| **Integration** | CSV imports via BULK INSERT | Simulates SEQTA/Synergetic exports |
| **Documentation** | Markdown + Mermaid | Runbooks, training guides, flowcharts |

**Project Structure:**
```
stc_datalab/
├── sql/
│   ├── 00_create_db.sql          # Initial database creation
│   ├── 01_schema.sql             # Tables, constraints, indexes
│   ├── 02_seed_data.sql          # 1,500+ records with edge cases
│   ├── 03_views.sql              # 4 reporting views
│   ├── 04_stored_procedures.sql  # 4 parameterized SPs
│   ├── 05_import_export.sql      # CSV integration logic
│   └── 07_backup_restore.sql     # Backup/recovery procedures
├── data/
│   ├── students_import.csv       # Sample import data
│   ├── classes_import.csv
│   └── enrollments_import.csv
├── docs/
│   ├── Assessment1/              # Level 1: Setup & basics
│   ├── Assessment2/              # Level 2: Integration
│   └── Assessment3/              # Level 3: Operations
│       ├── 06_runbook.md         # 1,000+ line operational guide
│       ├── 07_demo_script.md     # Interview presentation
│       └── 08_staff_training_guide.md
└── screenshots/                  # 15+ annotated screenshots
```

---

## The Impact: Confidence Through Deliverables

This wasn't just practice—it was portfolio-building with interview-ready artifacts:

| Metric | Result |
|--------|--------|
| **Technical documentation** | 3,000+ lines across 15 files |
| **SQL scripts** | 10 files, 800+ lines of T-SQL |
| **Seed data generated** | 1,562 records across 6 tables |
| **Views & procedures** | 8 reusable database objects |
| **Operational runbook** | 1,000+ lines with flowcharts |
| **Training materials** | Non-technical staff guide |
| **Time investment** | 16 days, committed execution |

### **What This Proves**

| Skill Category | Evidence |
|---------------|----------|
| **Database fundamentals** | Schema design with normalization, constraints, indexes |
| **T-SQL proficiency** | CTEs, window functions, stored procedures, error handling |
| **Data integration** | CSV imports with staging, validation, rollback procedures |
| **Backup/recovery** | Full/differential backups, 3-stage restore validation |
| **Documentation** | Runbooks, training guides, troubleshooting flowcharts |
| **Production mindset** | Security (least privilege), audit logging, change management |

### **Interview Readiness**

Instead of saying *"I can learn SQL Server"*, I can now walk into an interview and say:

> *"I built a production-grade school data platform with 6 normalized tables, 8 reporting objects, comprehensive backup procedures, and operational documentation. Here's the GitHub repo, here's the demo script, and here are the 15 annotated screenshots. Let me show you the runbook."*

---

## Future Roadmap: From Simulation to Production

While this project is interview-focused, the architecture supports real-world expansion:

### **1. Power BI Dashboard Integration**
- Connect reporting views to interactive dashboards
- Real-time attendance monitoring with alerting
- Enrollment trend analysis across years
- Teacher workload visualization

### **2. Automated SEQTA Sync**
- Scheduled SSIS packages for nightly imports
- Incremental updates with change data capture
- Email notifications on import failures
- Data quality scorecards

### **3. Advanced Security & Compliance**
- Row-level security based on staff roles
- Transparent data encryption for medical_info
- Audit tables with temporal queries
- GDPR-compliant data retention policies

### **4. Performance Optimization**
- Columnstore indexes for historical reporting
- Query Store analysis for slow queries
- Database partitioning by enrollment_year
- Read replicas for Power BI loads

### **5. Cloud Migration Path**
- Azure SQL Database deployment
- Geo-replication for disaster recovery
- Azure Data Factory for ETL orchestration
- Integration with Microsoft 365 (SharePoint, Teams)

---

## Key Takeaways

This project reinforced several engineering principles:

1. **Build to prove, not just to practice** — Every decision was portfolio-oriented
2. **Documentation = Deliverable** — The runbook is as important as the code
3. **Simulate real constraints** — SQL Server Express limits forced production-ready design
4. **Edge cases reveal skill** — Intentional data quality issues prove validation competency
5. **Timeline discipline** — 16-day execution plan kept momentum and accountability

---

## Try It Yourself

The complete project is open source and ready to deploy:

| Resource | Link |
|----------|------|
| **GitHub Repo** | [github.com/lfariabr/stc-datalab](https://github.com/lfariabr/stc-datalab) |
| **Setup Guide** | [Assessment 1 Documentation](https://github.com/lfariabr/stc-datalab/tree/main/docs/Assessment1) |
| **Operational Runbook** | [06_runbook.md](https://github.com/lfariabr/stc-datalab/blob/main/docs/Assessment3/06_runbook.md) |
| **Demo Script** | [07_demo_script.md](https://github.com/lfariabr/stc-datalab/blob/main/docs/Assessment3/07_demo_script.md) |

**Quick Start (Docker):**
```bash
# 1. Clone the repo
git clone https://github.com/lfariabr/stc-datalab.git
cd stc-datalab

# 2. Start SQL Server Express
docker run -e "ACCEPT_EULA=Y" \
  -e "MSSQL_SA_PASSWORD=StC_SchoolLab2025!" \
  -e "MSSQL_PID=Express" \
  -p 1433:1433 --name sqlserver \
  -d mcr.microsoft.com/mssql/server:2022-latest

# 3. Create database and schema
sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -i sql/00_create_db.sql
sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -i sql/01_schema.sql

# 4. Seed demo data
sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -i sql/02_seed_data.sql

# 5. Test reporting
sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q \
  "USE StC_SchoolLab; EXEC sp_AttendanceByDate @StartDate='2025-01-22', @EndDate='2025-01-22';"
```

---

## Let's Connect!

This project exemplifies my approach to technical challenges: structured execution, production-quality deliverables, and comprehensive documentation. If you're:

- Building enterprise data systems
- Working with SQL Server in education/non-profit sectors
- Interested in data engineering best practices
- Hiring for database administration roles

I'd love to connect:

- **LinkedIn:** [linkedin.com/in/lfariabr](https://www.linkedin.com/in/lfariabr/)
- **GitHub:** [github.com/lfariabr](https://github.com/lfariabr)
- **Portfolio:** [luisfaria.dev](https://luisfaria.dev)

---

**Tech Stack Summary:**

| Current Implementation | Production Extensions |
|----------------------|----------------------|
| SQL Server 2022 Express, SSMS, T-SQL, Docker, Markdown | Azure SQL Database, SSIS, Power BI, Columnstore Indexes, TDE, Azure Data Factory |

---

*Built with 🎓 and database discipline by [Luis Faria](https://luisfaria.dev)*

> *Hard work is my preferred language and I try to speak it fluently.*