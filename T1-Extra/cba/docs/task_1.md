# CommBank Backend Task - Luis Faria

## Activities Done

1. Created mongodb free cluster
2. Created database 'cba'
3. Created user 'lfariabr' with a secure password
4. Included '0.0.0.0/0' to the cluster in the network access
5. Configured "mongodb+srv" connection string in the Secrets.json file
6. Forked CommBank-Server repository
7. Installed .NET 6.0 SDK
8. Ran the application:
```bash
cd ~/Desktop/sEngineer/masters_SWEAI/T1-Extra/cba/CommBank-Server
dotnet build
dotnet run
```
9. Explored Swagger UI at http://localhost:5203/swagger/index.html
10. Edited Goal.cs file with Icon property:
```csharp
public string? Icon { get; set; }
```
11. Sent a post request to create a goal at /api/goal:
```json
{
    "id": "890f46c78d4f6754dd0f3e11",
    "name": "Travel to Australia",
    "targetAmount": 4000,
    "targetDate": "2025-12-31T00:00:00Z",
    "balance": 320.50,
    "created": "2025-07-04T06:39:00Z",
    "transactionIds": [],
    "tagIds": [],
    "userId": "60d5f6f9d3e2b21f4c8c2f5a",
    "icon": "https://cdn.example.com/icons/australia.png"
}
```
12. Sent a get request to get all goals at /api/goal.
13. Added DotNetEnv package to the project: `dotnet add package DotNetEnv`
14. Added .env file to the project.
15. Edited Program.cs file to load the .env file:
```csharp
Env.Load();
```
16. Changed Secrets.json to .env
17. Updated Program.cs file to use the .env file and Get MongoDB connection string:
```csharp
var connectionString = Environment.GetEnvironmentVariable("MONGODB_CONNECTION_STRING") ?? 
    throw new InvalidOperationException("MongoDB connection string not found in environment variables");
var mongoClient = new MongoClient(connectionString);
```
18. Removed Secrets.json file from the project since it is not needed anymore.

## Result

✔ All steps from the original task have been completed successfully.  
✔ Tested POST and GET operations confirmed the Icon field works as expected.  
✔ No errors remain in the current implementation.

## Github Repo:
[GitHub Repo](https://github.com/lfariabr/masters-swe-ai/tree/master/T1-Extra/cba/CommBank-Server)  
