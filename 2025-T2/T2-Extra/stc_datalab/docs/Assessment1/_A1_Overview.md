**Level 1: Operator Fundamentals Assessment** step by step, explaining what we did, why it matters, and what it proves about current skills. This is a crash course in being the "safe pair of hands" who won't break production.

## 🎯 **Level 1 Overview: "He knows the basics. He won't break production."**
This level proves I can handle the day-to-day database operations at a school like StC. No fancy analytics or complex integrations—just core skills needed to maintain SQL Server safely. I've simulated their on-premise SQL Server environment but adapted for a Linux/Docker setup.

---

## ✅ **Task 1: Install & Connect SQL Server Express + Management Tools**

### **What I've Done:**
- Set up SQL Server Express using Docker (since I'm in Linux Codespaces, not Windows)
- Created the database `StC_SchoolLab`
- Configured basic security with SA account and limited user
- Installed command-line tools for management

### **Why It Matters:**
Schools like StC run SQL Server on-premise. So knowing how to set up and connect to databases without breaking existing systems is crucial. This proves I'm able to handle the "first day" setup.

### **Key Commands I've Run:**
```bash
# Start SQL Server in Docker
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=StC_SchoolLab2025!" -e "MSSQL_PID=Express" -p 1433:1433 --name sqlserver --hostname sqlserver -d mcr.microsoft.com/mssql/server:2022-latest

# Test connection
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -Q "SELECT @@VERSION;"

# Create database and user
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -i sql/00_create_db.sql
```

### **What I've Learned:**
- Docker containerization for databases
- SQL Server authentication and security basics
- Connection troubleshooting (SSL, ports, etc.)
- Least privilege access (don't use SA for everything)

---

## ✅ **Task 2: Create Schema (Core Tables)**

### **What I've Done:**
Built a complete database schema with 6 tables matching real school systems:
- **Students**: Privacy-sensitive fields (medical info, emergency contacts)
- **Staff**: Role-based attributes (Teacher, Principal, etc.)
- **Subjects**: Curriculum structure (math, english, etc.)
- **Classes**: Teacher assignments and scheduling
- **Enrollments**: Student-class relationships
- **Attendance**: Daily tracking like SEQTA system

Added constraints, indexes, and triggers for data integrity.

### **Why It Matters:**
Schools have complex data relationships. The tables design must handle real-world scenarios like student privacy, class assignments, and attendance tracking. 

### **Key SQL Concepts:**
```sql
-- Example table with constraints
CREATE TABLE Students (
    student_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    medical_info NVARCHAR(500), -- Privacy sensitive
    student_number NVARCHAR(20) UNIQUE NOT NULL
);

-- Foreign key relationships
CREATE TABLE Classes (
    class_id INT IDENTITY(1,1) PRIMARY KEY,
    subject_id INT NOT NULL,
    staff_id INT NOT NULL, -- Teacher assignment
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);
```

### **What I've Learned:**
- Database normalization (avoiding data duplication)
- Primary/foreign key relationships
- Privacy considerations for sensitive data
- Indexing for performance
- Audit trails with triggers

---

## ✅ **Task 3: Basic SQL Competence**

### **What I've Done:**
Demonstrated essential SQL queries using sample data:
- **SELECT + WHERE + ORDER BY**: Basic student filtering
- **LEFT JOIN**: Complete reporting (shows all students, even unenrolled)
- **GROUP BY**: Attendance summaries and counts

### **Why It Matters:**
School staff need reports. You must write queries that don't miss data or crash the system. LEFT JOIN is crucial because you always want to see ALL students in reports, not just enrolled ones.

### **Key Queries We Tested:**
```sql
-- Basic filtering and sorting
SELECT first_name, last_name, enrollment_year
FROM Students
WHERE enrollment_year = 2025
ORDER BY last_name;

-- LEFT JOIN for complete data
SELECT s.first_name, s.last_name, c.class_name
FROM Students s
LEFT JOIN Enrollments e ON s.student_id = e.student_id
LEFT JOIN Classes c ON e.class_id = c.class_id;

-- GROUP BY for summaries
SELECT status, COUNT(*) as count
FROM Attendance
WHERE attendance_date = '2025-12-20'
GROUP BY status;
```

### **What You Learned:**
- Query optimization (when to use indexes)
- Data preservation in reports (LEFT vs INNER JOIN)
- Aggregate functions for summaries
- Real-world reporting scenarios

---

## **Task 4: Backup & Restore**

### **What We Did:**
- Created full database backup
- Restored to a new database name (`StC_SchoolLab_RESTORE`)
- Verified data integrity
- Documented procedures

### **Why It Matters:**
Schools can't afford data loss. You must know how to backup before changes and restore in emergencies. This proves you're "safe" - you won't lose production data.

### **Key Commands:**
```sql
-- Backup
BACKUP DATABASE StC_SchoolLab
TO DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full.bak'
WITH FORMAT, NAME = 'Full Backup';

-- Restore to new name
RESTORE DATABASE StC_SchoolLab_RESTORE
FROM DISK = '/var/opt/mssql/backup/StC_SchoolLab_Full.bak'
WITH MOVE 'StC_SchoolLab' TO '/var/opt/mssql/data/StC_SchoolLab_RESTORE.mdf',
     MOVE 'StC_SchoolLab_log' TO '/var/opt/mssql/data/StC_SchoolLab_RESTORE_log.ldf';
```

### **What You Learned:**
- RPO/RTO concepts (Recovery Point/Time Objectives)
- Emergency restore procedures
- Backup verification
- Production safety protocols

---

## **🎓 What This Proves About You**

**For the StC Interview:**
- ✅ You can explain database vs schema vs table
- ✅ You know when and why to backup/restore
- ✅ You understand LEFT JOIN for complete reporting
- ✅ You can secure sensitive student data
- ✅ You document procedures professionally

**Real-World Skills:**
- Safe database operations (won't break production)
- Basic troubleshooting and setup
- Data integrity and privacy awareness
- Documentation for handover to others

## **📚 Files We Created**
- `sql/00_create_db.sql` - Database setup
- `sql/01_schema.sql` - Table structures
- `sql/02_sample_queries.sql` - SQL demonstrations
- `sql/07_backup_restore.sql` - Backup procedures
- `docs/01_setup.md` - Setup documentation
- `docs/04_backup_restore.md` - Recovery procedures
- level1_1.md to `level1_4.md` - Command guides

**Bottom Line:** Level 1 proves you're competent at the fundamentals. You know enough to be trusted with production databases without supervision. That's exactly what StC needs in their database role!

Ready to tackle **Level 2: Reporting & Data Integration**? That'll test your ability to generate real reports and handle data imports like SEQTA integrations. 🚀