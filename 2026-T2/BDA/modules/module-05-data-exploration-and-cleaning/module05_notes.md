# Module 5 — Data Exploration and Cleaning

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Han, Pei & Kamber (2012) — Getting to Know Your Data (§2.1–2.3) | ✅ |
| **2** | Read & summarise Han, Pei & Kamber (2012) — Data Preprocessing (§3.2 Cleaning, §3.4 Reduction) | ✅ |
| **3** | Read & summarise Lee & Drabas (2018) — PySpark Cookbook Ch.4: Preparing Data for Modeling | ✅ |
| **4** | Read & summarise ProjectPro (2020) — Why Data Preparation Matters | ✅ |
| 5 | Activity 1: Data Exploration using PySpark (Bank Marketing dataset) | 🕐 |
| 6 | Activity 2: Data Cleaning (remove `Job` = unknown/unemployed, re-run Activity 1) | 🕐 |

> **Source-boundary note:** Resource 2's overview lists §3.2, §3.4 **and §3.5** (Data Transformation & Discretization), but only the §3.2 and §3.4 PDF excerpts were supplied. §3.5 ideas (normalization, binning-as-discretization, concept hierarchies) are summarised here from cross-references inside §3.2/§3.4 and from the PySpark/ProjectPro readings, and flagged where used. The §3.2 PDF also ends mid-section (§3.2.3) and the §3.4 PDF stops inside §3.4.8 (Sampling); the tail (stratified sampling, data cube aggregation) is noted from the chapter's own forward references.

---

## Key Highlights

### 1. Han, J., Pei, J. & Kamber, M. (2012). Getting to Know Your Data (§2.1–2.3).

**Citation:** Han, J., Pei, J. & Kamber, M. (2011). *Data mining: Concepts and techniques*. Waltham, MA: Elsevier. (3rd ed., 2012). Chapter 2, §2.1–2.3 (pp. 39–65).

**Purpose:** Before you clean or model anything, you must understand the *shape* of your data — what kind of attributes you hold, where their values sit (central tendency), how spread out they are (dispersion), and how to *see* them. This is the diagnostic groundwork for every later preprocessing step.

---

#### 1. Data objects & attribute types (§2.1)
- **Data object** = an entity (a row / *tuple*); **attribute** = a characteristic of it (a column). Synonyms you will meet: object = sample / instance / data point; attribute = dimension (warehousing) / feature (ML) / variable (statistics).
- The **type of an attribute** is set by its possible values:

| Type | Meaning | Ordered? | Maths meaningful? | Valid central tendency | Example |
|---|---|---|---|---|---|
| **Nominal** | names / categories / codes | ❌ | ❌ | mode only | hair colour, occupation, marital status |
| **Binary** | 2 states (0/1, true/false) | ❌ | ❌ | mode | smoker?, medical test ±  |
| **Ordinal** | ranked, but gap size unknown | ✅ | ❌ | mode, median | drink size S/M/L, grades, military rank |
| **Numeric** | measurable quantity (int/real) | ✅ | ✅ | mean, median, mode | salary, temperature, age |

- **Binary** splits into **symmetric** (both states equally important, e.g. *gender*) vs **asymmetric** (rare outcome matters most → code the rare one as 1, e.g. *HIV positive*).
- **Numeric** splits into **interval-scaled** (equal-size units, *no true zero* → can rank and subtract but **cannot take ratios**, e.g. °C/°F, calendar years) vs **ratio-scaled** (inherent zero-point → ratios are valid, e.g. Kelvin, weight, height, counts, years of experience).
- Nominal/binary/ordinal = **qualitative**; numeric = **quantitative**.
- A second, orthogonal cut (ML language): **discrete** (finite or countably infinite — e.g. binary, age 0–110, zip codes, customer ID) vs **continuous** (real-valued, stored as floating-point).

#### 2. Basic statistical descriptions (§2.2)
**Central tendency — "where is the middle?"**
- **Mean** = arithmetic average; **weighted mean** when values carry weights; **trimmed mean** (chop the top/bottom few %) to resist outliers. ⚠️ The mean is **sensitive to extreme values**.
- **Median** = middle of the ordered data; the **better choice for skewed data**; can be interpolated for grouped/binned data.
- **Mode** = most frequent value; works for qualitative *and* quantitative; data can be unimodal / bimodal / multimodal.
- **Midrange** = (min + max) / 2.
- Shapes: **symmetric** → mean = median = mode. **Positively skewed** → mode < median < mean. **Negatively skewed** → mean < median < mode. Empirical rule (moderate skew): `mean − mode ≈ 3 × (mean − median)`.

