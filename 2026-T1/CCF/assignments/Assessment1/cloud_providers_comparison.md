# Cloud Providers Comparison — CCF501 Assessment 1 Reference

**Context:** ABC Enterprise migration scenario. AWS selected as primary provider.

---

## 1. AWS Services in the ABC Enterprise Architecture

| Service | Category | What It Does | Justification |
|---|---|---|---|
| EC2 | Compute | Virtual machine instances | Core compute substrate for web/app servers; IaaS baseline |
| Auto Scaling | Compute | Scales EC2 up/down on demand | Absorbed 10× surge with zero manual intervention |
| Elastic Load Balancing (ELB) | Networking | Distributes traffic across EC2 instances | Automates routing + health checks; native Route 53 integration |
| Lambda | Serverless | Event-driven, pay-per-execution compute | Workflow automation (order placed → delivery assigned); scales to zero |
| Route 53 | DNS | Traffic routing and domain management | Already in ABC architecture; native ELB integration signal |
| S3 | Storage | Object storage | Backups, imagery, static assets; 99.999999999% durability |
| RDS | Database | Managed relational database (MySQL/PostgreSQL) | Business data processing with managed patching and backups |
| VPC | Networking | Virtual private network isolation | Multi-tenant isolation, security segmentation |
| CloudFront | CDN | Global content delivery network | Low-latency access for distributed users |
| CloudWatch | Monitoring | Metrics, logs, and observability | Operational visibility; maps to NIST Measured Service |
| Cost Explorer | FinOps | Cost tracking and usage analysis | Validates 80% cost reduction claim; rightsizing recommendations |

---

## 2. NIST Essential Characteristics Mapping

| NIST Characteristic | AWS Services |
|---|---|
| On-Demand Self-Service | EC2, RDS, S3 (provision without human interaction) |
| Broad Network Access | Route 53, CloudFront (accessible over internet via standard mechanisms) |
| Resource Pooling | VPC, EC2 (multi-tenant, location-independent pooled resources) |
| Rapid Elasticity | Auto Scaling (scales in/out automatically on demand) |
| Measured Service | CloudWatch, Cost Explorer (metered usage, transparent reporting) |

---

## 3. Three-Cloud Side-by-Side Comparison

| Feature | AWS | Azure | GCP |
|---|---|---|---|
| **Load Balancing** | Elastic Load Balancing (ALB/NLB) | Azure Load Balancer / Application Gateway | Cloud Load Balancing |
| **Serverless** | Lambda | Azure Functions | Cloud Functions / Cloud Run |
| **VM Compute** | EC2 | Azure Virtual Machines | Compute Engine |
| **DNS** | Route 53 | Azure DNS | Cloud DNS |
| **Object Storage** | S3 | Azure Blob Storage | Cloud Storage |
| **Managed DB** | RDS (Aurora, MySQL, PostgreSQL) | Azure SQL / Cosmos DB | Cloud SQL / Spanner |
| **CDN** | CloudFront | Azure CDN / Front Door | Cloud CDN |
| **Monitoring** | CloudWatch | Azure Monitor | Cloud Monitoring (Operations Suite) |
| **Cost Tools** | Cost Explorer + Budgets | Azure Cost Management | Cloud Billing / Recommender |
| **Ecosystem Fit** | Broadest managed-service catalogue | Deep Microsoft/enterprise integration | Analytics and data-heavy workloads |
| **ABC Alignment** | ✅ Route 53 already in use; ELB + Auto Scaling + Lambda stack | ⚠️ No .NET, Office 365, or Hyper-V signals | ⚠️ No BigQuery or analytics-heavy workload signals |

---

## 4. Why AWS for ABC Enterprise

**Integration signals already present:**
- Route 53 is in the existing ABC architecture → AWS ecosystem lock-in already exists
- Switching to Azure or GCP would require DNS migration with no offsetting benefit

**Best-fit managed-service stack:**
- ELB + Auto Scaling + Lambda form a native, tightly integrated automation layer
- RDS + S3 + CloudWatch = standard managed operations with minimal overhead

**No competitor signals:**
- No Azure indicators: no .NET stack, no Microsoft 365 dependency, no Hyper-V infrastructure
- No GCP indicators: no BigQuery usage, no ML/Analytics-first workload, no Kubernetes-native architecture

**Maturity and support:**
- AWS has the longest cloud track record (since 2006) and the largest partner/support network
- Largest global region footprint for latency-sensitive ABC operations

---

## 5. Cost Model — Three-Tier Hybrid Strategy

| Tier | Mechanism | Discount | Use Case |
|---|---|---|---|
| **1. Reserved Capacity** | 1–3 year reserved instances | 40–60% vs on-demand | Stable baseline (web servers, DB) |
| **2. Pay-as-You-Go** | On-demand pricing | Standard rate | Demand spikes, growth campaigns |
| **3. Spot Instances** | Preemptible spare capacity | Up to 90% off | Background jobs, batch processing |

**Key cost claim:** ABC reduced IT costs by ~80% post-migration — validated via:
- Elimination of on-premises hardware (CapEx → OpEx)
- Auto Scaling avoiding over-provisioning
- Reserved instances for predictable baseline workloads
- Cost Explorer providing rightsizing data

---

## 6. Key Definitions (Quick Reference)

| Term | Definition |
|---|---|
| IaaS | Infrastructure as a Service — user manages OS and above (EC2) |
| PaaS | Platform as a Service — user manages app and data (RDS, Elastic Beanstalk) |
| SaaS | Software as a Service — provider manages everything (fully managed apps) |
| Serverless | FaaS model — no server management, event-driven, pay-per-invocation (Lambda) |
| Auto Scaling | Automatically adjusts compute capacity based on demand signals |
| Elasticity | Ability to scale resources up or down rapidly (NIST characteristic) |
| CapEx | Capital expenditure — upfront hardware investment (on-prem model) |
| OpEx | Operational expenditure — pay-as-you-go (cloud model) |

---

*Reference file for CCF501 Assessment 1 — not a submission artifact.*
