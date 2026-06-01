# BDA601 · Module 1 — One-Pager

> **Introduction to Big Data & Analytics — the V's, the Lifecycle, the Strategy**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape, 4 zones).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Big data isn't about MORE data — it's about turning digital trails into VALUE for a business decision.**
> (Marr's whole argument, and the spine of Module 1.)

## 🖤 Zone 1 — What & Why now?
- **Big Data = relative.** Not just "too big for one computer" — complex relative to *your* people, skills, tools. Big for a charity ≠ big for Google.
- 🔵 **Why it exploded:** cheap **storage** + cheap **compute** + **IoT / digital trails** (humans *and* machines, 24/7).
- 🔵 **Two sources:** *human-generated* (browsing, posts, photos, cards) · *machine-generated* (sensors, CCTV, wearables, satellites).
- 🔴 **Structured vs Unstructured** — Structured = rows/cols, easy to query (transactions, surveys). Unstructured = video, image, text, speech — *richer but needs advanced processing.*
- 🔴 Marr's shop example: counting people = structured; **video of behaviour** = unstructured gold.

## 🖤 Zone 2 — The 6 V's ⭐ SLO a) — THE GRADED CORE
| V | One-liner |
|---|---|
| **Volume** | how *much* (storage/processing pain) |
| **Velocity** | how *fast* (real-time pressure) |
| **Variety** | how many *types* (text, video, sensors) |
| **Veracity** | how *trustworthy* (errors, gaps, duplicates) |
| **Valence** | how *connected* (linked data = richer + riskier) |
| **Value** | does it *help the business?* |

- 🔴 First **3 = Gartner, 2011** (Volume, Velocity, Variety).
- 🔴 **Value is the ANCHOR** — no value = no point.
- 🔵 **Valence** = connected items ÷ all possible connections; grows over time; high valence = harder to model + privacy risk.
- 🔵 Mnemonic: *"Very Vast, Varied & Verified, Vibrantly Valuable."*

## 🖤 Zone 3 — Data Analytics Lifecycle (EMC, 6 phases — it's a CIRCLE)
```
   1 Discovery ──► 2 Data Prep ──► 3 Model Planning
        ▲                                  │
        │                                  ▼
   6 Operationalize ◄─ 5 Communicate ◄─ 4 Model Building
```
1. **Discovery** — what's the problem? (hypotheses, data sources)
2. **Data Prep** — *analytic sandbox*, clean & shape (ELT/ETLT)
3. **Model Planning** — which method fits?
4. **Model Building** — train/test, does it work?
5. **Communicate** — so-what, value, caveats
6. **Operationalize** — pilot → monitor → retrain

- 🔴 **Discovery + Data Prep decide project quality** (most projects fail by rushing them).
- 🔴 **Data prep + communication eat more time than modelling.**
- 🔴 **Evaluation ties back to Phase 1 success criteria** — not just accuracy.

## 🖤 Zone 4 — Strategy, BI vs BDA & Tools
- **Marr's 6 business uses:** Decisions · Customers/markets · Better products · Better services · Operations · **Monetise data**.
- 🔴 **"Why before tools."** Projects fail when teams chase tech before the business reason.

| Traditional BI | Big Data Analytics |
|---|---|
| structured only | structured + semi/unstructured |
| *what happened* | *why + what's next* |
| retrospective | predictive / real-time |

- 🔵 **Tool ecosystem (just recognise):** Hadoop · **Spark** (← Module 4!) · Kafka · NoSQL · Hive · MapReduce · YARN.

## 🔴 Assessment Hook (bottom red strip)
> **A1 = Design a Data Pipeline** · report 1500 words · 30% · due **28/06/2026** · SLOs **a) b) e)**.
> Module 1 = your SLO a) foundation. Familiarise with the brief **this week.**

## 🔴 If you only memorise 5 things
1. Big data = **value from trails**, not size.
2. **6 V's** — Value is the anchor (3 from Gartner 2011).
3. **6-phase lifecycle is a CIRCLE** — Discovery & Prep matter most.
4. **Why before tools** (Marr) — strategy first.
5. **Spark** comes in Module 4; **Jupyter** is your IDE (Activity 1 to-do).

---

### Margin prompts (answer in blue while you write)
1. Pick a dataset from your own work — which of the 6 V's bites hardest?
2. For Assessment 1, which lifecycle phase will be hardest to design for, and why?

### This-week to-dos (still 🕐 in your notes)
- [ ] Activity 1 — install & explore **Jupyter Notebook** (Anaconda/conda)
- [ ] Activity 2 — Module 1 **Interactive Knowledge Check** (retake freely)
