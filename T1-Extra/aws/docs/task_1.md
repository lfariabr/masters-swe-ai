# AWS Solutions Architect Task #1 - Luis Faria

## Context

Before we get started with the task, let's give some more context on Amazon Web Services (AWS). 

AWS provides myriad services for doing all kinds of things! While you don’t need to be familiar with them all, outlined below are a few that give you a sense of what type of services AWS provides and how they are billed. 

Please have a read through the services below and proceed to next step. It's likely that you'll need to use some of this information on the next part of this task - but you can easily navigate back and forth as required! 

### General Services

1. **CodePipeline**
This will build code and can deploy it to various AWS services. It is charged per pipeline. Can be used with Elastic Beanstalk for blue/green no-downtime deployments.

2. **Elastic Load Balancing**
Distributes traffic across application servers, such as EC2, Lambda or Fargate. Can use health checks to know which servers should service requests. Charges are based on the number of hours the load balancer runs and (at a high level) the amount of traffic it services. The actual charging rules can be quite complex.

3. **RDS**
Relational database hosting platform. Charged in the same way as EC2 (i.e. a virtual machine with a set amount of resources). Servers can be resized but must be restarted to do so.

4. **Route 53**
AWS' domain and DNS management.

5. **S3**
Store objects in the cloud. Charged based on the amount of data being stored, how it’s stored, and for retrieval.


### Application Executors

AWS provides a few ways of executing applications, from virtual machines, to container executors to function executors.

1. **EC2**
Scalable virtual servers. Charged based on resources of the virtual servers (RAM, CPU, storage), per hour. Servers can change their resource allocation but must be restarted to apply them.

2. **Fargate**
Run containerized applications (e.g., Docker images). Charges are based on the resources assigned to the container (RAM, CPU, etc.) and how long it runs for. Very scalable but can require manual orchestration.

3. **Lambda**
An application is uploaded to Lambda and only executed when triggered, for example, on HTTP request or via S3. For example, a Lambda instance would run to just service a single HTTP request. Charging is based on the amount of memory the Lambda uses and how long it runs for, plus the number of requests. Sometimes data transfers can also be charged depending on which region(s) a Lambda is fetching data from. Highly scalable up and down. Not suited for serving static content.

4. **Lightsail**
Virtual machines, like EC2 but simpler to set up. Charges are based on the resources of the Lightsail virtual machine. Virtual machines' resources can’t be changed, instead the machines must be cloned to a new instance and restarted. 

5. **Elastic Beanstalk**
Ties together EC2, RDS and Elastic Load Balancing with simple configuration and deployment. Its primary advantage is how it can facilitate the autoscaling of EC2 instances. Billing is based on a combination of the EC2, RDS and ELB that you use. Deployment is made easy with CLI tools, and we can use rolling deployments so there is no downtime. It has support for several languages including Python, NodeJS, Java and Go.

### Availability Zones

For extra redundancy, services can be deployed across multiple availability zones (AZ). This means that requests can fall over from one AZ to another in the case of infrastructure failure. In general, the cost of a service is multiplied by the number of availability zones it’s in.

You should be able to tell the customer why you have chosen Elastic Beanstalk and what components it contains, and the purpose of these. The AWS resource pages for each service contain descriptions of how they are charged.

### Pricing

- CodePipeline
- Elastic Load Balancing
- RDS
- Route 53
- S3
- Elastic Beanstalk

The concrete pricing differs in each region, however, the method of price calculation is the same. For example, an EC2 instance in Region A may cost more than the same instance in Region B, however, both are billed at an hourly rate. The AWS pricing calculator at https://calculator.aws/ can also give some guidance.

---

## Task #1 Description
You receive a client email request
In this task, imagine you are a solutions architect at AWS. A customer has contacted you because they are having some problems with the way their web application is currently hosted.

Here's what the client has to say: 

