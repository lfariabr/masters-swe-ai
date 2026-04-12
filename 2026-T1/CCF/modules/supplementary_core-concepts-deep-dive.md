# Supplementary — Cloud Computing Core Concepts Deep Dive

**Source:** Be A Better Dev. (2023). *Cloud computing explained: The most important concepts to know* [Video]. YouTube. https://www.youtube.com/watch?v=ZaA0kNm18pE  
**Covers:** Scaling · Load Balancing · Autoscaling · Serverless · Event-Driven Architecture · Container Orchestration · Storage · Availability · Durability · IaC · Cloud Networks

---

## 1. Scaling → *Modules 3, 7*

Two approaches to handle traffic spikes:

| | Vertical Scaling | Horizontal Scaling |
|---|---|---|
| **How** | Beef up one machine (more CPU, RAM, storage) | Clone the app across many smaller machines |
| **Cost** | Diminishing returns — gets expensive fast | Cheaper; add/remove as needed |
| **Stability** | Single point of failure — machine dies, app dies | Other instances absorb the load |
| **Cloud fit** | Legacy approach; still possible | The modern standard |

> Horizontal scaling is why cloud computing exists. Vertical scaling is what you did before it.

---

## 2. Load Balancing → *Modules 3, 7*

Sits in front of horizontally scaled instances. Has its own DNS/IP. Distributes incoming traffic across healthy instances only.

**Three routing algorithms:**
- **Round robin** — cycles through instances one by one
- **Least connections** — sends to whichever instance has fewest active connections
- **Least utilisation** — sends to whichever instance has lowest CPU/resource usage

> Load balancer + horizontal scaling = the foundation of availability.

---

## 3. Autoscaling → *Modules 3, 6, 7*

Automatically adds or removes instances based on a metric threshold — no manual intervention.

- Set a baseline (e.g. 3 instances)
- Define a trigger metric (connections, CPU %, memory)
- When traffic spikes → new instance spins up
- When traffic drops → instance tears down (saves cost)

In AWS: **Auto Scaling Groups** (ASGs). You define min/max instance counts and the scaling metric.

---

## 4. Serverless → *Module 4, 6*

**Original meaning (AWS Lambda model):**
- Write your function → upload it → Lambda handles *everything* underneath (provisioning, scaling, patching)
- You pay per execution, not per running instance
- You have zero visibility of the underlying EC2 machines

**Current (diluted) meaning:**
- AWS now calls services like OpenSearch Serverless "serverless" even though you still pay for underlying instances — you just don't *manage* them
- Still auto-scales, but cost model is different

**Rule of thumb:** True serverless = pay per invocation (Lambda, DynamoDB). "Managed serverless" = you don't manage infra but still pay for it running (OpenSearch Serverless, Aurora Serverless).

---

## 5. Event-Driven Architecture (EDA) → *Module 6*

**Old model — Request/Response (tight coupling):**
- Service A calls Service B, waits for response, then calls Service C
- A needs to know B and C exist; if C breaks, everything breaks

**New model — Event-Driven (loose coupling):**

```
Producer → SNS Topic / Event Bus → [Subscriber 1]
                                  → [Subscriber 2]
                                  → [Subscriber N]
```

- Producer fires a message ("order placed") and moves on
- Any number of subscribers consume it independently
- Adding a new subscriber = no change to the producer

**Key terms:**
- **Publisher** — produces the event (e.g. order service)
- **Subscriber** — consumes the event (e.g. fraud service, fulfilment service, billing)
- **Pub/Sub** — the pattern
- **Fan-out** — one message → many consumers
- **AWS services:** SNS (Simple Notification Service), EventBridge

**Trade-off:** Loose coupling introduces eventual consistency — if fraud detection flags an order *after* fulfilment started, you need compensating events to reverse it.

---

## 6. Container Orchestration → *Module 6*

**Problem:** Deploying a container manually to EC2 = you manage restarts, health checks, load balancing, deployments. Pain.

**Solution:** Orchestration services do all of that automatically.

| AWS Service | What it is |
|---|---|
| **ECS** (Elastic Container Service) | AWS-native container orchestration |
| **EKS** (Elastic Kubernetes Service) | Kubernetes managed by AWS |

Both give you:
- Deploy across N machines with one command
- Automatic health checks + restart on failure
- Built-in load balancer integration
- Easy rolling deployments (no downtime updates)

