# Module 3 — Big Data Integration and Storage

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Foote (2019) — Big Data Integration 101: What, Why, How | ✅ |
| **2** | Read & summarise Dong & Srivastava (2015) — Traditional Data Integration (Ch. 1 §1.1) | ✅ |
| 3 | Read & summarise Pasupuleti & Purra (2015) — Data Integration, Quality & Enrichment (Ch. 3) | 🔥 WIP — needs manual ebook access (EBSCO) |
| **4** | Read & summarise AWS / Baker (2019) — Data Lake Storage: S3 + ADLS Gen2 | ✅ |
| **5** | Read & summarise Siddiqa et al. (2017) — Big Data Storage Technologies: A Survey | ✅ |
| 6 | Activity 1: Discussion Forum — Cost models of AWS S3 vs ADLS Gen2 | 🔥 draft ready — see [module03_activities.md](module03_activities.md) |
| 7 | Activity 2: Interactive Knowledge Check | 🔥 prep checklist ready — see [module03_activities.md](module03_activities.md) |

---

## Where Module 3 sits (the through-line)

Module 2 stopped at the **intake tier** (Source → Transient → Raw). Module 3 is the **management tier** of the data lake: once raw data has landed, you must give it a **unified, trustworthy, queryable view** and then **store it** so it stays performant, scalable, secure and cheap. Two halves:

- **Integration** (R1, R2, R3): combine autonomous, conflicting sources into one consistent view — *schema alignment → record linkage → data fusion*, then enrich.
- **Storage** (R4, R5): land the integrated result in a **data hub** — cloud lake storage (S3 / ADLS Gen2) over a NoSQL taxonomy chosen via the **CAP trade-off**.

> 🔴 **A1 hook:** this is the **SLO b)** content (sourcing → integration → storage backbone). Your *Design a Data Pipeline* report needs an integration step (how do you reconcile sensor + reference data?) and a storage choice (which engine, and *why* — consistency or availability?).

---

## Key Highlights

### 1. Foote, K. D. (2019). Big Data Integration 101: The What, Why, and How.

**Citation:** Foote, K. D. (2019, February 27). *Big data integration 101: The what, why and how.* DATAVERSITY. https://www.dataversity.net/big-data-integration-101-the-what-why-and-how/

**Purpose:** A plain-language primer on *why* integration is the unglamorous-but-essential step that must happen **before** any analytics, the tools that do it, and the five recurring challenges that sink integration projects.

---

#### 1. What Big Data Integration is
- **Definition:** combining data from a variety of **different sources and software formats**, then presenting users with a **translated and unified view**.
- It blends **traditional, social media, IoT, and transactional** data. Data that is *not compatible or not transformed* is "essentially useless" for the project.
- **Payoff:** integrated data → more confidence in decisions + superior insights.
- 🔑 **CTO John Thielens (Cleo):** "*before any analytics can be performed, data integration has to happen*" — data must be **sourced, moved, transformed, and provisioned** to users, securely, all along the way.

#### 2. Why it matters / the ETL → ELT shift
- Traditional warehouses use **ETL (extract, transform, load)**; those tools are evolving to handle big data's **volume + unstructured variety**.
- **Batch + real-time** integration across many sources is the useful combination (e.g. pharma merging an **MDM** system with prescription-outcome big data).
- Cloud option: **iPaaS** (integration Platform-as-a-Service), pulling from SaaS sources. **MDM** systems promote reliable, consolidated data.
- 🔵 **CEO Mike Tuchen (Talend):** a "*once-in-a-generation shift*" — firms drop legacy integration for **agile solutions optimized for Hadoop** (the ETL→ELT-on-Hadoop trend).

#### 3. The 5 challenges of Big Data Integration

