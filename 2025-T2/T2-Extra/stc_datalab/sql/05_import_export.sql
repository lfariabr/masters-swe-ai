-- =====================================================
-- Level 2 Task 2.4: Import/Export Simulation
-- Mimics SEQTA CSV imports with staging, validation, and merge
-- =====================================================

USE StC_SchoolLab;
GO

-- =====================================================
-- PART 1: CREATE STAGING TABLES
-- These mirror production tables but allow NULLs and duplicates
-- for validation before merging
-- =====================================================

PRINT '--- Creating Staging Tables ---';

-- Drop staging tables if they exist (for re-runs)
IF OBJECT_ID('Staging_Students', 'U') IS NOT NULL DROP TABLE Staging_Students;
IF OBJECT_ID('Staging_Classes', 'U') IS NOT NULL DROP TABLE Staging_Classes;
IF OBJECT_ID('Staging_Enrollments', 'U') IS NOT NULL DROP TABLE Staging_Enrollments;
IF OBJECT_ID('Import_Log', 'U') IS NOT NULL DROP TABLE Import_Log;
GO

-- Staging table for students (loose constraints for validation)
CREATE TABLE Staging_Students (
    staging_id INT IDENTITY(1,1) PRIMARY KEY,
    student_number NVARCHAR(20),
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    date_of_birth DATE,
    address NVARCHAR(255),
    phone NVARCHAR(20),
    email NVARCHAR(100),
    emergency_contact NVARCHAR(100),
    emergency_phone NVARCHAR(20),
    enrollment_year INT,
    import_date DATETIME2 DEFAULT GETDATE(),
    import_batch NVARCHAR(50),
    is_valid BIT DEFAULT 1,
    validation_errors NVARCHAR(MAX)
);
GO

-- Staging table for classes
CREATE TABLE Staging_Classes (
    staging_id INT IDENTITY(1,1) PRIMARY KEY,
    class_name NVARCHAR(100),
    subject_code NVARCHAR(20),
    teacher_email NVARCHAR(100),
    year_level INT,
    semester NVARCHAR(20),
    max_students INT,
    room NVARCHAR(50),
    schedule NVARCHAR(200),
    import_date DATETIME2 DEFAULT GETDATE(),
    import_batch NVARCHAR(50),
    is_valid BIT DEFAULT 1,
    validation_errors NVARCHAR(MAX)
);
GO

-- Staging table for enrollments
CREATE TABLE Staging_Enrollments (
    staging_id INT IDENTITY(1,1) PRIMARY KEY,
    student_number NVARCHAR(20),
    class_name NVARCHAR(100),
    enrollment_date DATE,
    status NVARCHAR(20),
    grade NVARCHAR(5),
    import_date DATETIME2 DEFAULT GETDATE(),
    import_batch NVARCHAR(50),
    is_valid BIT DEFAULT 1,
    validation_errors NVARCHAR(MAX)
);
GO

-- Import log for tracking batch imports
CREATE TABLE Import_Log (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    import_batch NVARCHAR(50) NOT NULL,
    table_name NVARCHAR(50) NOT NULL,
    source_file NVARCHAR(255),
    rows_imported INT DEFAULT 0,
    rows_valid INT DEFAULT 0,
    rows_invalid INT DEFAULT 0,
    rows_duplicate INT DEFAULT 0,
    rows_merged INT DEFAULT 0,
    import_start DATETIME2 DEFAULT GETDATE(),
    import_end DATETIME2,
    status NVARCHAR(20) DEFAULT 'Started', -- Started, Validated, Merged, Failed
    error_message NVARCHAR(MAX)
);
GO

PRINT 'Staging tables created successfully.';
GO

-- =====================================================
-- PART 2: STORED PROCEDURE FOR STUDENT IMPORT VALIDATION
-- =====================================================