> To: aws@aws.com
> From: Lilly.sawyer@fastier.com
> Subject: AWS services for Web Application Hosting

Hi,

My name is Lilly Sawyer and I am the co-founder and CTO of Fastier, the online tool that makes organizing things fast.

You may have seen that we have been in the news recently and have been experiencing some big growth as a result. Unfortunately, this means we’ve been having some difficulties with our website. The response times can be slow during peak periods and sometimes we even have server crashes when it runs out of memory. We also experience some downtime during deployments and don’t have a disaster recovery plan. Based on our current trajectory, we predict we’re going to see consistent linear growth for a while.

Our application is a SPA React Application backed by Python and Flask, with PostgreSQL as a database. It all runs off a single AWS EC2 instance currently (t3.medium, 4GB of RAM).

Can you design an architecture for us that will alleviate the problems we’re experiencing? We are not on a strict budget right now, but at the same time, it’s not unlimited.

Kind regards,
Lilly

Your task is to draft an email reply to Lilly Sawyer. So, what should we say back? Click next to find out!

---

### Draft your email to Lilly
Okay let's get started on the email to Lilly. In the email, you will need to show an architecture diagram and explain: 

> - What each part of the architecture is
> - Why it was chosen
> - How the costs are calculated and how they may vary month-to-month 
> Remember you don’t need to give concrete numbers, just an overview!

Your team has come together and decided on the architecture approach. Outlined below is all the information you need to draft your email - you can also refer back to Step 2 to learn about AWS services. 

Read the information and write your response in the text box below. Your response should be approx. 600-700 words. 

We'll show you an example answer on the next step, but we encourage you to give it a go first! 

---

#### First - Your team considers the brief:

When deciding on the right AWS solution, your team considers these points:

> The company is a startup. We are lucky because we can provide more of a greenfield approach, and they are more likely to be able to make changes to their application stack. Compared to an enterprise, where change can take a long time, and they may end up only being able to migrate part of their system at a time.
Again, being a startup, it is probably easy to migrate their data into AWS.
They have a single server and already experience downtime, so they are probably OK with some downtime during migration and setup.
Being a mixed API and web app they will need to host some static content as well.

#### Second - You decide on the solution: 

In this case, we will recommend a solution based on Elastic Beanstalk based on these requirements:

> The customer has a Python application that Elastic Beanstalk has support for.
The customer will need to scale, and this is one of the fundamental features of Elastic Beanstalk.
They want to remove downtime when deploying and Elastic Beanstalk’s Blue/Green deployment can assist with this.
The AWS Elastic Beanstalk documentation provides some more information if you want to learn about it! 


#### Third - Specify the services: 

The services we will use are listed below: 

Route 53
Elastic Load Balancing
Elastic Beanstalk with Autoscaling EC2 Group
RDS
S3
CodePipeline
An additional availability zone for redundancy is proposed but is not necessary.


#### Fourth - Evaluate!

Importantly, the team recognizes that Elastic Beanstalk is not the only product that we could recommend for this customer! AWS is an open platform and encourages creativity when building solutions. We need to be aware of the pros and cons of each solution and how they will best fit each customer.

Other options like Lambda or Fargate can be more complex to set up. Lightsail and EC2 can be easy but they don’t provide that automatic scaling; the customer can end up paying more because they are running virtual machines that are often not at capacity. However, each of these services also has its own advantages, and depending on the application that’s being built we can provide different recommendations and discuss the options more in-depth with the customer before coming up with the final design.

Here is the architecture diagram that your team creates for Lilly:

![Architecture Diagram](T1-Extra/aws/docs/ArchitectureDiagram.png)

**Draft your email here!**  Your response should be approx. 600-700 words.

---

**Subject:** Re: Scaling and Deployment Solutions for Your Python Web Application

Dear Lilly,

Thank you for reaching out to AWS regarding the scaling and deployment challenges you're experiencing with your Python web application. I understand the frustration of dealing with server overload during peak traffic and the operational disruption caused by deployment downtime. 