| Challenge | What goes wrong |
|---|---|
| **Finding staff** | Shortage of experts fluent in relational + in-memory + NoSQL + Hadoop. |
| **Bringing in the data** | Extracting from an extensive range of sources needs real skill. |
| **Synchronization** | Sources use different schedules/rates → data **desyncs** from origin; extraction/migration/transformation all promote desync. |
| **Data management tools** | Incompatible **NoSQL approaches** (hierarchical-object vs key-value) cause confusion; tool choice needs forethought. |
| **Choosing a strategy** | Teams leap project-to-project breaking **data silos** with no plan; a *true integration strategy* is required. |

- 🔴 **Big picture:** treat **performance, data governance, and security** as **core constituents** from the **logical architecture → physical deployment**. Bolt them on later and you pay for it. (Same "governance is not optional" lesson as the lake-vs-swamp point in Module 2.)

#### 4. Big Data databases (recognise the names)

| Engine | Strength | Weakness |
|---|---|---|
| **Cassandra** | Extremely scalable, decentralised, redundant; Hadoop + MapReduce support | Limited retrieval options; occasionally unpredictable performance |
| **Hadoop** | Structured **and** unstructured, cost-efficient (open source), fast; auto-backup | No built-in security; poor at "small" data |
| **HBase** | Consistency, sharding, failover, load sharing | Slow HMaster recovery; weak querying, single index per table |
| **MongoDB** | Fast document store, ACID-ish, auto-failover, auto-sharding, easy queries | No JOINs, no transactions; memory limits from indexing |