**Dispersion — "how spread out?"**
- **Range** = max − min.
- **Quantiles** → **quartiles** (Q1 = 25th pct, Q2 = median, Q3 = 75th pct) and **percentiles**.
- **Interquartile range: `IQR = Q3 − Q1`.**
- 🔑 **Outlier rule of thumb: flag any value more than `1.5 × IQR` above Q3 or below Q1.** (This reappears verbatim in the PySpark recipe — resource 3.)
- **Five-number summary**: Min, Q1, Median, Q3, Max → drawn as a **boxplot** (box = IQR, line = median, whiskers to extremes, outliers plotted individually).
- **Variance σ²** and **standard deviation σ** = spread about the mean. σ = 0 only when all values are equal; otherwise σ > 0 (Chebyshev's inequality bounds how far data can sit from the mean).

**Graphic displays (visual stats):** quantile plot (one distribution at a glance), **q-q plot** (compare two distributions for a shift), **histogram** (numeric → equal-width/equal-frequency **bins/buckets**; nominal → **bar chart**), **scatter plot** (bivariate → spot **positive / negative / null correlation** and outliers).

#### 3. Data visualization (§2.3)
- Goal: communicate data clearly **and** reveal relationships not visible in raw numbers.
- Families to *recognise* (not memorise the maths):

| Family | Idea | Examples |
|---|---|---|
| **Pixel-oriented** | one coloured pixel per value, one window per dimension | sorted customer income/credit windows |
| **Geometric projection** | project high-D onto 2-D | scatter-plot **matrix**, **parallel coordinates** |
| **Icon-based** | map dimensions onto a glyph | **Chernoff faces** (≤18 dims), stick figures |
| **Hierarchical** | partition dimensions into nested subspaces | worlds-within-worlds (n-Vision), **tree-maps** |
| **Complex data / relations** | non-numeric + networks | **tag clouds**, disease-influence graphs |

#### Key Takeaways for BDA601
1. This is the exact **exploratory toolkit Activity 1 asks for** — mean/median/std, bar graph, histogram, *binning*, scatter plot — only executed **at scale via PySpark** (resource 3).
2. **Attribute type decides which statistic is legal**: never average a nominal code; use the median for skewed numerics. This judgement is what graders look for.
3. The **`1.5 × IQR`** outlier rule is the conceptual bridge into the data-cleaning reading and the PySpark `approxQuantile` recipe.

---

### 2. Han, J., Pei, J. & Kamber, M. (2012). Data Preprocessing — §3.2 Data Cleaning, §3.4 Data Reduction.

**Citation:** Han, J., Pei, J. & Kamber, M. (2011). *Data mining: Concepts and techniques*. Waltham, MA: Elsevier. (3rd ed., 2012). Chapter 3, §3.2, §3.4 (and §3.5, not supplied) (pp. 88–93, 99–120).

**Purpose:** Real-world data is *incomplete, noisy and inconsistent*. This reading is the **toolbox** for fixing it (cleaning) and shrinking it (reduction) so models train efficiently without losing the signal.

---

#### 1. Cleaning — handling missing values (§3.2.1)
Six methods, ordered roughly worst → best:

| # | Method | Note |
|---|---|---|
| 1 | **Ignore the tuple** | Only OK when the class label is missing; wasteful otherwise |
| 2 | **Fill manually** | Infeasible at scale |
| 3 | **Global constant** ("Unknown", −∞) | Simple, but the miner may treat "Unknown" as a real pattern |
| 4 | **Attribute mean / median** | mean for symmetric data, **median for skewed** |
| 5 | **Mean / median of the same class** | conditioning on the tuple's class |
| 6 | **Most probable value** (regression, Bayesian, decision tree) | ✅ uses the most information — the recommended strategy |

- ⚠️ Methods 3–6 **bias** the data (the fill may be wrong). A **missing value ≠ an error** (e.g. a non-driver legitimately leaves "licence number" blank — forms should allow "not applicable").

#### 2. Cleaning — smoothing noisy data (§3.2.2)
- **Binning**: sort values → partition into equal-frequency / equal-width **bins** → smooth by **bin means**, **bin medians**, or **bin boundaries** (replace each value with the nearest min/max of its bin). *Worked example:* bin {4, 8, 15} → mean smoothing → {9, 9, 9}. Binning is also a **discretization** and **reduction** technique.
- **Regression**: fit values to a function (simple / multiple linear regression).
- **Outlier analysis**: cluster the data; points falling outside the clusters are candidate outliers.

#### 3. Cleaning as a process (§3.2.3)
- Step 1 = **discrepancy detection**. Use **metadata** (data type, domain, acceptable values per attribute) plus the §2.2 statistics (mean/median/mode, range, σ — values **> 2σ from the mean** are potential outliers).
- Watch for **inconsistent codes / date formats** (`2010/12/25` vs `25/12/2010`) and **field overloading**.
- Enforce **unique rule** (all values distinct), **consecutive rule** (no gaps between low and high), **null rule** (how blanks/`?`/special chars are recorded).
- Tools: **data scrubbing** (domain knowledge + fuzzy matching) and **data auditing** (find rule/relationship violations — variants of data-mining tools).

#### 4. Data reduction (§3.4)
Goal: a representation that is **much smaller in volume yet keeps the analytical integrity** of the original (and the reduction time must not erase the time it saves).

| Strategy | What it does | Methods |
|---|---|---|
| **Dimensionality reduction** | fewer attributes / variables | **Wavelet transforms (DWT)**, **PCA**, **attribute subset selection** |
| **Numerosity reduction** | replace data with a smaller form | *parametric*: regression, log-linear · *non-parametric*: **histograms, clustering, sampling, data-cube aggregation** |
| **Data compression** | encode smaller | **lossless** (exact reconstruction) vs **lossy** (approximation) |

- **PCA** (Karhunen-Loeve): normalize → compute *k* orthonormal **principal components** (sorted by variance) → drop the weak (low-variance) ones → reconstruct a good approximation.
- **Attribute subset selection**: 2ⁿ possible subsets for n attributes, so use **greedy heuristics** — *stepwise forward selection*, *backward elimination*, *combination*, and *decision-tree induction* (attributes absent from the tree are deemed irrelevant). May also **construct** new attributes (e.g. `area = height × width`).
- **Histograms** as reduction: singleton vs equal-width / equal-frequency buckets.
- **Sampling**: **SRSWOR** (without replacement), **SRSWR** (with replacement), **cluster sample**, (stratified — chapter forward-reference).

#### Key Takeaways for BDA601
1. §3.2 **is Activity 2**: the owner declares `Job` = "unknown"/"unemployed" rows *inaccurate*, so you remove them — a textbook discrepancy-detection + tuple-removal cleaning step.
2. The **missing-value ladder** and **binning** map directly onto PySpark's `dropna` / `fillna` / `approxQuantile` (resource 3).
3. **Reduction (§3.4)** delivers the module's "reduce volume & complexity" SLO and ties back to **Module 4** — reduce *first*, then Spark models faster on less data.

---

### 3. Lee, D. & Drabas, T. (2018). PySpark Cookbook — Chapter 4: Preparing Data for Modeling.

**Citation:** Lee, D. & Drabas, T. (2018). *PySpark cookbook: Over 60 recipes for implementing big data processing and analytics using Apache Spark and Python*. Birmingham, UK: Packt. Chapter 4 (pp. 136–170).

**Purpose:** The hands-on companion — the same cleaning/exploration ideas, **executed in PySpark** on a small 22-row "dirty cars" dataset. This chapter is the working template for **both module activities**.

> Mantra: *"All data is dirty until proven otherwise."* Cleaning + getting familiar with data is **~80% of a data scientist's job** (the other 20% is modelling and complaining about cleaning).

---

#### 1. Handling duplicates
- Detect: compare `df.count()` vs `df.distinct().count()`; list dupes with `df.groupby(df.columns).count().filter('count > 1').show()`.
- Remove exact dupes: `df.dropDuplicates()`. "Same record, different ID": `df.dropDuplicates(subset=[cols except 'Id'])`.
- **ID collisions** (different records, same ID): mint fresh keys with `fn.monotonically_increasing_id()` (unique up to ~1B partitions × ~8B rows).

#### 2. Handling missing observations
- **Per row**: drop to the underlying RDD, `.map(lambda row: sum([c == None for c in row]))` to count nulls. Drop sparse rows with `df.dropna(thresh=4)` (keep rows with ≥ 4 non-null values); bare `dropna()` drops any row with any null.
- **Per column**: `1 - fn.count(c)/fn.count('*')` = missing %. Drop near-empty columns (the example drops `MSRP`).
- **Impute**: `df.fillna(value)` or `df.fillna({dict})`. The recipe builds **ratio-based multipliers** (`toPandas().to_dict('records')`) to fill `FuelEconomy`/`Cylinders` — "not totally accurate, but better than a predefined constant."

#### 3. Handling outliers
- Uses the **§2.2 IQR rule** directly: `approxQuantile(col, [0.25, 0.75], relErr)` → `IQR = Q3 − Q1` → bounds `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]` → flag and `filter` out. (relErr `0` = exact but expensive.)

#### 4. Descriptive statistics
- `df.describe(features)` → **count, mean, stddev, min, max** (works on string cols too, if oddly). Grouped stats via `df.groupBy('Cylinders').agg(fn.count, fn.mean, fn.stddev, …)` — also `skewness`, `kurtosis`, `var_pop`, etc.

#### 5. Computing correlations
- `df.corr('a', 'b')` (**Pearson only**). Build a correlation matrix with a manual double loop. Two features highly correlated with each other → keep **one** (multicollinearity makes models unstable).

#### 6. Histograms & scatter plots (visualization at scale)
- DataFrames have **no native histogram** → drop to RDD: `df.select(col).rdd.flatMap(lambda r: r).histogram(5)` returns `(bin_bounds, counts)`.
- 🔑 **Don't `.collect()` big data to the driver** — compute bin counts in Spark and return only the small summary, then plot locally (`registerTempTable` → `%%sql -o` → `matplotlib`/`bokeh`). Pulling everything to the driver "will break it."

#### Key Takeaways for BDA601
1. This chapter is literally **the verbs for both activities**: `dropDuplicates`, `dropna`, `fillna`, `approxQuantile`, `describe`, `groupBy().agg()`, `corr`, `.rdd.histogram()`.
2. Reinforces **Module 4**: keep heavy compute *inside* Spark, pull only small results to the driver (`.collect()` can crash it).
3. Connects the **theory** (IQR outliers, missing-value strategies from resources 1–2) to **working PySpark code** you can paste into the Bank Marketing notebook.

---

### 4. ProjectPro (2020). Why Data Preparation Is an Important Part of Data Science.

**Citation:** ProjectPro. (2020, 7 June). *Why data preparation is an important part of data science?* Retrieved from https://www.projectpro.io/article/why-data-preparation-is-an-important-part-of-data-science/242

**Purpose:** The **"why"** — the business and time-cost case that justifies the effort behind resources 1–3.

---

#### 1. Prep dominates the data scientist's time
- The headline: **50–80% of a data scientist's time** is spent collecting, cleaning and preparing data before any analysis (Steve Lohr, *NYT*). A CrowdFlower survey of ~80 data scientists: **60%** organizing/cleaning + **19%** collecting + 9% mining + 3% training + 4% refining algorithms.
- **57%** call cleaning the *most boring / least enjoyable* task — but it is unavoidable.

#### 2. Why it matters — the cost of skipping it
- **Rocket-ship analogy**: a better algorithm = a faster rocket; useless if it's pointed the wrong way. **Clean data points the rocket in the right direction** — *garbage in, garbage out*.
- **Gartner**: poor data quality costs an average organization **~$13.5 million per year**.
- "Predictive analysis results can only be as good as the data assembled."

#### 3. The 5 steps of data preparation (mirrors Han)

| Step | What |
|---|---|
| 1. **Data cleaning** | fill missing values, smooth noise, fix inconsistencies/duplicates |
| 2. **Data integration** | schema integration, resolve conflicts, remove redundancy |
| 3. **Data transformation** | normalization, aggregation, generalization |
| 4. **Data reduction** | dimensionality reduction, data-cube aggregation, numerosity reduction |
| 5. **Data discretization** | split continuous attributes into intervals (for algorithms that need categorical input) |

- **Need for cleaning**: discrepancies in names/codes; outliers/errors; missing attributes of interest; data that is merely quantitative, not qualitative.
- **Tools**: OpenRefine (GoogleRefine), DataCleaner; **Python (pandas)** and **R (dplyr, tidyr, reshape2, lubridate)** for wrangling.

#### Key Takeaways for BDA601
1. The **executive summary** of the whole module — it supplies the two quotable figures for your A1 narrative on data quality: **~80% of time** on prep and **~$13.5M/yr** cost of bad data (Gartner).
2. Its **5-step pipeline** lines up cleanly with Han's chapters and the broader **data analytics lifecycle (Module 1)** — cleaning/reduction are not busywork, they decide whether the model can be trusted.
3. Reinforces that data prep is a **learnable, code-driven craft** (Python/R/PySpark), not an afterthought — which is exactly what Activities 1–2 make you practise.
