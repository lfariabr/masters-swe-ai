# CommBank Testing Task - Luis Faria

# Description
Icons are supported in code! But before you can land your changes, you need to cover them. This series of tasks will onboard you to our testing patterns. You will use the xUnit testing framework to cover your changes. After getting all test cases to pass, upload a file with your changes to GoalControllerTests.cs.

# Activity Status
1. Cover the `GetGoalsForUser` route
> If You Get Stuck: https://github.com/fencer-so/commbank-program/blob/master/tasks/4_tests/cover_get_for_user.md
2. Run `cd /Users/luisfaria/Desktop/sEngineer/masters_SWEAI/T1-Extra/cba/ && dotnet test CommBank.Tests` or just `dotnet test` in the root directory
3. Submit the file for analysis


## Tips
a. To run the server:
```bash
cd ~/Desktop/sEngineer/masters_SWEAI/T1-Extra/cba/CommBank-Web
npm start
```
b. To run the client:
```bash
cd ~/Desktop/sEngineer/masters_SWEAI/T1-Extra/cba/CommBank-Server
dotnet build
dotnet run
```

## Github Repo:
[GitHub Repo](https://github.com/lfariabr/masters-swe-ai/tree/master/T1-Extra/cba/CommBank.Tests)  

# Task original description
---
## Cover The `GetGoalsForUser` Route
- [X] Arrange and Act using `Get` as a model
- [X] Assert that:
    - [X] `result` is not null
- [X] For each `goal` in `result`, assert that:
    - [X] It is assignable from `Goal`
    - [X] It has the expected `UserId`


```cs
public class GoalControllerTests
{
    private readonly FakeCollections collections;

    public GoalControllerTests()
    {
        collections = new();
    }

    // ...

    [Fact]
    public async void GetForUser()
    {
        // Arrange
        var goals = collections.GetGoals();
        var users = collections.GetUsers();
        IGoalsService goalsService = new FakeGoalsService(goals, goals[0]);
        IUsersService usersService = new FakeUsersService(users, users[0]);
        GoalController controller = new(goalsService, usersService);

        // Act
        var httpContext = new Microsoft.AspNetCore.Http.DefaultHttpContext();
        controller.ControllerContext.HttpContext = httpContext;
        var result = await controller.GetForUser(goals[0].UserId!);

        // Assert
        Assert.NotNull(result);

        var index = 0;
        foreach (Goal goal in result!)
        {
            Assert.IsAssignableFrom<Goal>(goal);
            Assert.Equal(goals[0].UserId, goal.UserId);
            index++;
        }
    }
}

```