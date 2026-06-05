# BDA601 · Module 1 — Class Notes (Live Lecture)

> Dr. Chen Zhan · Week 1 · 02 Jun 2026 · 3h08m (recorded, on Teams). Lean recap of the live session + Q&A.
> Companions: [one-pager](module01_one-pager.md) · [reading notes](module01_notes.md).

## TL;DR
- **Hadoop separates storage from compute.** HDFS *stores*; MapReduce/YARN *process*. The quiz trap: "HDFS performs parallel processing" → **false**.
- The lecturer's real case — **SA Water** using a **laser sensor** (wavelength absorption) to monitor water quality, >200 readings/min, streamed to HQ to decide *when to dose more treatment* — is a live Module 1 pipeline touching every V.
- **6 V's:** Volume, Velocity, Variety, Veracity, **Value** (the anchor), + **Valence** (connectivity). Veracity bites *structured* data too, not just images/audio.
- **Lifecycle = pipeline = a loop**, not a one-way street: Discovery → Data Prep → Model Planning → Model Building → Communicate → Operationalize. You can go back, repeat, skip, or add steps.
- One line to keep: **Data → evidence → decision → evaluate. No decision = no value.**

---

## 📋 Course admin & rules (heard in lecture)
- **Online via MS Teams**, Tuesdays **8–11am Adelaide time** (~8:30am Sydney). Every session **recorded**; slides/datasets/code in the Teams *Shared* tab.
- **Formal comms** (extensions, absence) → email `@torrens.edu.au` *only* (the `mylearn.…` address doesn't reach him). Informal → Teams chat.
- **Late policy:** ≤7 days, no evidence needed, just ask · >7 days needs supporting docs (e.g. medical cert) · >14 days escalates to a university team · no valid reason → grade penalty.
- **Attendance** not compulsory but strongly encouraged (low engagement gets flagged via the LMS).
- **Grade distribution is regulated** → effectively a ranking system; only the **top ~1–2 students get HD**. To reach HD you must go **beyond what's taught** — add novelty/self-study to the assessment.
- **3 assessments, incremental:** A1 (28 Jun) feeds A2 (26 Jul) feeds A3 (19 Aug). A3 carries the most weight. Skills needed will be taught in class.
- **Course shape:** weeks 1–4 = conceptual (big data, pipeline, lifecycle, Spark); weeks 5–12 = technical (cleaning, classification, evaluation, prediction, clustering, association rules, graph analytics, privacy/security). *Breadth over depth* — it's an intro.

## 🎬 Opening video (Simplilearn) — source of the Hadoop quiz
Stats to anchor scale: ~40 EB/month per smartphone user × ~5B users; per-minute internet (3.8M Google searches, 4.5M YouTube views, 188M emails…). Healthcare framing of the 5 V's. Big-data value examples: **Halo 3 / Call of Duty** churn analysis; **Hurricane Sandy (2012)** — predicted landfall **5 days ahead**.
> The video ends with the exam-style MCQ on HDFS → leads straight into the architecture below.

---

## Hadoop architecture — storage vs processing
**Core principle: separation of storage and compute** (returns in modern stacks like Spark + S3/HDFS).

| Layer | Component | Responsibility |
|---|---|---|
| **Storage** | **HDFS** | Store data in distributed blocks — *storage only, no processing* |
| **Processing** | **MapReduce** | Split a big task → smaller tasks run in **parallel** across nodes → assemble results |
| **Resource mgmt** | **YARN** | Schedule jobs, allocate cluster resources |

- Files split into **blocks** (default **128 MB**, Hadoop 2+), spread across **DataNodes**, **replicated 3×** for fault tolerance (one machine fails → data safe elsewhere).
- **NameNode** = master, holds **metadata** (where blocks live). **DataNodes** = workers, store actual blocks. *(Common follow-up question.)*

### 🪤 The exam trap (knowledge-check Q)
> "HDFS performs parallel processing of data" → **INCORRECT.** Processing is MapReduce/YARN's job; HDFS only stores. (A, B, D are true.)

It borrows a *true* property of Hadoop (parallel processing happens) and pins it on the *wrong* layer. Read "parallel processing" → ask *which layer*.

> 🔭 Forward link (Module 4): **Spark vs MapReduce** — in-memory vs disk is why Spark largely replaced MapReduce. Constant data-eng interview question.

---

## The 6 V's — with the nuances he stressed
| V | Meaning | Lecture nuance |
|---|---|---|
| **Volume** | size of data | too large for traditional storage/processing/manual analysis (decades of logs, posts, sensor reads) |
| **Velocity** | speed of generation + need for (near) real-time response | fraud detection, recommendations, sensor alerts — payment can't take minutes |
| **Variety** | structured / semi-structured / unstructured | structured = rows×cols · semi = JSON/XML/web · unstructured = text/audio/video → needs deep learning / LLMs |
| **Veracity** | trust / quality: noisy, biased, incomplete, duplicated | 🔑 **structured data is noisy too** — gene expression reads 100 but true signal ≈50, rest is device/temperature noise. "Don't assume structured = clean." |
| **Value** | usefulness → supports a decision → financial benefit | **the anchor.** "A technically impressive analysis with no action pathway has limited business value." |
| **Valence** | connectivity among data items (newest V) | connections in **2 directions** (below) |

**Valence in two directions** (structured table = items × features):
- **item ↔ item** — e.g. students in the same assignment group are connected.
- **feature ↔ feature** — e.g. marks and course names are correlated.
- 🔴 **Warning:** more connectivity/features ⇒ more modelling complexity, **cost, and overfitting risk** (model memorises training data, loses generalisation). Don't collect more data "just because" — only with a clear analytical purpose.

---

## 💧 Case study — Dr. Chen's SA Water project *(gold for A1)*
**Correction to earlier notes:** it *is* a **laser sensor** — but **absorption spectroscopy, not LiDAR depth-mapping**. ("layer measurement" was actually **laser measurement**.)

- Laser scans the water body with **different wavelengths**; contaminants/ingredients **absorb specific wavelengths**, so the **reflected signal** (which wavelengths drop) reveals water quality.
- **>200 wavelength data points per minute, per sensor**; **multiple sensors** across the water body.
- Sensors sit **in the water**; a **ground station** relays data to **HQ** (water bodies are remote).
- **The decision the data drove** (Luis asked this live): the system tells HQ **when more treatment solution must be added** to keep water in good quality.

**Maps onto Module 1:**
| Concept | In this case |
|---|---|
| **Volume + Variety** | 200+ wavelength reads × every minute × many sensors |
| **Velocity** | HQ acts in near-real-time on the stream |
| **Veracity** | a bad/false reading → wrong dosing → unsafe water. How do you catch a **drifting sensor**? |
| **Value (anchor)** | the **dose-or-not** decision — Marr's "why before tools" in the flesh |
| **EMC lifecycle** | raw wavelength reads (*Data Prep*) → quality model/thresholds (*Model Building*) → dosing signal to HQ (*Communicate*) → ongoing monitoring + retrain on drift (*Operationalize*) |

---

## Data Analytics Lifecycle (6 phases) — the spine
A **structured loop** from *data generated* → *insight that drives a decision → financial/economic reward*. He walked it with a **retail "increase sales"** example:

1. **Discovery** — frame the business problem + **success criteria** (e.g. +10–20% sales). Decide what data is needed.
2. **Data Preparation** — collect (incl. external data: census, economic trends), clean, transform, understand.
3. **Model Planning** — pick the task (classification / clustering / prediction…) then the **algorithm** (know each one's pros & cons). *e.g. "is this customer a target for the campaign?" → classification.*
4. **Model Building** — train / test / refine; **tune parameters** (no one-size setting — case by case; always back changes with evidence).
5. **Communicate Results** — present **evidence** to stakeholders (e.g. "price too high vs competitors → that's why sales are low"). Stakeholders decide.
6. **Operationalize** — deploy, **monitor, maintain, retrain** on data drift. The whole point of "pipeline": it must be **reproducible** for the next product/question.

🔁 **Not one-way:** hit a wall and you **go back** (need more data → step 2; wrong algorithm → step 3), **repeat** steps, **skip** steps (consultant gets clean data → jump to planning), or **add** steps (need a Power BI dashboard → add a viz component).

## ⚠️ Why Big Data projects are challenging (slide)
Storage/infra cost · integration & cleaning (combine sources/formats) · trust & governance (access control) · **modelling & interpretation** (overfitting, bias, **explainability** — model it *well*, make it make sense to the domain) · operationalization (scalability — un-scalable models crash as data grows) · **value realisation** (project fails if stakeholders can't act on or measure the impact).

---

## What is Big Data Analytics? (3 lenses — all three at once)
| Lens | One-liner |
|---|---|
| **As a pipeline** | raw data → cleaned, structured, modelled, interpretable evidence |
| **As org capability** | tools/services matter, but value = governance + skills + **domain knowledge** + adoption |
| **As decision science** | a model is useful only when it informs a decision you can **evaluate** |

- 🔵 The goal is **not** "having data" — it's **better decisions** (Value is the anchor; "why before tools").
- The gap to bridge: **technical big-data skill × domain expertise.**

## 🎯 Q&A — "What's the ideal accuracy?" (Sachin)
**No single threshold — case by case.** Cancer example: prevalence ~1.1%, so a model that labels *everyone healthy* scores **99% accuracy** and is **useless**. Don't fixate on "80% = good." → motivates **class imbalance** and looking past accuracy (Module 7, Model Evaluation; relevant to A2/A3).

## 🐍 Practical — Jupyter / Python setup (Activity 1)
- Install **Python** (manually, pick a **stable** version) → **Anaconda** (GUI package/env manager) → **Jupyter Lab/Notebook**.
- Dr. Chen recommends **Python 3.14** (latest *stable*; 3.15/3.16 are pre-release/beta — avoid unless you need a new feature). *(Matches my Homebrew py3.14 env.)*
- **Conda** = isolated env per project to avoid version conflicts: `conda create -n bda python=3.14` → `conda activate bda` → install packages → launch Jupyter.
- **Jupyter Notebook** = live coding: **code chunks + markdown text chunks + outputs/charts** in one `.ipynb` → reproducibility.
- **Google Colab** = Jupyter on the cloud — acceptable.
- 🔴 **Delivery rule for assessments:** hand in a **`.ipynb`** (code + result tables + charts), **not** a plain `.py`.

## 👤 Dr. Chen — background (networking ammo)
Data science / ML / AI (ex-cybersecurity). PhD: **pharmacy data → adverse drug events** (TGA monitoring). Postdoc (COVID): **educational data mining / learning analytics**. Then **computational biology** (single-cell RNA-seq, cancer, high-dimensional, noisy). Also **environmental science (SA Water)** and **government economic data** (SA import/export, comparative advantage, red wine). Teaches BDA601 + Intro to Data Science. *Theme: data skills transfer across domains — blend IT career with other industries.*

---

## 💡 My in-class insight *(mine — not lectured)*
I asked Dr. Chen the **Value question** live — *"what real decision did the data drive?"* — and the answer (when to dose treatment) is the cleanest possible illustration of the course thesis: **200 readings (pipeline) → HQ judgement (decision science) → was the water safe? (evaluate).** Three lenses, one example. This is a portfolio-grade pipeline I can build **Assessment 1** around.

## 🔴 Assessment hook
**A1 = Design a Data Pipeline · report 1500 words · 30% · due 28/06/2026 · SLOs a/b/e.**
Strong candidate domain: a **real-time water-quality sensor pipeline** — ingest 200+ wavelength reads → validate veracity (sensor drift/outliers) → score against safety thresholds → signal HQ to dose. Designing something a human actually built makes the report far sharper. Remember: deliverables as **`.ipynb`** where code is involved.