As a Solutions Architect at AWS, I'm excited to present a solution that will 🔨 crush your pain points while positioning **Fastier** for sustainable growth.

**Recommended Architecture Solution**

After analyzing your requirements, I recommend implementing an **AWS Elastic Beanstalk-based architecture** complemented by several supporting services. Please refer to the attached architecture diagram (ArchitectureDiagram.png) for a visual representation of this solution.

**Core Components and Rationale:**

**1. AWS Elastic Beanstalk**
This will serve as the foundation of your application hosting. Elastic Beanstalk is ideal for your Python application because it:
- Provides native Python runtime support with minimal configuration
- Automatically handles capacity provisioning, load balancing, and health monitoring
- Enables zero-downtime deployments through blue/green deployment strategies
- Offers automatic scaling based on traffic patterns, eliminating your current capacity constraints

**2. Auto Scaling EC2 Group**
Integrated within Elastic Beanstalk, this ensures your application automatically scales up during traffic spikes and scales down during quiet periods, optimizing both performance and costs. You'll never again face the scenario where your single server becomes overwhelmed.

**3. Elastic Load Balancer (ELB)**
This distributes incoming traffic across multiple application instances, providing:
- High availability through health checks and automatic failover
- Improved response times by routing requests to the least loaded servers
- SSL termination capabilities for enhanced security

**4. Amazon RDS (Relational Database Service)**
For your database needs, RDS offers:
- Automated backups and point-in-time recovery
- Multi-AZ deployment for database redundancy
- Automatic scaling and maintenance windows
- Enhanced security with encryption at rest and in transit

**5. Amazon S3**
For static content hosting (CSS, JavaScript, images), S3 provides:
- Virtually unlimited storage capacity
- High durability (99.999999999%)
- Cost-effective storage with multiple storage classes
- Global content delivery when paired with CloudFront

**6. AWS CodePipeline**
This addresses your deployment downtime concerns by:
- Automating your entire deployment process
- Enabling continuous integration and continuous deployment (CI/CD)
- Supporting blue/green deployments for zero-downtime releases
- Providing rollback capabilities if issues arise

**7. Route 53**
AWS's DNS service ensures:
- High availability and reliable domain resolution
- Health checks and automatic failover
- Integration with other AWS services for seamless traffic routing

**Addressing Your Specific Concerns:**

**Scalability:** The auto-scaling capabilities will automatically adjust your infrastructure based on demand, handling traffic spikes seamlessly while reducing costs during low-traffic periods.

**Deployment Downtime:** Blue/green deployments through Elastic Beanstalk and CodePipeline will eliminate deployment-related downtime entirely. Your users will experience uninterrupted service during updates.

**Migration Strategy:**
Given your startup's current single-server setup, migration will be straightforward:
1. We'll help you containerize your Python application
2. Set up the Elastic Beanstalk environment
3. Migrate your database to RDS with minimal downtime
4. Implement the CI/CD pipeline
5. Gradually shift traffic to the new infrastructure

**Cost Optimization:**
This solution follows AWS's pay-as-you-use model. During low traffic periods, you'll only pay for minimal resources, while automatic scaling ensures you can handle growth without over-provisioning.

**Next Steps:**
I'd be delighted to schedule a technical consultation to discuss implementation details, timeline, and provide a detailed cost estimate based on your specific traffic patterns and requirements.

Please don't hesitate to reach out with any questions. We're committed to ensuring your transition to AWS is smooth and your application is positioned for scalable success.

Best regards,

Luis Faria  
Solutions Architect  
Amazon Web Services  
luis.faria@aws.com

---

## Activities To Do

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
https://www.youtube.com/watch?v=qDAgkOuijUg```
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
[GitHub Repo](https://github.com/lfariabr/masters-swe-ai/tree/master/T1-Extra/aws)  
