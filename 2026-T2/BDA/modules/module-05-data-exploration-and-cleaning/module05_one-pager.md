# BDA601 · Module 5 - One-Pager

> **Data Exploration & Cleaning - attribute types · stats & visualisation · cleaning · reduction · PySpark prep**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Before you model anything, you must KNOW your data, CLEAN it, then SHRINK it.** Real data is incomplete, noisy and inconsistent - prep is **~80%** of the job and bad data costs **~$13.5M/yr** (Gartner). Garbage in, garbage out.
> (Han, Pei & Kamber Ch.2-3 · Lee & Drabas PySpark Ch.4 · ProjectPro)

## 🖤 Zone 1 - KNOW it: attribute types (the vocabulary)
- 🖤 **Data object** = a row / *tuple*; **attribute** = a column (a.k.a. dimension / feature / variable).
- 🔴 **The type decides which statistic is legal** - never average a nominal code.

| Type | Order? | Maths? | Valid centre | Example |
|---|---|---|---|---|
| **Nominal** | no | no | mode | job, marital |
| **Binary** | no | no | mode | housing yes/no |
| **Ordinal** | yes | no | mode, median | education S/M/L |
| **Numeric** | yes | yes | mean, median, mode | age, balance |

- 🔵 **Binary:** symmetric (gender) vs **asymmetric** (rare = 1, e.g. HIV+). **Numeric:** interval (no true zero, no ratios - °C, years) vs **ratio** (true zero, ratios OK - balance, age, counts).

## 🖤 Zone 2 - DESCRIBE it: central tendency + spread ⭐ SLO c) - THE GRADED CORE
- 🔵 **Centre:** mean (⚠️ outlier-sensitive → trimmed mean), **median** (use for skew), mode, midrange. Skew: `mean - mode ≈ 3·(mean - median)`.
- 🖤 **Spread:** range · quartiles (Q1/Q2/Q3) · **`IQR = Q3 - Q1`** · variance σ² / std σ · five-number summary → **boxplot**.
- 🔴 **Outlier rule of thumb: flag any value > `1.5·IQR` above Q3 or below Q1.** (Reused verbatim in PySpark `approxQuantile`.)
- 🔵 **See it:** histogram (numeric → bins; nominal → bar chart) · scatter (correlation: +/-/none) · q-q plot. Viz families: pixel · scatter-matrix / parallel coords · Chernoff faces · tree-maps.

## 🖤 Zone 3 - CLEAN it: missing, noisy, inconsistent (§3.2)
- 🖤 **Missing-value ladder** (worst → best): ignore tuple → fill manual → global constant ("Unknown") → **attr mean/median** → class mean/median → **most-probable value (regression/Bayes/tree) ✅**.
- 🔴 Methods 3-6 **bias** the data. A **missing value ≠ an error** (non-driver leaves licence blank).
- 🔵 **Smooth noise:** **binning** (bin means / medians / boundaries) · regression · outlier/cluster analysis.
- 🔵 **Process:** discrepancy detection via metadata + stats (**> 2σ** flags) · unique / consecutive / null rules · scrubbing & auditing tools.

## 🖤 Zone 4 - SHRINK it: data reduction (§3.4)
> Smaller in volume, **same analytical result**.

| Strategy | What | Methods |
|---|---|---|
| **Dimensionality** | fewer attributes | **PCA**, wavelet (DWT), attribute subset selection |
| **Numerosity** | smaller data form | regression / log-linear · **histograms, clustering, sampling, cube agg** |
| **Compression** | encode smaller | **lossless** vs **lossy** |

- 🔵 **Attribute subset selection** = greedy: forward · backward · decision-tree induction (2ⁿ subsets, can't brute-force). **Sampling:** SRSWOR / SRSWR / cluster / stratified.

## 🖤 Zone 5 - DO it in PySpark (Lee & Drabas Ch.4 = the A2 toolkit)
- 🔵 **Dupes:** `dropDuplicates(subset=...)` · **Missing:** `dropna(thresh=k)` / `fillna(dict)` · **Outliers:** `approxQuantile(c,[.25,.75],e)` → IQR rule.
- 🔵 **Explore:** `describe(cols)` · `groupBy().agg(mean,stddev,...)` · `corr('a','b')` (Pearson) · histograms via `.rdd...histogram(n)`.
- 🔴 **Keep heavy compute IN Spark - never `.collect()` a big DataFrame to the driver** (it crashes). Reduce first, pull only the small summary to plot.

## 🔴 Assessment Hook (bottom red strip)
> **A2 = Visualisation and Model Development** · source code + report (**1000 words** ±10%) · **30%** · due **26/07/2026** · SLOs **c) d) e)**.
> Module 5 is "familiarise with the A2 brief" week - its statistics, visualisation, cleaning and reduction (run in PySpark) **are** the A2 toolkit. The LA1/LA2 Bank-Marketing notebook is your A2 warm-up.

## 🔴 If you only memorise 5 things
1. **Attribute type decides the statistic** - never average a nominal; use the **median for skew**.
2. **Outliers = beyond `1.5·IQR`** past Q1/Q3 (boxplot whiskers; same rule in PySpark).
3. **Missing-value ladder:** ignore → constant → mean/median → **most-probable (best)**; missing ≠ error.
4. **Reduction = dimensionality (PCA) · numerosity (sampling/histograms) · compression (lossless/lossy)**.
5. **PySpark verbs:** `dropna`/`fillna`/`approxQuantile`/`describe`/`groupBy.agg`/`corr`/`.rdd.histogram` - keep compute in Spark.

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. In your warehouse, name 2 columns that are **nominal codes you must never average** and 2 that are **true ratio measures** - what breaks if you confuse them?
2. A customer table with missing `income`: which rung of the **missing-value ladder** would you defend to a stakeholder, and why **median over mean** when balances are right-skewed?

### This-week to-dos (still 🔥 in your notes)
- [ ] 🔥 Run the **LA1/LA2 PySpark notebook** on Colab (Bank Marketing `bank.csv`), check outputs vs the reference appendix
- [ ] 🔥 Post **Activity 1** (data exploration) and **Activity 2** (cleaning: drop `Job` = unknown/unemployed, re-run) discussion forums
- [ ] **Familiarise with the Assessment 2 brief** (Visualisation & Model Development, due 26/07/2026)
- [ ] Module 5 **knowledge check** quiz (LMS)
