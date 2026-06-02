# BDA601 · Module 1 — Class Notes (Live Lecture)

> Dr. Chen Zhan · Week 1 lecture. Lean recap of the live session + Q&A.
> Companions: [one-pager](module01_one-pager.md) · [reading notes](module01_notes.md).

## TL;DR
- **Hadoop separates storage from compute.** HDFS *stores*; MapReduce/YARN *process*. Mixing these up is the classic exam trap.
- The lecturer's real-world case — a **government water-quality sensor pipeline (200+ parameters → HQ decides treat-or-distribute)** — is a live Module 1 case study: it touches Volume, Variety, Velocity, Veracity and Value in one breath.
- **Big Data Analytics working definition:** collect → manage → process → analyse → visualise → communicate large/complex data to produce insight and **support a decision**.
- One line to keep: **Data → evidence → decision → evaluate. No decision = no value.**

---

## Hadoop architecture — storage vs processing
**Core principle: separation of storage and compute** (same idea returns in modern stacks like Spark + S3/HDFS).

| Layer | Component | Responsibility |
|---|---|---|
| **Storage** | **HDFS** | Store data in distributed blocks — *storage only, no processing* |
| **Processing** | **MapReduce** | Parallel computation over that data |
| **Resource mgmt** | **YARN** | Schedule jobs, allocate cluster resources |

- Files are split into **blocks** (default **128 MB** in Hadoop 2+), spread across **DataNodes**, usually **replicated 3×** for fault tolerance.
- **NameNode** = master, holds **metadata** (where blocks live). **DataNodes** = workers, store the actual blocks. *(Common follow-up question.)*

### 🪤 The exam trap (knowledge-check Q)
> "HDFS performs parallel processing of data" → **INCORRECT.** Processing is MapReduce/YARN's job; HDFS only stores.

The misdirection: it borrows a *true* property of Hadoop (parallel processing happens) and attaches it to the *wrong* component. Read "parallel processing" → don't just nod along; ask *which layer*.

> 🔭 Forward link: when we hit **MapReduce vs Spark** (Module 4), the headline is *why Spark largely replaced MapReduce* (in-memory vs disk) — a constant data-engineering interview question.

---

## 💧 Case study — Dr. Chen Zhan's government water project *(gold for A1)*
Not LiDAR/laser depth-mapping — it's **water-quality monitoring**: a sensor array measuring **200+ characteristics per sample**, streamed to HQ, where someone decides *fine-tune the treatment or pass it forward (distribute)*.

- **"Layer measurement"** = sampling the water column / successive treatment stages.
- Typical parameters: pH, turbidity, dissolved oxygen, conductivity, temperature, chlorine residual, heavy metals, nitrates, microbial indicators.

**Maps straight onto Module 1:**
| Concept | In this case |
|---|---|
| **Volume + Variety** | 200+ params × continuous sampling × multiple sites |
| **Velocity** | HQ acts in (near) real time on the stream |
| **Veracity** | a bad reading → unsafe water → *life-or-death*, not academic. How do you catch a **drifting sensor** before it triggers a wrong call? |
| **Value (anchor)** | the whole point is the **distribution go/no-go** — Marr's "why before tools" in the flesh |
| **EMC lifecycle** | raw reads (*Data Prep*) → thresholds/model (*Model Building*) → go/no-go signal (*Communicate*) → ongoing monitoring + retrain (*Operationalize*) |

**Questions worth asking him:** Out of 200+, how many actually *drove* the decision vs were just monitored? Fixed threshold or a learned model? How did you detect a faulty/drifting sensor? What was the latency budget? And the opener: *"walk me through one sample's journey, from sensor to a human at HQ acting on it."*

---

## What is Big Data Analytics? (3 lenses — it's all three at once)
| Lens | One-liner |
|---|---|
| **As a pipeline** | raw data → cleaned, structured, modelled, interpretable evidence |
| **As org capability** | tools matter, but value = governance + skills + domain knowledge + adoption |
| **As decision science** | a model is useful only when it informs a decision you can evaluate |

- 🔵 The goal is **not** "having data" — it's **better decisions** (Value is the anchor; "why before tools").
- Projects fail not from bad tech, but from **no governance/adoption**.

---

## 💡 My in-class insight *(mine — not lectured)*
The water-sensor story is doing the *same thing* as the "3 lenses" slide: **200 parameters (pipeline) → HQ judgement (decision science) → was the water safe? (evaluate)**. Three lenses, one example — that's the whole subject's thesis. This is a portfolio-grade pipeline I can build **Assessment 1** around.

## 🔴 Assessment hook
**A1 = Design a Data Pipeline · report 1500 words · 30% · due 28/06/2026 · SLOs a/b/e.**
Strong candidate domain: a **real-time water-quality sensor pipeline** — ingest 200+ params → validate veracity (drift/outliers) → score against safety thresholds → alert HQ. Designing something a human actually built makes the report far sharper.
