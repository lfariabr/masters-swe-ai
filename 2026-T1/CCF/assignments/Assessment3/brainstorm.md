# CCF501 Assessment 3 — Deployment Brainstorm

## Key Decision: Provider First

**Use Azure.** Dr. Bhagwan + Dr. Shen explicitly recommended Azure as the certification target
over AWS/GCP (meeting 2026-03-18). This assessment is free reps — every screenshot builds
AZ-900/DP-900 muscle memory before the exams.

---

## App Options

### Option A — Metabase on Azure
**Safest, strongest submission**

**What it is:** Open-source BI platform. Point it at a database, it generates dashboards,
charts, and ad-hoc queries through a clean UI. Self-hosted alternative to Tableau/Power BI.

**Why it fits:**
- Currently working as a Data Analyst at St Catherine's School — building SQL Server pipelines
  and reporting workflows in an educational environment
- Metabase is the cloud-native version of that exact work
- Can connect to a PostgreSQL instance (same Azure resource group) and populate with synthetic
  data from previous projects (healthcare clinic data from ClinicTrendsAI/Research Proposal)
- The deployment mirrors real infrastructure decisions made professionally

**How the report looks:**

*Introduction (~100w):* "This report documents the deployment of Metabase, an open-source
analytics platform, on Microsoft Azure — selected to align with a Data Engineer career
trajectory and Azure certification roadmap (AZ-900). The deployment mirrors analytics
infrastructure patterns used in production educational environments."

*Background (~200w):* Cloud computing enabling data-driven decision-making, IaaS + PaaS
service models, public cloud deployment model. Brief comparison: on-premises BI vs
cloud-hosted analytics — connects NIST characteristics (on-demand self-service, measured
service) to the deployment context.

*2a — Provider rationale:* Azure wins on data/ML integration (Azure SQL, Synapse),
certification alignment, and free-tier VM availability. Short comparison table:
AWS RDS vs Azure SQL vs GCP Cloud SQL for a data workload.

*2b — Block diagram:*
```
Azure Resource Group
  └── VNet + Subnet
        └── NSG (allow 22, 80, 3000 / deny all else)
              └── Ubuntu VM
                    └── Docker: Metabase container (port 3000)
                          └── Azure Database for PostgreSQL
```

*2c — Deployment procedure:* 4 clean tasks with screenshots — resource group creation,
VNet + subnet config, NSG inbound rules, Metabase running on port 3000 with login screen.

*2d — Security:* NSG rules (deny-all default, explicit allow on 80/443/22), Metabase
built-in user auth, connection string secrets (env vars, not hardcoded), principle of
least privilege. Can cross-reference CuraNexus Secure-by-Design project for credibility.

*2e — Application analysis:* Current setup is single VM (SPOF). Production improvements:
Azure Load Balancer, managed PostgreSQL with automated backups, SSL via Let's Encrypt,
private endpoint instead of public IP. Ties to ISY503 cloud security content.

**Ratings:**
- Deploy complexity: Low (Docker image, ~15 min)
- Screenshot appeal: High (clean dashboard UI)
- Security section: Easy (NSG + built-in auth)
- Portfolio fit: Strong (data engineering + current job)
- Report score estimate: **8/10**

---

### Option B — Apache Superset on Azure
**Most impressive portfolio piece**

**What it is:** Open-source data exploration and visualisation platform by Apache (originally
Airbnb). More powerful than Metabase — SQL Lab (raw queries), 40+ chart types, role-based
access control, connects to Snowflake, BigQuery, PostgreSQL, and more. Python-native,
Docker-based.

**Why it fits:**
- Python-native (primary language)
- More technical setup than Metabase — more impressive to anyone reading the portfolio
- Nobody in the cohort is deploying Superset — off the brief's suggested list entirely
- Directly relevant to T4 Big Data & Analytics (BDA601, T1-2027)
- Azure Synapse Analytics uses a similar architectural pattern that Superset integrates with

**How the report looks:**

Same structure as Metabase but with stronger technical depth:

*2a — Provider rationale:* Same Azure argument + add that Azure Synapse Analytics mirrors
the Superset integration architecture — forward-looking to T4. Short table: self-hosted
Superset vs Tableau Cloud vs Power BI Embedded (cost, openness, portability).

*2d — Security:* Superset's RBAC is richer than Metabase — document multiple user roles
(Admin, Alpha, Gamma), row-level security, and how these map to the IT governance rubric
criteria. The 20% governance criterion writes itself here. Strong section.