#### Key Takeaways for BDA601
1. **Integration precedes analytics** — this is the conceptual spine of the whole module (and of A1's middle step).
2. The five challenges map directly onto **veracity + governance** themes you already met; "performance, governance, security from day one" is a quotable design principle.
3. The engine table previews **R5's taxonomy** — Cassandra/HBase = column, MongoDB = document — so read R1 as the "intuition" and R5 as the "rigorous version".

---

### 2. Dong, X. L. & Srivastava, D. (2015). Big Data Integration — Ch. 1 §1.1: Traditional Data Integration.

**Citation:** Dong, X. L., & Srivastava, D. (2015). *Big data integration.* Synthesis Lectures on Data Management, 7(1), 1–198. Morgan & Claypool. https://www.morganclaypool.com/doi/suppl/10.2200/S00578ED1V01Y201404DTM040/suppl_file/dong_Ch1.pdf

**Purpose:** Shows, via a concrete **Flights** example, that integration is hard *even for a handful of structured sources* — and names the **three-step pipeline** every integration system uses. This is the rigorous backbone behind R1's friendly overview.

---

#### 1. The goal and why it's hard
- **Data integration = providing unified access to data residing in multiple, autonomous data sources.** Easy to state, "notoriously hard" to achieve — even for a few structured sources.
- **Value explodes when data is linked/fused** with other data — the query *"for each flight number, average the delay between scheduled and actual departure over the past month"* is answerable over the **integrated** database but **not from any single source**.

#### 2. The Flights example — 5 autonomous sources
- **Airline1, Airline2** (per-airline schedules + flights), **Airport3** (departures/arrivals at one airport), **Airfare4** (comparison-shopping fares), **Airinfo5** (reference: airport & airline codes).
- Each is useful alone; integrated, they answer questions none can alone (e.g. airlines learn delay causes from airport gate/takeoff times; the fare site adds on-time stats for customers).

#### 3. Three integration problems → three pipeline steps ⭐ (memorise this)

| Step | Solves the problem of… | What it produces |
|---|---|---|
| **1. Schema Alignment** | **Semantic ambiguity** — same concept modelled differently (or different concepts modelled alike) | A **mediated schema** (unified view) + **attribute matching** + **schema mapping** to reformulate queries |
| **2. Record Linkage** | **Instance-representation ambiguity** — same entity written differently | A **partitioning of records** where each partition = one distinct real-world entity |
| **3. Data Fusion** | **Data inconsistency / quality** — sources give conflicting values | A decision on the **true value(s)** for each data item |

- **Semantic ambiguity example:** `Departure Time` means *gate* time in Airline1 but *takeoff* time in Airline2; `Departure Date` means *actual* date in one source, *scheduled* date in another.
- **Instance ambiguity example:** flight numbers as digits (`49`) vs alphanumerics (`A1-49`); airports as 3-letter codes (`EWR`) vs strings (`Newark Liberty`) → may need **approximate string matching**.
- **Inconsistency example:** conflicting actual-arrival dates (mis-typing, out-of-date copies). Fusion decides which to trust.
- 🔴 **Scale trap:** record linkage can't compare *every pair* of records when there are **billions** — this is exactly where "big data" breaks traditional methods.

#### 4. Traditional → Big Data Integration (BDI)
- BDI differs along the **V dimensions**: not just huge *volume per source* but the **number of sources** grows to **tens–hundreds of thousands** in a single domain (e.g. every airline + airport worldwide).
- Same three steps remain, but **Volume, Velocity, Variety, Veracity** each make alignment/linkage/fusion dramatically harder.

#### Key Takeaways for BDA601
1. **Schema alignment → record linkage → data fusion** is the single most exam-quotable structure in this module. Learn it cold.
2. It gives A1 a concrete **integration step**: if your pipeline ingests sensor data + a reference table, *name* the alignment/linkage/fusion you'd perform.
3. The Vs reframed as *integration* difficulties tie Module 1's 6 V's directly to Module 3's mechanics.

---

### 3. Pasupuleti, P. & Purra, B. S. (2015). Data Lake Development with Big Data — Ch. 3: Data Integration, Quality & Enrichment. 🔥 WIP

**Citation:** Pasupuleti, P., & Purra, B. S. (2015). *Data lake development with big data* (Ch. 3, pp. 51–77). Packt. (EBSCO eBook — Torrens institutional login required.)

**Status:** Not summarised yet — this is an **EBSCO eBook behind authentication**, so there is no local copy to extract. To complete: open via the Torrens library proxy, export Ch. 3, drop the PDF/text into this folder, then re-run `/study-mode BDA 3`.

**What it covers (from the resource brief — to verify on read):** the data lake's **management tier** — the second component after intake. It decomposes data management into sub-tasks (**integration, cleaning/quality, enrichment**), gives approaches/techniques for each, stresses **enrichment** (augmenting data with new attributes to ease later analytics), and surveys tools for big data integration. This is the textbook companion that turns R1/R2's *concepts* into the lake's *architecture*, and it sets up the **data hub** (storage) covered by R4/R5.

> 🔗 Reconciles with Module 2: intake tier (Mod 2) → **management tier** (this chapter) → consumption tier (Mod 5+).

---

### 4. AWS & Baker, J. (2019). Data Lake Storage — Amazon S3 + Azure ADLS Gen2.

**Citation:** Amazon Web Services. (n.d.). *Data lake storage on AWS.* https://aws.amazon.com/products/storage/data-lake-storage/ · Baker, J. (2019, February 14). *Under the hood: Performance, scale, security for cloud analytics with ADLS Gen2.* Microsoft Azure Blog.

**Purpose:** The two industry-standard **cloud data-lake storage** services — the "data hub" of the management tier. Read together they show the four things lake storage must deliver: **performant, scalable, secure, cost-effective**.

---

#### 1. Amazon S3 as a data lake foundation
- **S3 = the lake foundation:** unmatched **durability, availability, scalability, security, compliance, audit**; "more than 1,000,000 data lakes run on AWS".
- **Break down silos** → store **all** data from any source **in its original format**, then query directly.
- Supporting cast: **Lake Formation** (build secure lakes in days), **Glue** (serverless integration — ingest real-time *or* batch, **crawl/catalog/index**, transform), **Athena** (query), **EMR** (processing), **DataZone** (governance).
- 4 benefits: **store all data** · **increase innovation** (more data → better ML/predictions) · **best tool for the job** (purpose-built services) · **eliminate server management** (serverless).

#### 2. Azure ADLS Gen2 — under the hood
- **Purpose-built for big data analytics**, priced at object-storage rates, no silos.
- 🔑 **Hierarchical Namespace (HNS):** arranges data like a **filesystem of directories**. Analytics engines (Spark, Hive) assume a hierarchical FS; the classic "rename temp dir on job completion" is an **O(n) copy+delete** on plain object stores but a **single atomic metadata operation** in ADLS → big speed-up.
- **ABFS driver** (Azure Blob Filesystem, part of Apache Hadoop): optimised for **large-IO throughput** → less compute needed.
- **Scalable:** built on Azure Blob (EB scale); analytics frameworks **scale horizontally** (add nodes) only if **storage scales linearly too** — ADLS does (100s of PB).
- **Secure:** Azure AD **OAuth** auth · **RBAC + POSIX ACLs** (same ACL mechanism as Hadoop) · **encryption at rest & in transit (TLS 1.2)** · **storage firewalls** at packet level.
- Fits the **Modern Data Warehouse** pattern: HDInsight/Databricks (process), Data Factory (ingest/orchestrate), Synapse/Analysis Services, Power BI (consume).

#### 3. The shared principle
- 🔴 **"Performance is the #1 driver of value":** a faster storage layer → **less compute** (the expensive part) → insights sooner **and** cheaper. This is the economic argument for picking lake storage well.
- Both stress **separation of storage and compute** (echo of Module 1's Hadoop lesson) and **governance/catalog/security as first-class**, not afterthoughts.

| | AWS | Azure |
|---|---|---|
| **Lake store** | Amazon S3 | ADLS Gen2 (on Azure Blob) |
| **Governance/catalog** | Lake Formation + Glue + DataZone | Azure AD + RBAC/ACLs |
| **Key perf trick** | Glue serverless integration | **Hierarchical Namespace** (atomic rename) + ABFS |
| **Analytics** | Athena, EMR, Redshift | HDInsight, Databricks, Synapse |

#### Key Takeaways for BDA601
1. This **is** the data-lake **storage / data-hub** layer — the destination of the integration pipeline. Cite **one** concrete service in A1's storage step.
2. **"Performance → less compute → lower cost"** is the design rule that justifies your storage choice in the report.
3. Directly feeds **Activity 1** (compare S3 vs ADLS **cost models**) — note S3's pay-for-what-you-store + tiers vs ADLS's object-rate pricing + HNS efficiency.

---

### 5. Siddiqa, A., Karim, A. & Gani, A. (2017). Big Data Storage Technologies: A Survey.

**Citation:** Siddiqa, A., Karim, A., & Gani, A. (2017). Big data storage technologies: A survey. *Frontiers of Information Technology & Electronic Engineering, 18*(8), 1040–1070. https://doi.org/10.1631/FITEE.1500441

**Purpose:** The academic backbone of the storage half: *why* big data forced a shift from relational → NoSQL, a **taxonomy of 26 NoSQL engines by data model**, and a decision framework via **Brewer's CAP theorem** (consistency vs availability). This is your "choose a store, and justify it" reference for A1.

---

#### 1. Why relational databases fail at big data
- Big data is **schema-less, interconnected, rapidly growing**; relational schemas are **rigid**, evolve slowly, and handle heterogeneous/unstructured data poorly.
- **NoSQL** answers with **flexible data models, horizontal scalability, schema-less storage, high availability, replication, and low cost** — and supports many concurrent users.
- *Storage is the **preliminary process** of big data analytics* — get it wrong and nothing downstream works (echoes Module 2's "bad ingestion = bad analytics").

#### 2. Taxonomy — 4 NoSQL data models ⭐

| Model | How it stores | Best for | Example engines |
|---|---|---|---|
| **Key-value** | Small objects: a **key** → its **value** (not blocks); schema-free | Huge volumes of small records, fast lookups: sessions, online shopping/games | Redis, DynamoDB, Riak, Voldemort, BerkeleyDB, Scalaris |
| **Column-oriented** | Columns stored **separately** (vertical partitioning), compressed | Aggregation/analytics, warehousing, "add a feature to all rows" | **HBase, BigTable, Hypertable, Cassandra** |
| **Document-oriented** | **Value = a document** (usually **JSON**/XML); flexible schema + indexes; complex/hierarchical queries | User profiles, web/content analytics, transactional apps | **MongoDB, CouchDB, Terrastore, RethinkDB** |
| **Graph** | Persistent **objects + relationships**, easy traversal | Recommendations, fraud, social networks, low-latency relationship queries | **Neo4j, AllegroGraph, InfiniteGraph, OrientDB, HyperGraphDB** |

- **Tensor-based models** (e.g. **SciDB**) extend graphs for high-order/multi-relational *analytics* (topic modelling, social-network analysis).
- **Licensing** axis: open-source / proprietary / commercial (most key-value & column engines are open source; **BigTable** = proprietary, **DynamoDB** = commercial).

#### 3. Brewer's CAP theorem — the decision framework ⭐

> A distributed store can guarantee at most **two of three**: **C**onsistency · **A**vailability · **P**artition-resilience. Brewer's **updated** reading: **partition-resilience is mandatory** (network splits are rare but unavoidable), so the real design choice is **C vs A**.

- **ACID** (relational) = **strong consistency**; **BASE** (NoSQL) = **B**asic **A**vailability, **S**oft state, **E**ventual consistency — better for faults/partial failures at low cost.
- **CP systems** = strong consistency, **synchronous writes**, may go **unavailable** during a partition while replicas re-sync.
- **AP systems** = always answer, accept **eventual consistency**.

| Type | Picks | Example engines |
|---|---|---|
| **CP** (consistency) | Correctness over uptime | Scalaris, Redis, MemcacheDB, BerkeleyDB · **HBase, Hypertable, BigTable** · MongoDB, Terrastore, RethinkDB · **all graph DBs** |
| **AP** (availability) | Uptime over freshness | **Cassandra, Voldemort, DynamoDB** · SimpleDB, CouchDB, OrientDB |

- 🔴 **Design rule:** *fraud/dosing decision must be correct?* → lean **CP**. *Must always accept writes from a sensor firehose?* → lean **AP**. This is the sentence that turns A1's storage choice into an *argument*.

#### 4. Ecosystem & open challenges
- **Hadoop + MapReduce** = de-facto **batch** standard; **S4** for real-time streaming; Apache stack: **Mahout, Lucene, Hive, Pig, Spark**. **HDFS** is **append-only** (no in-place update).
- **Future challenges:** frequent **schema change**; choosing **horizontal vs vertical partitioning** when access patterns shift; **replication** cost (space vs locality); **user expertise** (easy-to-use yet high-performance).

#### Key Takeaways for BDA601
1. The **4-model taxonomy + CAP** is the rigorous version of R1's engine list — use the table to *pick and justify* a store in A1.
2. **CP vs AP** is the highest-value exam/assessment idea in the module: tie it to your domain's **consistency-vs-availability** need.
3. **HDFS append-only / separation of storage & compute** links back to Module 1 (Hadoop) and forward to Module 4 (Spark).

---

## 🔴 Assessment hook (carry into A1)

**A1 = Design a Data Pipeline · report 1500 words · 30% · due 28/06/2026 · SLOs a/b/e.** Module 3 supplies the **middle and end** of your pipeline:

1. **Integrate** — name a **schema alignment → record linkage → data fusion** step for your sources (e.g. reconcile sensor reads with a reference/threshold table).
2. **Store** — pick a **lake store** (S3 or ADLS Gen2) and a **NoSQL model** (key-value / column / document / graph), and **justify it via CAP** (does your decision need CP correctness or AP availability?).
3. **Design principle to quote:** *performance → less compute → lower cost*, and *governance/security from the logical architecture, not bolted on later*.
