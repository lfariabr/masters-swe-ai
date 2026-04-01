# Module 08 — Deployment Case Studies

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| **#** | Task | Status |
|---|------|--------|
| **1** | Read & summarise Amazon Web Services (2022) — eHealth NSW cloud migration | ✅ |
| **2** | Read & summarise Phalip & Niemitz (2020) — Twitter ad analytics on Google Cloud | ✅ |
| **3** | Read & summarise Amazon Web Services (2021) — City of Charles Sturt on AWS | ✅ |
| **4** | Watch & summarise IBM (n.d.) — Innocens BV predictive AI for neonatal care | ✅ |
| 5 | Activity 1: A Cloud Deployment Success Story — Vitaldent discussion forum | 🕐 |
| 6 | Activity 2: Hands-On Lab — Set up and deploy Amazon EC2 Linux instances | 🕐 |
| 7 | Activity 3: Lab Reflections — EC2 configuration reflection post | 🕐 |

---

## Key Highlights

### 1. Amazon Web Services. (2022). eHealth NSW transforms public health system with the cloud.

**Citation:** Amazon Web Services. (2022). *eHealth NSW transforms public health system with the cloud.* https://aws.amazon.com/solutions/case-studies/ehealth-nsw-case-study/

**Purpose:** Documents how NSW Health's ICT arm migrated 10 mission-critical clinical applications from on-premises infrastructure to AWS, realising measurable performance, cost, and workforce improvements.

---

#### 1. The Migration Context

- **eHealth NSW** is the ICT service provider for NSW's public health system — 8.2 million residents, 160,000 staff, 228 hospitals
- Migrated **10 clinical applications** (2021–2022), with a strategy to **refactor** rather than just lift-and-shift — adopting managed AWS services along the way
- Cloud migration was driven by three goals: **operational efficiency**, **patient data access**, and **digital workforce upskilling**

#### 2. Key AWS Services Used

| Service | Purpose |
|---------|---------|
| AWS Security Hub + Amazon GuardDuty | Automated security checks, continuous monitoring, early threat detection |
| Amazon FSx for NetApp ONTAP | Hosts Enterprise Image Repository (EIR) — 1.6 PB of diagnostic images, growing 25%/year |
| Amazon RDS | High availability, encrypted DB, automated patching/backups |
| Amazon Connect | Built a COVID-19 testing call centre in 2 weeks; peaked at 40,000 tickets/week |
| Amazon Pinpoint | SMS bot for COVID test result notifications (from 10 days → hours) |

#### 3. Measured Outcomes

| Metric | Before | After |
|--------|--------|-------|
| Enterprise Patient Records performance | Baseline | **10× improvement** |
| Critical incidents | Baseline | **70% reduction** |
| Time to create new environments | 6–8 weeks | **Under 4 hours** |
| Enhancement delivery speed | Baseline | **50% faster** |
| Cost/benefit recognised | — | **US$16M avoided costs** |
| Clinician productivity recovered | — | **144,000 collective hours** |
| Video conferencing capacity during COVID | Baseline | **18× scale increase** |

#### 4. Workforce Upskilling — Digital Academy

- **Digital Academy (DA)** launched 2020 with 9 pillars: Agile, Cloud, Cybersecurity, Analytics, Human-Centred Design, Integration, Safety & Quality, Service Management, and Customer-first
- AWS added as a multi-technology cloud stream; targets enterprise architects, cloud engineers, clinicians, project managers, and others
- **1,500+ staff** trained by October 2022 (target: majority of 2,000 by 2023)
- Notable outcome: increased confidence in tech among women staff

#### Key Takeaways for CCF501
1. Demonstrates all five NIST cloud characteristics in practice: on-demand provisioning, scalability, measured service, broad access, resource pooling
2. Refactoring vs. lift-and-shift is the difference between moderate and transformational benefit — relevant for Assessment 3 cloud strategy discussions
3. Security (GuardDuty, Security Hub) and compliance are non-negotiable in health data — maps to Module 7's key deployment considerations
4. Staff training is as critical as the technical migration — cloud success is a people and culture challenge, not just a technology one

---

### 2. Phalip, J., & Niemitz, S. (2020). Modernizing Twitter's ad engagement analytics platform.

**Citation:** Phalip, J., & Niemitz, S. (2020, March 19). *Modernizing Twitter's ad engagement analytics platform.* Google Cloud. https://cloud.google.com/blog/products/data-analytics/modernizing-twitters-ad-engagement-analytics-platform

**Purpose:** Details Twitter's two-phase migration of its ad engagement analytics platform from a bespoke on-premises Hadoop stack to a fully managed Google Cloud architecture, achieving billions of events processed in near-real time.

---

#### 1. The Legacy Architecture (Pre-Migration)

