using CommBank.Models;
using CommBank.Services;
using MongoDB.Driver;
using DotNetEnv;

Env.Load();

var builder = WebApplication.CreateBuilder(args);

// Load environment variables from .env file
Env.Load();

builder.Services.AddControllers();

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Get MongoDB connection string from environment variables
var connectionString = Environment.GetEnvironmentVariable("MONGODB_CONNECTION_STRING") ?? 
    throw new InvalidOperationException("MongoDB connection string not found in environment variables");

var mongoClient = new MongoClient(connectionString);
var mongoDatabase = mongoClient.GetDatabase("CommBank");

IAccountsService accountsService = new AccountsService(mongoDatabase);
IAuthService authService = new AuthService(mongoDatabase);
IGoalsService goalsService = new GoalsService(mongoDatabase);
ITagsService tagsService = new TagsService(mongoDatabase);
ITransactionsService transactionsService = new TransactionsService(mongoDatabase);
IUsersService usersService = new UsersService(mongoDatabase);

builder.Services.AddSingleton(accountsService);
builder.Services.AddSingleton(authService);
builder.Services.AddSingleton(goalsService);
builder.Services.AddSingleton(tagsService);
builder.Services.AddSingleton(transactionsService);
builder.Services.AddSingleton(usersService);

builder.Services.AddCors();

var app = builder.Build();

app.UseCors(builder => builder
   .AllowAnyOrigin()
   .AllowAnyMethod()
   .AllowAnyHeader());

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();

