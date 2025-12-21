-- Create the main database for StC School Data Lab
CREATE DATABASE StC_SchoolLab;
GO

-- Create a basic login for security (school_user with read/write access)
-- Note: In production, use stronger passwords and least privilege
CREATE LOGIN school_user WITH PASSWORD = 'SecurePass123';
GO

USE StC_SchoolLab;
GO

CREATE USER school_user FOR LOGIN school_user;
GO

-- Grant basic read/write roles
ALTER ROLE db_datareader ADD MEMBER school_user;
ALTER ROLE db_datawriter ADD MEMBER school_user;
GO