IF OBJECT_ID('sp_ValidateStagingStudents', 'P') IS NOT NULL DROP PROCEDURE sp_ValidateStagingStudents;
GO

CREATE PROCEDURE sp_ValidateStagingStudents
    @ImportBatch NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    
    PRINT '--- Validating Staging_Students for batch: ' + @ImportBatch + ' ---';
    
    -- Rule 1: Required fields (student_number, first_name, last_name, date_of_birth)
    UPDATE Staging_Students
    SET is_valid = 0,
        validation_errors = COALESCE(validation_errors + '; ', '') + 'Missing required field(s)'
    WHERE import_batch = @ImportBatch
      AND (student_number IS NULL OR student_number = ''
           OR first_name IS NULL OR first_name = ''
           OR last_name IS NULL OR last_name = ''
           OR date_of_birth IS NULL);
    
    -- Rule 2: Invalid phone numbers (contains '???')
    UPDATE Staging_Students
    SET is_valid = 0,
        validation_errors = COALESCE(validation_errors + '; ', '') + 'Invalid phone number'
    WHERE import_batch = @ImportBatch
      AND phone LIKE '%???%';
    
    -- Rule 3: Invalid address (pending)
    UPDATE Staging_Students
    SET is_valid = 0,
        validation_errors = COALESCE(validation_errors + '; ', '') + 'Address pending - needs update'
    WHERE import_batch = @ImportBatch
      AND address LIKE '%Pending%';
    
    -- Rule 4: Duplicate student_number within batch (mark all but first)
    ;WITH Duplicates AS (
        SELECT staging_id,
               ROW_NUMBER() OVER (PARTITION BY student_number ORDER BY staging_id) AS rn
        FROM Staging_Students
        WHERE import_batch = @ImportBatch
    )
    UPDATE s
    SET is_valid = 0,
        validation_errors = COALESCE(s.validation_errors + '; ', '') + 'Duplicate student_number in batch'
    FROM Staging_Students s
    JOIN Duplicates d ON s.staging_id = d.staging_id
    WHERE d.rn > 1;
    
        -- Rule 5: Name casing issues (informational)
        -- IMPORTANT: do NOT auto-titlecase names. It is culturally/linguistically brittle
        -- (e.g., McDonald, O'Brien, van der Berg, hyphenated surnames). Flag for review instead.
        UPDATE Staging_Students
        SET validation_errors = COALESCE(validation_errors + '; ', '') + 'Warning: lowercase first name detected'
        WHERE import_batch = @ImportBatch
            AND first_name COLLATE Latin1_General_CS_AS = LOWER(first_name) COLLATE Latin1_General_CS_AS
            AND LEN(first_name) > 0;
    
        -- Email normalization: lowercase any email containing uppercase characters
        -- (email local-parts can be case-sensitive in theory, but in practice school systems treat
        -- addresses case-insensitively; lowercasing prevents report dedupe issues).
        UPDATE Staging_Students
        SET email = LOWER(email),
                validation_errors = COALESCE(validation_errors + '; ', '') + 'Fixed: email lowercased'
        WHERE import_batch = @ImportBatch
            AND email IS NOT NULL
            AND email COLLATE Latin1_General_CS_AS <> LOWER(email) COLLATE Latin1_General_CS_AS;
    
    -- Trailing spaces in last names
    UPDATE Staging_Students
    SET last_name = RTRIM(last_name),
        validation_errors = COALESCE(validation_errors + '; ', '') + 'Fixed: trailing space in last name'
    WHERE import_batch = @ImportBatch
      AND last_name <> RTRIM(last_name);
    
    -- Return validation summary
    SELECT 
        COUNT(*) AS total_rows,
        SUM(CASE WHEN is_valid = 1 THEN 1 ELSE 0 END) AS valid_rows,
        SUM(CASE WHEN is_valid = 0 THEN 1 ELSE 0 END) AS invalid_rows,
        SUM(CASE WHEN validation_errors LIKE '%Duplicate%' THEN 1 ELSE 0 END) AS duplicate_rows
    FROM Staging_Students
    WHERE import_batch = @ImportBatch;
    
    -- Return invalid records for review
    SELECT staging_id, student_number, first_name, last_name, validation_errors
    FROM Staging_Students
    WHERE import_batch = @ImportBatch AND is_valid = 0;
    
    PRINT 'Validation complete for batch: ' + @ImportBatch;
END;
GO

-- =====================================================
-- PART 3: STORED PROCEDURE FOR MERGE TO PRODUCTION
-- =====================================================

IF OBJECT_ID('sp_MergeStagingStudents', 'P') IS NOT NULL DROP PROCEDURE sp_MergeStagingStudents;
GO

CREATE PROCEDURE sp_MergeStagingStudents
    @ImportBatch NVARCHAR(50),
    @ForceUpdate BIT = 0  -- If 1, update existing records
AS
BEGIN
    SET NOCOUNT ON;

    -- Merge semantics:
    -- - By default, NULL/empty values in staging do NOT overwrite production values.
    -- - To intentionally clear a nullable field in production, pass the sentinel value 'CLEAR'
    --   in the CSV/staging column; the merge will set the target column to NULL.
    --   (Applies to: address, phone, email, emergency_contact, emergency_phone)
    
    DECLARE @RowsInserted INT = 0;
    DECLARE @RowsUpdated INT = 0;
    DECLARE @RowsSkipped INT = 0;
    
    PRINT '--- Merging Staging_Students to Students for batch: ' + @ImportBatch + ' ---';
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Insert new students (not already in production)
        INSERT INTO Students (
            student_number, first_name, last_name, date_of_birth,
            address, phone, email, emergency_contact, emergency_phone,
            enrollment_year, created_date, updated_date
        )
        SELECT 
            s.student_number, s.first_name, s.last_name, s.date_of_birth,
            s.address, s.phone, s.email, s.emergency_contact, s.emergency_phone,
            s.enrollment_year, GETDATE(), GETDATE()
        FROM Staging_Students s
        WHERE s.import_batch = @ImportBatch
          AND s.is_valid = 1
          AND NOT EXISTS (
              SELECT 1 FROM Students p WHERE p.student_number = s.student_number
          );
        
        SET @RowsInserted = @@ROWCOUNT;
        
        -- Update existing students if @ForceUpdate = 1
        IF @ForceUpdate = 1
        BEGIN
            UPDATE p
            SET first_name = s.first_name,
                last_name = s.last_name,
                date_of_birth = s.date_of_birth,
                                address = CASE
                                                        WHEN s.address = 'CLEAR' THEN NULL
                                                        WHEN s.address IS NULL OR LTRIM(RTRIM(s.address)) = '' THEN p.address
                                                        ELSE s.address
                                                    END,
                                phone = CASE
                                                    WHEN s.phone = 'CLEAR' THEN NULL
                                                    WHEN s.phone IS NULL OR LTRIM(RTRIM(s.phone)) = '' THEN p.phone
                                                    ELSE s.phone
                                                END,
                                email = CASE
                                                    WHEN s.email = 'CLEAR' THEN NULL
                                                    WHEN s.email IS NULL OR LTRIM(RTRIM(s.email)) = '' THEN p.email
                                                    ELSE s.email
                                                END,
                                emergency_contact = CASE
                                                                            WHEN s.emergency_contact = 'CLEAR' THEN NULL
                                                                            WHEN s.emergency_contact IS NULL OR LTRIM(RTRIM(s.emergency_contact)) = '' THEN p.emergency_contact
                                                                            ELSE s.emergency_contact
                                                                        END,
                                emergency_phone = CASE
                                                                        WHEN s.emergency_phone = 'CLEAR' THEN NULL
                                                                        WHEN s.emergency_phone IS NULL OR LTRIM(RTRIM(s.emergency_phone)) = '' THEN p.emergency_phone
                                                                        ELSE s.emergency_phone
                                                                    END,
                updated_date = GETDATE()
            FROM Students p
            JOIN Staging_Students s ON p.student_number = s.student_number
            WHERE s.import_batch = @ImportBatch
              AND s.is_valid = 1;
            
            SET @RowsUpdated = @@ROWCOUNT;
        END
        
        -- Count skipped (already exists, not updated)
        SELECT @RowsSkipped = COUNT(*)
        FROM Staging_Students s
        WHERE s.import_batch = @ImportBatch
          AND s.is_valid = 1
          AND EXISTS (SELECT 1 FROM Students p WHERE p.student_number = s.student_number)
          AND @ForceUpdate = 0;
        
        COMMIT TRANSACTION;
        
        -- Update import log
        UPDATE Import_Log
        SET rows_merged = @RowsInserted + @RowsUpdated,
            import_end = GETDATE(),
            status = 'Merged'
        WHERE import_batch = @ImportBatch AND table_name = 'Students';
        
        -- Return summary
        SELECT 
            @ImportBatch AS import_batch,
            @RowsInserted AS rows_inserted,
            @RowsUpdated AS rows_updated,
            @RowsSkipped AS rows_skipped,
            'Success' AS status;
        
        PRINT 'Merge complete. Inserted: ' + CAST(@RowsInserted AS VARCHAR) + 
              ', Updated: ' + CAST(@RowsUpdated AS VARCHAR) + 
              ', Skipped: ' + CAST(@RowsSkipped AS VARCHAR);
              
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        
        UPDATE Import_Log
        SET status = 'Failed',
            error_message = ERROR_MESSAGE(),
            import_end = GETDATE()
        WHERE import_batch = @ImportBatch AND table_name = 'Students';
        
        SELECT 
            @ImportBatch AS import_batch,
            0 AS rows_inserted,
            0 AS rows_updated,
            0 AS rows_skipped,
            'Failed: ' + ERROR_MESSAGE() AS status;
            
        PRINT 'ERROR: Merge failed - ' + ERROR_MESSAGE();
    END CATCH;
END;
GO

-- =====================================================
-- PART 4: EXPORT PROCEDURE (for Power BI, SEQTA sync)
-- =====================================================

IF OBJECT_ID('sp_ExportStudentData', 'P') IS NOT NULL DROP PROCEDURE sp_ExportStudentData;
GO

CREATE PROCEDURE sp_ExportStudentData
    @Format NVARCHAR(20) = 'FULL',  -- FULL, BASIC, ATTENDANCE
    @YearLevel INT = NULL,
    @ActiveOnly BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    -- ActiveOnly definition (consistent across formats):
    -- treat students enrolled this year or last year as "active" for export purposes.
    
    IF @Format = 'FULL'
    BEGIN
        -- Full student profile export (for data warehouse)
        SELECT 
            student_number,
            first_name,
            last_name,
            date_of_birth,
            DATEDIFF(YEAR, date_of_birth, GETDATE())
              - CASE
                    WHEN DATEADD(YEAR, DATEDIFF(YEAR, date_of_birth, GETDATE()), date_of_birth) > CAST(GETDATE() AS DATE)
                    THEN 1
                    ELSE 0
                END AS age,
            address,
            phone,
            email,
            emergency_contact,
            emergency_phone,
            enrollment_year,
            created_date,
            updated_date
        FROM Students
        WHERE (@ActiveOnly = 0 OR enrollment_year >= YEAR(GETDATE()) - 1)
        ORDER BY last_name, first_name;
    END
    ELSE IF @Format = 'BASIC'
    BEGIN
        -- Basic info only (for external systems like SEQTA)
        SELECT 
            student_number,
            first_name,
            last_name,
            date_of_birth,
            email
        FROM Students
        WHERE (@ActiveOnly = 0 OR enrollment_year >= YEAR(GETDATE()) - 1)
        ORDER BY student_number;
    END
    ELSE IF @Format = 'ATTENDANCE'
    BEGIN
        -- Attendance-focused export with class info
        SELECT 
            s.student_number,
            s.first_name + ' ' + s.last_name AS student_name,
            c.class_name,
            e.status AS enrollment_status,
            COUNT(CASE WHEN a.status = 'Present' THEN 1 END) AS days_present,
            COUNT(CASE WHEN a.status = 'Absent' THEN 1 END) AS days_absent,
            COUNT(CASE WHEN a.status = 'Late' THEN 1 END) AS days_late,
            COUNT(a.attendance_id) AS total_marked
        FROM Students s
        LEFT JOIN Enrollments e ON s.student_id = e.student_id
        LEFT JOIN Classes c ON e.class_id = c.class_id
        LEFT JOIN Attendance a ON s.student_id = a.student_id AND c.class_id = a.class_id
        WHERE (@YearLevel IS NULL OR c.year_level = @YearLevel)
          AND (@ActiveOnly = 0 OR s.enrollment_year >= YEAR(GETDATE()) - 1)
        GROUP BY s.student_number, s.first_name, s.last_name, c.class_name, e.status
        ORDER BY s.last_name, s.first_name, c.class_name;
    END
    ELSE
    BEGIN
        RAISERROR('Invalid @Format. Use FULL, BASIC, or ATTENDANCE.', 16, 1);
        RETURN;
    END
    
    -- Return export metadata
    SELECT 
        @Format AS export_format,
        @@ROWCOUNT AS rows_exported,
        GETDATE() AS export_timestamp;
END;
GO

-- =====================================================
-- PART 5: DEMO - SIMULATED IMPORT WORKFLOW
-- =====================================================

PRINT '';
PRINT '=====================================================';
PRINT 'DEMO: Simulated Import Workflow';
PRINT '=====================================================';

-- Step 1: Create import batch
DECLARE @BatchId NVARCHAR(50) = 'IMPORT_' + FORMAT(GETDATE(), 'yyyyMMdd_HHmmss');
PRINT 'Created batch: ' + @BatchId;

-- Step 2: Log the import start
INSERT INTO Import_Log (import_batch, table_name, source_file, status)
VALUES (@BatchId, 'Students', 'students_import.csv', 'Started');

-- Step 3: Simulate BULK INSERT (in real scenario, use BULK INSERT or SSIS)
-- For demo, we insert sample data directly
INSERT INTO Staging_Students (student_number, first_name, last_name, date_of_birth, address, phone, email, emergency_contact, emergency_phone, enrollment_year, import_batch)
VALUES 
    ('STU2025001', 'Emma', 'Johnson', '2010-03-15', '123 Main Street Sydney NSW 2000', '0412345678', 'emma.johnson@student.stc.edu.au', 'Sarah Johnson', '0498765432', 2025, @BatchId),
    ('STU2025002', 'Liam', 'Williams', '2010-07-22', '45 Park Avenue Melbourne VIC 3000', '0423456789', 'liam.williams@student.stc.edu.au', 'Michael Williams', '0487654321', 2025, @BatchId),
    ('STU2025003', 'olivia', 'Brown', '2010-01-08', '78 Ocean Drive Brisbane QLD 4000', NULL, 'olivia.brown@student.stc.edu.au', 'Jennifer Brown', '0476543210', 2025, @BatchId),
    ('STU2025004', 'Noah', 'Taylor', '2009-11-30', '12 Hill Road Perth WA 6000', '0445678901', 'noah.taylor@student.stc.edu.au', NULL, '0465432109', 2025, @BatchId),
    ('STU2025005', 'Ava', 'Anderson', '2010-05-17', '56 River Lane Adelaide SA 5000', '???', 'ava.anderson@student.stc.edu.au', 'Robert Anderson', '0454321098', 2025, @BatchId),
    ('STU2025006', 'William', 'Thomas ', '2009-09-25', '89 Forest Way Hobart TAS 7000', '0467890123', 'WILLIAM.THOMAS@STUDENT.STC.EDU.AU', 'Linda Thomas', '0443210987', 2025, @BatchId),
    ('STU2025007', 'Sophia', 'Jackson', '2010-12-03', '234 Beach Road Gold Coast QLD 4217', '0478901234', 'sophia.jackson@student.stc.edu.au', 'David Jackson', '0432109876', 2025, @BatchId),
    ('STU2025008', 'James', 'White', '2009-04-11', '567 Mountain View Canberra ACT 2600', '0489012345', 'james.white@student.stc.edu.au', 'Karen White', '0421098765', 2025, @BatchId),
    ('STU2025009', 'Isabella', 'Harris', '2010-08-29', 'Address Pending', '0490123456', 'isabella.harris@student.stc.edu.au', 'Mark Harris', '0410987654', 2025, @BatchId),
    ('STU2025010', 'Oliver', 'Martin', '2009-02-14', '321 Valley Road Darwin NT 0800', '0401234567', 'oliver.martin@student.stc.edu.au', 'Susan Martin', '0409876543', 2025, @BatchId),
    ('STU2025011', 'Mia', 'Garcia', '2010-06-20', 'Singapore (Boarding Student)', NULL, 'mia.garcia@student.stc.edu.au', 'Carlos Garcia', '+6591234567', 2025, @BatchId),
    ('STU2025012', 'Benjamin', 'Lee', '2009-10-05', 'Jakarta Indonesia (Boarding Student)', '0412222333', 'benjamin.lee@student.stc.edu.au', 'Wei Lee', '+628123456789', 2025, @BatchId),
    ('STU2025001', 'Emma', 'Johnson', '2010-03-15', '123 Main Street Sydney NSW 2000', '0412345678', 'emma.johnson@student.stc.edu.au', 'Sarah Johnson', '0498765432', 2025, @BatchId);  -- Duplicate!

DECLARE @RowsImported INT = @@ROWCOUNT;
PRINT 'Rows imported to staging: ' + CAST(@RowsImported AS VARCHAR);

-- Update log
UPDATE Import_Log 
SET rows_imported = @RowsImported 
WHERE import_batch = @BatchId AND table_name = 'Students';

-- Step 4: Run validation
PRINT '';
PRINT '--- Running Validation ---';
EXEC sp_ValidateStagingStudents @ImportBatch = @BatchId;

-- Step 5: Show staging data with validation results
PRINT '';
PRINT '--- Staging Data After Validation ---';
SELECT staging_id, student_number, first_name, last_name, is_valid, validation_errors
FROM Staging_Students
WHERE import_batch = @BatchId
ORDER BY staging_id;

-- Update log with validation counts
UPDATE Import_Log
SET rows_valid = (SELECT COUNT(*) FROM Staging_Students WHERE import_batch = @BatchId AND is_valid = 1),
    rows_invalid = (SELECT COUNT(*) FROM Staging_Students WHERE import_batch = @BatchId AND is_valid = 0),
    rows_duplicate = (SELECT COUNT(*) FROM Staging_Students WHERE import_batch = @BatchId AND validation_errors LIKE '%Duplicate%'),
    status = 'Validated'
WHERE import_batch = @BatchId AND table_name = 'Students';

-- Show import log
PRINT '';
PRINT '--- Import Log ---';
SELECT * FROM Import_Log WHERE import_batch = @BatchId;

PRINT '';
PRINT '=====================================================';
PRINT 'Demo complete! Valid records ready for merge.';
PRINT 'Run: EXEC sp_MergeStagingStudents @ImportBatch = ''' + @BatchId + ''';';
PRINT '=====================================================';
GO
