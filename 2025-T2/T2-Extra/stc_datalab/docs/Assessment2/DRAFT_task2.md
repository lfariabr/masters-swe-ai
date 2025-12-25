
---

## **Task 2: Create reporting views**

### **What I've Done:**
Created three essential reporting views that simulate the kind of data access needed at StC:

1. **vw_StudentProfile** - Comprehensive student data for staff access
   - Student details (name, DOB, contact info)
   - Emergency contacts and medical information
   - Current enrollments and class assignments
   - Attendance summary (present/absent counts)

2. **vw_ClassRoll** - Daily attendance tracking for teachers
   - Class schedule and teacher information
   - Student attendance status for the current day
   - Roll call data for class management

3. **vw_AttendanceSummary** - Aggregated metrics for leadership
   - Daily attendance rates by class
   - Overall school attendance trends
   - Absence patterns and reporting

### **Why It Matters:**
These views demonstrate the ability to create reusable reporting objects that:
- Provide different data perspectives for different user roles
- Maintain data integrity while offering simplified access
- Support real operational needs like attendance tracking and student management
- Follow best practices for performance and maintainability

### **Validation Query**
```sql
SELECT COUNT(*) as vw_StudentProfile_Count FROM vw_StudentProfile;
SELECT COUNT(*) as vw_ClassRoll_Count FROM vw_ClassRoll;
SELECT COUNT(*) as vw_AttendanceSummary_Count FROM vw_AttendanceSummary;
```

**Expected Output:**
```bash
vw_StudentProfile_Count    vw_ClassRoll_Count    vw_AttendanceSummary_Count
-------------------------  --------------------  --------------------------
200                        30                    30
```

---