*2e — Application analysis:* Superset in production needs Celery workers + Redis for async
queries — propose this as the robustness improvement. Already built a Redis/Celery
architecture in Konquista, so the analysis is grounded and credible, not theoretical.

**Ratings:**
- Deploy complexity: Medium (Docker Compose with multiple services)
- Screenshot appeal: High (SQL Lab + dashboards look great)
- Security section: High (RBAC gives rich governance content)
- Portfolio fit: High (differentiator + feeds T4 directly)
- Report score estimate: **9/10**

---

### Option C — MLflow on Azure
**Best 18-month portfolio thread**

**What it is:** ML experiment tracking server + model registry. Log runs, parameters,
metrics, and artifacts. Industry standard for teams doing ML at scale. Track which model
version performed best, serve models to production.

**Why it fits:**
- Machine Learning (MLN601) and Deep Learning (DLE602) start T2-2026
- Deploying MLflow now = infrastructure ready for the next two subjects
- Every experiment run in those subjects can log to this Azure-hosted MLflow server
- Portfolio narrative spans three subjects across two terms — rare longitudinal coherence
- ISY503 (current) work can retroactively be logged to the server

**How the report looks:**

*Introduction:* "Deployed MLflow, an open-source ML experiment tracking platform, on
Microsoft Azure — provisioning MLOps infrastructure that will support ML coursework in
Machine Learning (MLN601) and Deep Learning (DLE602) subjects commencing T2-2026."

*Background:* Richer than other options — ML lifecycle, cloud compute for model training,
how IaaS enables scalable ML workloads. Directly bridges ISY503 and upcoming subjects.

*2d — Security (hardest section):* MLflow has minimal built-in auth — requires nginx
reverse proxy with basic auth or Azure AD integration. More complex to implement but
creates a stronger governance narrative: you had to *design* the security layer rather
than configure existing settings. Higher effort, higher rubric reward.

*2e — Application analysis:* Natural progression — Azure ML managed training jobs, Azure
Blob Storage for artifact storage, auto-scaling compute clusters for model training.
Strongest future-state section of all three options.

**Ratings:**
- Deploy complexity: Medium-High (nginx reverse proxy required for auth)
- Screenshot appeal: Medium (functional UI, not as visual as BI tools)
- Security section: Lower out-of-box, higher if nginx layer is added
- Portfolio fit: High (MLOps narrative, 3-subject thread)
- Report score estimate: **8.5/10**

---

## Comparison Table

| Criterion | Metabase | Superset | MLflow |
|---|---|---|---|
| Deploy complexity | Low | Medium | Medium-High |
| Screenshot appeal | High | High | Medium |
| Security section ease | High | High | Requires extra work |
| Portfolio differentiation | Medium | High | High |
| Ties to current job (St Catherine's) | Strong | Strong | Partial |
| Ties to upcoming subjects | Partial | T4 BDA601 | ML + DL (T4) |
| Off the brief's suggested list | Yes | Yes | Yes |
| Recommended provider | Azure | Azure | Azure |

---

## Decision Framework

**Choose Metabase if:** you want the safest, strongest submission with minimal deployment
risk — report practically writes itself, directly tied to current job.

**Choose Superset if:** you want the most impressive portfolio piece — harder to set up,
nobody else is doing it, security and robustness sections hit HD criteria cleanly, and
it feeds directly into BDA601.

**Choose MLflow if:** you're thinking about the 18-month picture — infrastructure pays
dividends across three future subjects, strongest longitudinal narrative in the portfolio.

---

## Common Report Skeleton (all options)

```
1. Introduction (~300w total)
   1.1 Introduction (~100w) — provider selection rationale
   1.2 Background (~200w) — cloud computing context, IaaS, public cloud model

2. Body (~1,000w) — five subsections from Part 2
   2a. Service Provider Selection Rationale + comparison table
   2b. Deployment Model + block diagram (Mermaid)
   2c. Deployment Procedure + screenshots (4 tasks)
   2d. Security Policies + NSG/firewall screenshots
   2e. Application Analysis + robustness improvements

3. Conclusion (~200w)

References (10–12 APA)
Appendices (deployment checklist, glossary)
```

**Submission:** `studentID_CCF501_Assessment 3.docx` — due 06 May 2026
**Screencast required:** cloud dashboard showing deployment steps + login credentials + public IP
