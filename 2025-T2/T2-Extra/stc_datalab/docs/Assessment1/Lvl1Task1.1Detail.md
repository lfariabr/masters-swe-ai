
# Level 1 Task 1: Install & Connect SQL Server Express + Management Tools

## Overview
This task sets up SQL Server Express using Docker in the Linux Codespaces environment, creates the database, and configures basic security. Since we're not on Windows, we use Docker for SQL Server and VS Code extensions instead of SSMS.

## Step-by-Step Commands

### 1. Verify Docker is Installed
```bash
docker --version
```
**Purpose**: Checks if Docker is available (it should be in Codespaces).

### 2. Run SQL Server Express Container
```bash
# Codespaces
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=StC_SchoolLab2025!" -e "MSSQL_PID=Express" -p 1433:1433 --name sqlserver --hostname sqlserver -d mcr.microsoft.com/mssql/server:2022-latest

# Macbook
docker run \
  -e 'ACCEPT_EULA=Y' \
  -e 'MSSQL_SA_PASSWORD=StC_SchoolLab2025!' \
  -e 'MSSQL_PID=Express' \
  -p 1433:1433 \
  --name sqlserver \
  --hostname sqlserver \
  -d mcr.microsoft.com/mssql/server:2022-latest
```
**Purpose**: Starts SQL Server Express in a Docker container.
- `ACCEPT_EULA=Y`: Accepts the license
- `MSSQL_SA_PASSWORD`: Sets SA password (must be strong)
- `MSSQL_PID=Express`: Specifies Express edition
- `-p 1433:1433`: Exposes port 1433
- `--name sqlserver`: Names the container
- `-d`: Runs in background

### 3. Check Container Status
```bash
docker ps
```
**Purpose**: Verifies the SQL Server container is running.

### 4. Install SQL Server Command-Line Tools
```bash
# Debian/Ubuntu package manager
sudo apt update && sudo apt install -y mssql-tools18

# Macbook Homebrew
brew tap microsoft/mssql-release https://github.com/microsoft/homebrew-mssql-release
brew update
HOMEBREW_NO_AUTO_UPDATE=1 brew install sqlcmd
```
**Purpose**: Installs sqlcmd and other tools for database management.

### 5. Test Connection to SQL Server
```bash
# Test connection (Codespaces)
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -Q "SELECT @@VERSION;"

# Test connection (Macbook)
sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q "SELECT @@VERSION;"
```
**Purpose**: Tests connection and shows SQL Server version.
- `-No`: Trusts self-signed SSL certificate
- `-Q`: Executes query and exits

### 6. Create the Database
```bash
# Create database (Codespaces)
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -Q "CREATE DATABASE StC_SchoolLab;"

# Create database (Macbook)
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q "CREATE DATABASE StC_SchoolLab;"
```
**Purpose**: Creates the main database for the project.

### 7. Verify Database Creation
```bash
# Codespaces
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -Q "SELECT name FROM sys.databases WHERE name = 'StC_SchoolLab';"

# Macbook
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q "SELECT name FROM sys.databases WHERE name = 'StC_SchoolLab';"
```
**Purpose**: Confirms the database exists.

### 8. Create Basic Security (User Account)
```bash
# Create login (Codespaces)
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -Q "CREATE LOGIN school_user WITH PASSWORD = 'SecurePass123';"

# Create login (Macbook)
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q "CREATE LOGIN school_user WITH PASSWORD = 'SecurePass123';"
```
**Purpose**: Creates a SQL login for application access.

```bash
# Create database user (Codespaces)
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -Q "USE StC_SchoolLab; CREATE USER school_user FOR LOGIN school_user; ALTER ROLE db_datareader ADD MEMBER school_user; ALTER ROLE db_datawriter ADD MEMBER school_user;"

# Create database user (Macbook)
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q "USE StC_SchoolLab; CREATE USER school_user FOR LOGIN school_user; ALTER ROLE db_datareader ADD MEMBER school_user; ALTER ROLE db_datawriter ADD MEMBER school_user;"
```
**Purpose**: Creates database user and grants read/write permissions.

## VS Code Setup (Manual Steps)
1. Install "SQL Server (mssql)" extension in VS Code
2. Use Command Palette: "MS SQL: Connect"
3. Connection details:
   - Server: `localhost`
   - Database: `StC_SchoolLab`
   - Authentication: `SQL Login`
   - Username: `sa` or `school_user`
   - Password: As above

## Notes
- All commands should be run in the terminal
- The Docker container persists during the session
- If Codespaces restarts, run `docker start sqlserver` to resume
- Passwords are for demo only; use stronger ones in production
- This setup matches school's on-premise SQL Server but adapted for Linux/Docker