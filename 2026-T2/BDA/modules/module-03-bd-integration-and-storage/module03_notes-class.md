# BDA601 · Module 3 — Class Notes (Live Lecture)

> Dr. Chen Zhan · Week 3 · 16 Jun 2026 · live session (recorded, on Teams, ~3h). Lean recap of the live session + Q&A.
> Companions: [one-pager](module03_one-pager.md) · [reading notes](module03_notes.md).

## TL;DR
- **Module 3 = the MIDDLE of the pipeline:** turn **raw, heterogeneous data into a reliable, reusable, safe data asset**. This is the lake's **management tier**.
- **The 3 lake tiers are LOGICAL, not physical:** `Intake (Mod 2) → Management (today) → Consumption (later)`. Each tier is *many* instances (compute nodes, S3 buckets, DBs), not one box.
- **Management tier = 4 components:** **Integration · Quality control · Enrichment · Storage.** (This is the Pasupuleti Ch.3 content.)
- **Integration ≠ copying files** — it's **resolving meaning, structure, identity and quality** so different sources serve the *same* business. Decide via **What / Why / How**.
- **4 integration patterns:** **ETL · ELT · Data Virtualization · Streaming.**
- **Logical (soft) fix > physical rewrite** of legacy data — rewriting risks data loss + cost; big firms minimise *risk*.
- **Operational principle:** catch integration/quality problems **early** (in management), not at modelling time.
- **A1 rehearsal** via the **City Fresh Market** case study + the teacher's explicit grading expectations (see hook).

---

