# Level 1 Task 2: Create Schema (Core Tables)

## Overview
This task creates the core database schema with 6 tables matching school management systems like Synergetic and SEQTA. The schema includes privacy-sensitive fields, role-based attributes, and proper relationships with constraints and indexes.

## Step-by-Step Commands

### 1. Execute Schema Creation Script
```bash
# Codespaces Ubuntu
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -i /workspaces/masters-swe-ai/2025-T2/T2-Extra/stc_datalab/sql/01_schema.sql
```
```bash
# Macbook
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -i /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2025-T2/T2-Extra/stc_datalab/sql/01_schema.sql
```
**Purpose**: Creates all core tables, constraints, indexes, and triggers.
- Tables created: Students, Staff, Subjects, Classes, Enrollments, Attendance
- Includes foreign keys, unique constraints, and performance indexes
- Adds update triggers for audit trails

### 2. Verify Table Creation
```bash
# Codespaces Ubuntu
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -Q "USE StC_SchoolLab; SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY TABLE_NAME;"
```
```bash
# Macbook
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q "USE StC_SchoolLab; SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY TABLE_NAME;"
```
**Purpose**: Confirms all 6 tables were created successfully.
- Expected output: Students, Staff, Subjects, Classes, Enrollments, Attendance

## Schema Details

### Students Table
- **Privacy-sensitive fields**: medical_info, emergency_contact
- **Unique identifier**: student_number
- **Audit fields**: created_date, updated_date (with trigger)

### Staff Table
- **Role-based attributes**: role (Teacher, Principal, Admin, etc.)
- **Status tracking**: is_active flag

### Subjects Table
- **Curriculum structure**: subject_code, year_level, semester
- **Academic credits**: credits field

### Classes Table
- **Teacher assignments**: staff_id foreign key
- **Capacity management**: max_students
- **Scheduling**: room, schedule fields

### Enrollments Table
- **Student-class relationships**: composite unique constraint
- **Status tracking**: enrollment status, grades
- **Audit trail**: enrollment_date, withdrawal_date

### Attendance Table
- **Daily tracking**: attendance_date, status
- **Audit fields**: marked_by, marked_date
- **Uniqueness**: One record per student per class per day

## Indexes Created
- Students: last_name, enrollment_year
- Staff: role
- Classes: subject_id, staff_id
- Enrollments: student_id, class_id
- Attendance: student_id, class_id, attendance_date

## Notes
- All tables use IDENTITY for auto-incrementing primary keys
- Foreign key constraints ensure referential integrity
- NVARCHAR used for Unicode support (important for names)
- Triggers maintain updated_date fields automatically
- Schema matches real school systems like SEQTA and Synergetic
- Useful commands:

### Try to create the schema: 
```bash
# Codespaces Ubuntu
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -i /workspaces/masters-swe-ai/2025-T2/T2-Extra/stc_datalab/sql/01_schema.sql

# macOs 
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -i /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2025-T2/T2-Extra/stc_datalab/sql/01_schema.sql
```

### Verify the tables: 
```bash
# Codespaces Ubuntu
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -Q "USE StC_SchoolLab; SELECT TABLE_NAME, TABLE_TYPE FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY TABLE_NAME;"

# macOs
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C \
  -Q "USE StC_SchoolLab; SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY TABLE_NAME;"
```