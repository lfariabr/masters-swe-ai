# BDA601 · Module 2 — Class Notes (Live Lecture)

> Dr. Chen Zhan · Week 2 · 09 Jun 2026 · live session (recorded, on Teams). Lean recap of the live session.
> Companions: [one-pager](module02_one-pager.md) · [reading notes](module02_notes.md).

## TL;DR
- **Module 2 = the FRONT of the pipeline:** `Sources → Ingestion → Store → Analyse`. The thesis: **bad ingestion = bad analytics** (garbage in, garbage out).
- **Data value pyramid:** Collection (I) + Pipelines (II) are the base — if the base cracks, Analytics (IV) and AI/ML (V) on top collapse. That's *why* ingestion matters.
- **3 ingestion patterns by latency:** Batch (hours/days) · Micro-batch (seconds–minutes) · Streaming (sub-second). ⚠️ **Fraud detection = STREAMING**, not micro-batch.
- **5 lake zones:** Source → Transient (validate) → Raw (immutable) → Curated → Serving = **Bronze/Silver/Gold** (medallion).
- **Storage golden rule:** keep **raw for auditability** · build **curated for reuse** · **document lineage** so users know where data came from.
- **Veracity lives in the Transient zone** — validation catches bad data *before* it pollutes the lake.

---

## 🧭 Framing — why this module
Three principles the lecturer opened with:
1. **Data is the raw material** — nothing downstream exists without it.
2. **Pipelines create flow** — they move data from where it's born to where it's used.
3. **Bad ingestion creates bad analytics** — quality is decided *at intake*, not after.

**The spine:** `Sources → Ingestion → Store → Analyse`.

### The data value pyramid
| Level | Layer | What lives here |
|---|---|---|
| **V** | AI / ML | models, intelligent products |
| **IV** | Analytics | reports, dashboards, decisions |
| **III** | Data products | reliable datasets / features |
| **II** | Data pipelines | flow, integration, retrieval |
| **I** | Data collection | sources, ingestion, storage |

🔑 **Read it bottom-up:** Collection (I) and Pipelines (II) are the **foundation**. If the base fails, everything above — analytics, AI — inherits the rot. This is "bad ingestion = bad analytics" drawn vertically.

### Module roadmap (what week 2 covers)
1. Data sources → 2. Data structures → 3. Ingestion challenges → 4. Pipeline principles → 5. Storage choices.

---

## ⏱️ Ingestion patterns — by latency *(corrected)*
> 🪤 **The trap to unlearn:** the latency tiers and their *examples* get swapped. **Fraud detection is streaming, not micro-batch**, and streaming is *seconds*, not "minutes/hours".

| Pattern | Latency | How it works | Typical use |
|---|---|---|---|
| **Batch** | hours → days | data collected + loaded on a schedule (nightly, hourly) | data warehousing, periodic reporting, payroll, billing |
| **Micro-batch** | seconds → minutes | small batches loaded frequently | near-real-time dashboards, IoT rollups, **Spark Structured Streaming** |
| **Streaming** | sub-second → seconds | events captured + processed continuously | **fraud detection**, live monitoring, clickstream, sensor alerts |

- 🔴 **Why fraud = streaming:** you must block the swipe **now** — you can't wait for the next batch window.
- **Micro-batch is the middle ground:** not truly real-time, but fresher than batch (Spark Structured Streaming is the canonical engine).

---

## 🔌 Common ingestion techniques
| Technique | Notes |
|---|---|
| **File transfer** | CSV, Excel, Parquet, JSON, XML, compressed archives. Often **batch** ingestion. |
| **Database extraction** | SQL queries, **change data capture (CDC)**, replication, or scheduled exports from operational systems. |
| **APIs** | programmatic access to external/internal services; needs **authentication, rate-limit handling, error handling**. |
| **Message queues / event streams** | high-velocity data from apps, IoT devices, user interactions. e.g. **Kafka, RabbitMQ, AWS Kinesis**. |
| **Web data collection** | only when permitted — mind **terms of service, privacy, robots.txt, data ethics**. |

---

## 🏞️ Storage — choices + the design rule
**Four destinations after ingestion:**

| | Store | When to use it |
|---|---|---|
| **DB** | Operational database | live transactions (OLTP) |
| **DW** | Data warehouse | structured, modelled, *known* questions (schema-on-write) |
| **DL** | Data lake | raw, multi-structured, *unknown* questions (schema-on-read) |
| **LH** | Lakehouse | lake + warehouse in one (raw storage + ACID/BI on top) |

> 🔴 **Golden rule of storage (slide, bolded → examinable):**
> **Keep raw for auditability · create curated for reuse · document lineage so users know where data came from.**
> Without this, "storage" is just vocabulary; with it, it's a **design principle** — which is exactly what A1 wants.

### The 5 lake zones (pipeline skeleton for A1)
**Source → Transient** (validate) **→ Raw** (immutable) **→ Curated → Serving**
**Medallion map:** Raw = **Bronze** · Curated = **Silver** · Serving = **Gold**.

- 🔑 **Transient / landing zone = where Veracity lives** — validation catches bad/duplicate/corrupt data **before** it reaches the lake. (Ties Module 1's *Veracity V* → architecture.)
- **Raw = immutable** — preserve the original capture for audit/replay; never edit in place.
- **Anchor phrase:** *separate raw capture from cleaned products.*
- 🔗 **Reconciles with the readings:** the class's **Curated ≈** Pasupuleti's **Management tier** (Silver); **Serving ≈ Consumption tier** (Gold). Same idea, different labels — see [module02_notes.md](module02_notes.md).

---

## 🔴 Assessment hook
**A1 = Design a Data Pipeline · report 1500 words · 30% · due 28/06/2026 · SLOs a/b/e.**
This whole class is **A1 scaffolding**: the **5 lake zones** are a ready-made pipeline skeleton, the **storage golden rule** is your design principle, and **"Veracity lives in the Transient zone"** is the one line that turns a diagram into an argument. Map your chosen domain (e.g. the **SA Water** sensor pipeline from Module 1) onto **Source → Transient → Raw → Curated → Serving**.