## 🧭 Where Module 3 sits — the 3 logical tiers
The lake splits into three **tiers / focuses** (Monica's Q&A made this explicit):

| Tier | Focus (angle) | Module |
|---|---|---|
| **Intake** | collect + accept data from where it's sourced | Module 2 |
| **Management** | **integrate · clean · enrich · store** | **Module 3 (today)** |
| **Consumption** | use the data — ML/AI, stats, BI dashboards | later weeks |

- 🪤 **Trap to unlearn:** tiers are **logical umbrellas, not 3 machines.** One tier = multiple physical instances (e.g. management = a compute node for cleaning **+** an S3 bucket for storage **+** a DB). It's *steps/process*, not a storage location.
- The 3 tiers are **universal** — every project has them; only the *sub-steps inside* each tier vary by project.
- One-line position: **"Module 3 turns raw heterogeneous data into a reliable, reusable, safe data asset."**

---

## 🧩 Integration — what it actually means
> 📌 **"Integration is not just copying files into one place — it's resolving meaning, structure, identity and quality."**

Data arrives in **silos** (CRM, shop sales, web logs, IoT inventory sensors, partner APIs, support tickets). All of it serves the *same* business, so you must align it. The integration questions:
- Does this **customer ID** mean the same thing across systems?
- Are **timestamps** in the same time zone? (Adelaide is ½h behind Sydney/Melbourne — real issue for Woolworths/Coles scale.)
- Are duplicates / missing values / outliers handled consistently? **Which record is authoritative?**

### The What / Why / How decision framework ⭐ (new — use in A1)
| | Question | Purpose |
|---|---|---|
| **What** | What data do I have, and what apps consume it? | inventory the heterogeneous sources |
| **Why** | Why integrate? | break **silos**, improve completeness, give decision-makers *one reliable version of reality*; locate where errors come from |
| **How** | How do I mitigate the differences? | **schema · metadata · transformation rules · quality checks · entity matching · governance · scalable storage** |

---

## 🪤 The 6 integration challenges → mapped to the Vs ⭐
Big data expands traditional integration along the **Vs**. The lecture's six challenges (each maps to a V):

| # | Challenge | What breaks | V |
|---|---|---|---|
| 1 | **Schema heterogeneity** | same concept, different column names/types/formats (e.g. `YYYY-MM-DD` vs `DD-MM-YYYY`) | variety |
| 2 | **Entity resolution** | identifying records for the *same* real-world object across systems (UniSA + Adelaide Uni merge → student described differently) | variety |
| 3 | **Data quality** | missingness, duplicates, outliers, inconsistent units, invalid values | **veracity** |
| 4 | **Velocity** | batch files vs streaming APIs arrive at different speeds | velocity |
| 5 | **Governance** | access control, privacy, lineage, accountability must be preserved | value |
| 6 | **Scalability** | keep storage/compute/retrieval performant **and** affordable as volume grows | volume |

> 🪤 **Naming trap:** the lecture's 6th V is **variance** (consistency over time). Module 1's reading called the 6th V **valence** (data connectivity). Same "6V" label, **different sixth V** depending on source — know both. For **A1, only the 5 Vs are in scope** (6V is "a bit recent / out of scope").

---

## 🔄 The 4 integration patterns ⭐
> The lecturer: *"pay most attention to the first two — ETL vs ELT."*

| Pattern | What it does | When / cost |
|---|---|---|
| **ETL** (Extract-Transform-Load) | standardise **before** storing (rename/clean, then drop into storage) | when data must be standard before storage; **risk:** a new dev may not know the source was rewritten |
| **ELT** (Extract-Load-Transform) | dump **raw** into cheap storage, transform **later** via a mapping/rule layer | cloud lakes & lakehouses; **cost:** extra storage + compute, but **preserves raw** |
| **Data Virtualization** | a **logical/soft view** that queries across sources **without physically moving** data | fast access, no copy; **cost:** latency + governance (runs integration on every query) |
| **Streaming ingestion** | continuously process events as they arrive | IoT, clickstream, **fraud detection**, ops monitoring |

### 🔑 Logical (soft) fix > physical (hard) fix — the teacher's recommendation
- **Hard fix:** physically rewrite/move all legacy data into one schema. Risk: **data loss** + **expensive** + accumulates across hundreds of columns/tables.
- **Soft fix:** keep raw as-is; add a **metadata / schema / transformation-rule layer** to *route and reconcile* logically.
- **Big companies prefer the soft fix — they minimise RISK over cost.**
- 🏫 **Example (school):** legacy data 2010–2020 lives on AWS, post-2020 on Azure. Don't migrate it all — write a **metadata rule**: a dashboard query for pre-2020 routes to AWS, current trimester routes to Azure.

---

## 🧪 The 4 management-tier components ⭐ (= Resource 3 content)
This is the detailed breakdown the lecture gave for the management tier — **the Pasupuleti Ch.3 material** the ebook gated:

**1. Integration** — join + reconcile heterogeneous sources (above).

**2. Quality control** — *fit-for-purpose, measured against the business question.* Concrete checks:
| Check | Catches |
|---|---|
| **Type check** | column is the expected type (date column = dates, grade = numeric, gender = categorical) |
| **Range check** | values within bounds (age ≥ 0 and integer; price ≥ 0; grade 0–100) |
| **Referential check** | referenced entity exists (an order's customer is still in the customer table) |
| **Duplicate detection + merge** | identical records (e.g. double-sent sensor packet, same timestamp) |
| **Missing-value handling** | nulls that break aggregations |
| **Quality logs + exception reports** | document raw-data issues so the next dev/analyst knows what to expect; aids debugging |

**3. Enrichment** — *add context/analytical value on top of raw data* (the component beginners under-rate). 4 types:
| Type | Example |
|---|---|
| **Internal** | customer segments, product hierarchies, department mappings |
| **External** | geography, demography, economic/public datasets |
| **Derived features** | lifetime value, churn risk, rolling averages |
| **Labels / metadata** | training labels, source lineage, quality scores, business definitions |

- 🎓 **Day-job example (learning analytics):** an LMS only logs raw actions (`student opened page at 9pm`, `paused video`, `rewound`). Engineer a derived feature **"video engagement = 1–5"** (1 = watched straight through, 3 = paused + rewound once...). That new column feeds an at-risk-student predictor or an engagement dashboard. **That is enrichment.**
- 🔴 **Caution:** enrichment can **introduce bias, privacy risk, misleading correlation if ungoverned.** Your segmentation logic may bake in an assumption (e.g. "young males who game don't buy shampoo"). Still do it — but flag the risk.

**4. Storage** — persist in a scalable, secure, retrieval-ready form (next section).

> 🔴 **Operational principle (examinable):** *"Don't wait until modelling to discover integration/quality problems. Capture rules, metadata, lineage during management."* Planning early in the management tier saves trouble in consumption.

---

## 🗄️ Storage — requirements + technology comparison
### Choose storage against 3 lenses
| Lens | Considerations |
|---|---|
| **Technical** | scalable; compatible with structured/semi/unstructured; high-throughput read/write; batch **and** stream support |
| **Governance** | identity + access control; encryption + key management; audit logs; policy-based lifecycle |
| **Business** | **cost**; reliability/availability (esp. multi-country); compliance (e.g. AU under-16 social-media ban → age checks) |

### Storage technology comparison (broader than just S3/ADLS)
| Tech | Profile |
|---|---|
| **HDFS** | on-prem distributed file system; high-throughput **batch**; you maintain the hardware/redundancy |
| **Object storage (S3 / ADLS Gen2)** | cloud lake foundation; elastic, cheap, durable; **needs good metadata + governance** |
| **NoSQL DB** | semi-structured, flexible schema, scale-out (e.g. MongoDB) |
| **SQL DB** | structured, close to traditional RDBMS; good if you have lots of legacy relational data |
| **Data warehouse** | structured BI/reporting, fast SQL; **less flexible** for raw/unstructured |
| **Lakehouse** | table format over the lake (raw storage + ACID/BI on top) |

- **S3 vs ADLS Gen2:** for a *user*, near-equivalent. Pick by (1) **accessibility** — stay on the platform your other services already use (don't split AWS storage onto Azure for no reason), and (2) **cost** (region/demand-dependent). ADLS = "cloud disk" feel (directory/file semantics via Hierarchical Namespace).

---

## 🏛️ Governance, metadata, lineage & ILM
> *"Without governance, a data lake becomes a data swamp."*

- **Metadata catalog** — what data exists, what it means, who owns it, last modified.
- **Lineage** — where data came from and how it changed (raw → corrected → annotated).
- **Access control** — who can read / write / transform.
- **Privacy & security** — protect sensitive data; regulatory compliance.
- **Retention & lifecycle (ILM)** — how long to keep, when to archive vs delete. 🧾 **Example:** the ATO requires 7 years of tax records → archive (don't delete) to cheaper storage.

---

## 🛒 Case study — "City Fresh Market" (the A1 rehearsal)
Brisbane online grocer (fresh/organic), ~550k visitors/month, 3 checkout paths (member / new member / one-time guest). **Accounts fragmented across teams** (customer relations vs health-nutrition outreach; procurement; UX ops). One-size-fits-all content → falling engagement/conversion. They want personalisation (product suggestions, personalised discounts, buying-pattern insight) and need a **data pipeline** to harmonise touchpoints into one repository.

**Class consensus (correct):** *the core problem is **integration**, not storage* — teams already store fine; the data is **fragmented** and must be harmonised before personalisation. Variety → lean **lakehouse over warehouse** (clickstream/engagement logs don't fit a warehouse cleanly).

---

## 🔴 Assessment hook — what Dr. Chen expects in A1
**A1 = Design a Data Pipeline · 1500 words · 30% · due 28/06/2026 · SLOs a/b/e.** His explicit expectations:

1. **Analyse the data FIRST** — list sources (internal *and* external), structure, data type, **example columns + example rows** per table (e.g. farm reports, inventory, client data internally; market-trends data externally).
2. **Align to the 5 Vs** — estimate volume, variety, velocity, veracity, value. ⚠️ **6V is out of scope for A1.**
3. **Design the pipeline twice:** **logical** (which components: ingestion → transform[clean+enrich] → storage → analytics → viz) **then map to physical** (which AWS/Azure/on-prem tool, *and why*).
4. **Recommend ONE platform** (greatest compatibility). Multi-platform only with a *strong* justification (e.g. existing legacy spread).
5. **Diagrams / workflow / flowcharts / tables = bonus marks** — *"the workflow speaks more than the text."* Don't submit pure prose.

> 🧠 Map your domain (e.g. **SA Water** sensors, or this **City Fresh Market** clone) onto: sources → ingestion → raw zone (immutable) → **management (integrate · quality · enrich)** → curated storage → consumption.

---

## 💡 Day-job anchors (from the live Q&A)
- 🏫 **School/student data (my question):** when an existing warehouse can't hold unstructured per-teacher student notes, **first add a logical metadata/schema-annotation layer** to point queries at where data lives; **migrate fully to a cloud data lake only as complexity keeps growing.** (Confirms the migration-timing answer — augment before you migrate.)
- 🎓 **Learning analytics enrichment** — derive a "video engagement 1–5" feature from raw LMS clickstream (see Enrichment above).
- 💧 **SA Water duplicates** — a remote sensor re-transmits after a sync failure → two identical-timestamp records → a **duplicate-detection** quality check catches it.