---

## 7. Storage → *Modules 4, 6*

Three distinct storage types in cloud:

| Type | What it stores | AWS example | When to use |
|---|---|---|---|
| **Object storage** | Files, media, JSON, CSVs, blobs | S3 | General-purpose; anything you'd dump in a folder |
| **Block storage** | Volumes attached to instances (like a hard drive) | EBS | Databases, OS disks, ML data jobs |
| **Databases** | Structured/semi-structured queryable data | RDS, DynamoDB, ElastiCache | Application data |

**Database sub-types:**
- **Relational (SQL):** PostgreSQL, MySQL, SQL Server — strict schema, ACID guarantees
- **NoSQL:** DynamoDB, MongoDB, OpenSearch — flexible schema, horizontally scalable
- **Cache:** Redis, Memcached — in-memory, ephemeral, ultra-fast reads

---

## 8. Availability → *Modules 3, 7*

How often your app is up. Measured as a percentage:

| SLA | Max downtime per year |
|---|---|
| 99.9% ("three nines") | ~8.7 hours |
| 99.99% ("four nines") | ~52 minutes |
| 99.999% ("five nines") | ~5 minutes |

**How to improve it:**
- Horizontal scaling + load balancing (instances absorb each other's failures)
- Deploy across **Availability Zones (AZs)** — physically separate data centres with independent power + networking within the same region
- Multi-region deployments for extreme resilience

---

## 9. Durability → *Modules 3, 7*

Not the same as availability. Durability = will your data survive?

- Cloud providers store **multiple copies** of your data across different machines, AZs, sometimes regions
- If one copy is lost (hardware failure, fire, "data centre goes nuclear") → auto-replicated from another copy
- AWS S3 durability: **99.999999999%** (11 nines) — designed to lose 1 object per 10 million stored per 10,000 years

> **Availability** = is the service up? **Durability** = is the data still there?

---

## 10. Infrastructure as Code (IaC) → *Modules 6, 7*

**Problem with manual console provisioning:**
- Easy to fat-finger config in production
- Impossible to replicate exactly across regions/environments
- No audit trail, no code review

**IaC solution:** Define all infrastructure as code, check it into git, review it like any other code change.

| Tool | Type | Notes |
|---|---|---|
| **CloudFormation** | Declarative (YAML/JSON) | AWS-native; verbose |
| **CDK** (Cloud Development Kit) | Imperative (Python, TypeScript, etc.) | AWS-native; loops, conditions, real code |
| **Terraform** | Declarative (HCL) | Cloud-agnostic; works with AWS, Azure, GCP |

**Best pick:** CDK for AWS-only; Terraform for multi-cloud.

---

## 11. Cloud Networks (VPC) → *Modules 3, 7*

In the old world: physical server room, manually managed subnets and firewalls.

In the cloud: **VPC (Virtual Private Cloud)** — your own isolated network inside AWS.

```
AWS (the whole cloud)
├── Your VPC
│   ├── Public subnet  → internet-facing (web servers, load balancers)
│   └── Private subnet → internal only (databases, sensitive data)
├── Friend's VPC       → can be peered to yours if needed
└── Jeff's VPC         → completely isolated by default
```

**Key concepts:**
- **Subnets** — divide your VPC into public (internet-accessible) and private (internal-only) zones
- **Security Groups** — firewall rules at the instance level (e.g. "DB can only receive traffic from app servers, not from the internet")
- **VPC Peering** — connect two VPCs so they can communicate privately
- By default, VPCs are completely isolated from each other and from the internet — you explicitly open what you need

---

## CCF Module Cross-Reference

| Concept | Most relevant CCF module |
|---|---|
| Vertical vs horizontal scaling | Module 3 — Deployment Models |
| Load balancing | Module 3 — Deployment Models |
| Autoscaling | Module 3, 7 |
| Serverless / FaaS | Module 4 — Service Models (extends SaaS/PaaS/IaaS) |
| Event-driven architecture | Module 6 — Advanced Cloud Models |
| Container orchestration | Module 6 — Advanced Cloud Models |
| Object / block / database storage | Module 4 — Service Models |
| Availability + AZs | Module 7 — Key Considerations |
| Durability | Module 7 — Key Considerations |
| Infrastructure as Code | Module 6, 7 |
| VPC / Cloud Networks | Module 3 — Deployment Models |
