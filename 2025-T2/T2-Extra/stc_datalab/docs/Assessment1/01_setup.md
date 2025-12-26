# Setup Documentation: SQL Server Express + Docker

## Overview
This document outlines the setup of SQL Server Express using Docker in a Linux environment (GitHub Codespaces), adapted from the standard Windows installation due to the cloud-based development environment.

## Prerequisites
- Docker installed and running
- Ubuntu 24.04 (Codespaces environment) or macOS
- SQL Server command-line tools (mssql-tools18)

## Step-by-Step Setup

### 1. Install Docker (if not present)
Docker is pre-installed in Codespaces. Verify with:
```bash
docker --version
```

### 2. Run SQL Server Express Container
Pull and run the official Microsoft SQL Server 2022 image configured for Express edition:

```bash
docker run -e "ACCEPT_EULA=Y" \
           -e "MSSQL_SA_PASSWORD=StC_SchoolLab2025!" \
           -e "MSSQL_PID=Express" \
           -p 1433:1433 \
           --name sqlserver \
           --hostname sqlserver \
           -d mcr.microsoft.com/mssql/server:2022-latest
```

**Parameters explained:**
- `ACCEPT_EULA=Y`: Accepts the End User License Agreement
- `MSSQL_SA_PASSWORD`: Strong password for the 'sa' (system administrator) account
- `MSSQL_PID=Express`: Specifies Express edition
- `-p 1433:1433`: Maps container port 1433 to host port 1433
- `--name sqlserver`: Names the container for easy reference
- `-d`: Runs in detached mode (background)

### 3. Install SQL Server Tools
Install command-line tools for database management:

```bash
# Debian/Ubuntu package manager
sudo apt update
sudo apt install -y mssql-tools18

# Macbook Homebrew
brew tap microsoft/mssql-release https://github.com/microsoft/homebrew-mssql-release
brew update
HOMEBREW_NO_AUTO_UPDATE=1 brew install sqlcmd
```

### 4. Verify Connection
Test the connection to SQL Server:

```bash
# Test connection (Codespaces)
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -Q "USE StC_SchoolLab; CREATE USER school_user FOR LOGIN school_user;"

# Test connection (Macbook)
sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -Q "SELECT @@VERSION;"
```

Expected output: SQL Server version information confirming Express Edition on Linux.

### 5. Create Database
Execute the database creation script:

```bash
# Codespaces
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -No -i sql/00_create_db.sql

# Macbook
/opt/homebrew/bin/sqlcmd -S localhost -U sa -P 'StC_SchoolLab2025!' -C -i sql/00_create_db.sql
```

### 6. Configure Basic Security
The setup includes:
- SA account with strong password
- Additional user account (`school_user`) with read/write permissions
- SQL Server Authentication enabled

**Security Notes:**
- SA password meets complexity requirements
- Created limited user for application access (least privilege principle)
- In production, would implement additional measures like:
  - Windows Authentication (if applicable)
  - Encrypted connections
  - Regular password changes
  - Audit logging

### 7. Connect via VS Code
1. Install the "SQL Server (mssql)" extension in VS Code
2. Open Command Palette (Ctrl+Shift+P)
3. Select "MS SQL: Connect"
4. Enter connection details:
   - Server: `localhost`
   - Database: `StC_SchoolLab`
   - Authentication: `SQL Login`
   - Username: `sa` or `school_user`
   - Password: As set above

## Screenshots
[Note: Screenshots would be captured here in a GUI environment. For Codespaces, terminal outputs are documented above.]

- Docker container running: `docker ps`
- SQL Server version query result
- Database creation confirmation
- VS Code connection successful

## Troubleshooting
- **Connection refused**: Ensure container is running (`docker ps`) and port 1433 is not blocked
- **SSL errors**: Use `-No` flag with sqlcmd to trust self-signed certificates
- **Permission denied**: Verify Docker is running and user has permissions
- **Container not starting**: Check Docker logs with `docker logs sqlserver`

## Environment Notes
- Adapted for Linux/Codespaces instead of Windows/SSMS
- Uses Azure Data Studio alternative via VS Code extension
- Maintains Express edition for resource efficiency
- Password stored securely (not in version control)