- **Input**: Real-time ad engagement events streamed to HDFS as LZO-compressed Thrift files
- **Batch**: Scalding pipelines aggregated data; results stored in **Manhattan** (Twitter's homegrown key-value store)
- **Streaming**: Eventbus (messaging) → Heron (stream processing) → Nighthawk (sharded Redis)
- **Pain points**: Difficult to extend; long-running jobs were unreliable; serving system was expensive and couldn't support large queries

#### 2. First Iteration (2017) — Storage Migration

| Component | Before | After |
|-----------|--------|-------|
| Aggregation | Scalding (on-prem, unchanged) | Scalding (on-prem, unchanged) |
| Ad-hoc/batch storage | Manhattan | **BigQuery** (serverless data warehouse) |
| Serving/APIs storage | Manhattan | **Cloud Bigtable** (low-latency NoSQL) |
| Query service | Expensive legacy system | New service on **GKE**, co-located with Bigtable |
| Serving P99 latency | 2+ seconds | **300 ms** |

- De-risked migration by separating storage migration from business logic migration
- Reliability improved significantly — on-call pages for serving system "rarely, if ever" triggered

#### 3. Second Iteration (2019) — Full Pipeline Migration to Apache Beam / Dataflow

**Why Apache Beam?**
- Built-in **exactly-once semantics** at massive scale across clusters
- **Unified batch + streaming** model — one job codebase handles both inputs (Cloud Storage) and streaming inputs (Pub/Sub)
- Deep integration with BigQuery, Bigtable, and Pub/Sub
- Deployable on **Dataflow** (fully managed)

**New Architecture:**

| Layer | Technology | Scale |
|-------|-----------|-------|
| Data ingestion (streaming) | **Pub/Sub** — two Avro-formatted message streams | 200K + 80K messages/sec |
| Data processing | **4 Dataflow jobs (J0–J3)** running Beam pipelines | 3M+ aggregations/sec |
| Batch layer | Dataflow batch job from Cloud Storage → BigQuery + Bigtable | Dual-write |
| Serving | Cloud Bigtable (unchanged from iteration 1) | Sub-300ms P99 |
| Ad-hoc analysis | BigQuery | Serverless |

**Stream partitioning strategy:**
- High-volume stream split into **6 Pub/Sub topics**, processed by 3 parallel Dataflow jobs
- Hash-based partitioning ensures **per-key grouping is scoped to a single partition** — required for consistent aggregation
- Allows individual job draining/updates without affecting the others
- Horizontal scale path: up to 6 independent jobs if needed

#### 4. Developer Experience Improvements

- Custom **pystachio DSL** for declarative job configuration (tuning, sources, sinks, code location)
- Custom CLI tool automates job updates: drains old job, polls for watermark, launches new job
- Eliminates boilerplate for orchestration — developers focus on transformation logic only

#### Key Takeaways for CCF501
1. Real-world example of cloud agility and scalability — Twitter's platform went from unreliable and expensive to processing 3M+ aggregations/second reliably
2. Phased migration is a risk management strategy — validate gains at each step before committing further
3. Managed services (Dataflow, Pub/Sub, Bigtable) eliminated operational overhead that custom infrastructure was creating — a direct cost and reliability win
4. The move from homegrown tools (Manhattan, Heron, Nighthawk) to managed cloud services illustrates why cloud adoption is often about **reducing complexity**, not just adding features

---

### 3. Amazon Web Services. (2021). The City of Charles Sturt transforms public service delivery for its community using the AWS cloud.

**Citation:** Amazon Web Services. (2021). *The City of Charles Sturt transforms public service delivery for its community using the AWS cloud.* https://aws.amazon.com/solutions/case-studies/city-of-charles-sturt/

**Purpose:** Case study of a South Australian local government council's first full data centre migration to AWS, completed on time and budget despite a global pandemic — with measurable improvements in resilience, security, and agility.

---

#### 1. The Organisation

- **City of Charles Sturt (CCS)**: Council serving 120,000 residents between Adelaide CBD and sea; 550+ staff; Civic Centre at Woodville, works depot, 5 library branches, community centres
- **IT environment**: 80+ applications, 1,700 IT assets, 50 TB of data
- IT partner: **Comunet** — 25-year IT strategy consultancy; AWS Partner

#### 2. The Challenge

| Problem | Detail |
|---------|--------|
| Aging on-premises infrastructure | Significant portion scheduled for replacement |
| Security posture | Needed resilience improvement and cyber security uplift |
| Operational risk | Single-point-person risk and weak disaster recovery practices |
| Innovation gap | Needed cloud agility to support Smart City initiative |
| Resource constraint | ICT team needed to shift from operational to value-add work |

#### 3. The Approach — AWS MAP (Migration Acceleration Program)

- **Lift and Shift** methodology: servers and storage migrated to **AWS Sydney Region**
- Comunet used the **AWS Professional Services MAP Methodology** — based on best practices from hundreds of customer migrations
- Emphasis on skills transfer: CCS wanted to upskill its own team, not just outsource and hand over

#### 4. The Outcome

| Metric | Result |
|--------|--------|
| Applications migrated | **48 applications** |
| Time to migrate | **93 days** |
| Portfolios migrated | Asset Management, City Services, Corporate Services |
| Uptime achieved | **99%** |
| Security guardrails implemented | **35** detective + preventative guardrails |
| AWS security services deployed | **10** (covering IAM, logging, monitoring, infrastructure, data protection) |
| Award | **Local Government IT SA — Excellence in IT Service Delivery (October 2020)** |
| Pandemic context | Completed on time and budget despite COVID-19 hitting mid-project |

#### 5. Cloud Value Drivers Demonstrated

- **Agility**: Faster server provisioning and deployment of new applications
- **Resilience**: 99% uptime + disaster recovery capability
- **Security**: Guardrails and monitoring services previously unavailable on-prem
- **Smart City readiness**: Cloud foundation enables future innovation initiatives

#### Key Takeaways for CCF501
1. Smaller organisations (local government) can achieve enterprise-grade resilience through cloud — cloud democratises access to infrastructure that was previously only viable for large enterprises
2. The AWS MAP methodology provides a structured, low-risk migration path — useful to reference in cloud strategy assessments
3. Agility is a recurring theme across all Module 8 case studies — cloud removes the slow provisioning cycles that constrain on-prem environments
4. Staff upskilling and partnership (Comunet) were as important as the technology — mirrors eHealth NSW's Digital Academy investment

---

### 4. IBM. (n.d.). Innocens BV uses predictive AI to protect the most vulnerable newborns [Video].

**Citation:** IBM. (n.d.). *Innocens BV uses predictive AI to protect the most vulnerable newborns* [Video]. IBM Media Center. https://mediacenter.ibm.com/media/Innocens+BV+uses+predictive+AI+to+protect+the+most+vulnerable+newborns./1_zs73psgr/61201542

**Purpose:** Demonstrates how a Belgian healthcare startup leveraged IBM Cloud and edge computing to build a real-time AI solution that detects neonatal sepsis hours earlier than traditional bedside monitoring, with implications for life-saving intervention.

---

#### 1. The Problem

- **Neonatal sepsis** is a bloodstream infection that is particularly dangerous in premature infants
- Symptoms are subtle; by the time it's clinically obvious, it may be too late for effective intervention
- Traditional monitoring requires continuous bedside observation — human attention is finite and inconsistent
- Innocens founder trained in Sydney and observed: "Nothing changed at the bedside for my patients and parents"

#### 2. The Solution — Edge Computing + Predictive AI

| Component | Description |
|-----------|-------------|
| **Data source** | Real-time vital signs from medical sensors (monitors at the bedside) |
| **Processing** | Edge computing device at the bedside — processes data locally for low latency |
| **AI model** | Machine learning model trained on vital sign patterns correlated to sepsis onset |
| **Cloud platform** | **IBM Cloud** — provides secure data environment and computational power for model training |
| **Output** | Risk score / alert to clinicians when patterns match known sepsis indicators |

#### 3. Performance Metrics

| Metric | Value |
|--------|-------|
| Severe sepsis detection accuracy | **~75%** |
| False alarm rate | **Less than 1 per week** |
| Time saved in diagnosis | **Up to several hours earlier** detection vs. standard care |
| Training data | University Hospital of Antwerp (cross-validated) |

#### 4. Federated Learning — Scaling Without Compromising Privacy

- Different NICUs (Neonatal Intensive Care Units) hold sensitive patient data that cannot be easily centralised
- Innocens + IBM Research are building a **federated learning model**: each centre trains locally; models are **aggregated in IBM Cloud** without sharing raw patient data
- This is a direct application of **cloud + AI for privacy-preserving healthcare at scale**

#### 5. IBM Cloud's Role

- **Trusted infrastructure**: Secure environment for sensitive healthcare data
- **Compute at scale**: Computational power to run heavy ML training iterations quickly
- **Trustworthy AI principles**: IBM's position is that AI in healthcare must be explainable and reliable

#### 6. Human-Centred Design

- Design sprints for the clinical dashboard **involve parents** — not just clinicians
- Surfaces insights about how families interact with health information at the bedside
- Reflects that cloud-hosted AI products must be designed for real human contexts, not just technical performance

#### Key Takeaways for CCF501
1. Edge computing + cloud is a powerful hybrid: data is processed locally for real-time speed, but the cloud handles model training, storage, and federation — connects back to Module 6's edge computing and hybrid models
2. AI-in-cloud is not hypothetical — Innocens shows a production system with measurable life outcomes (75% sepsis detection, <1 false alarm/week)
3. Federated learning is the cloud-native answer to healthcare data privacy — enables cross-institutional learning without centralising sensitive data
4. "Trusted tech partner" (IBM) is a recurring theme — cloud adoption is a partnership, not just a product purchase
