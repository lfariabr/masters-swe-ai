# Module 4 - Analytics Engine for Big Data - Apache Spark

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Drabas, Lee & Karau (2017) - Understanding Spark (Ch. 1) | ✅ |
| **2** | Watch & summarise LinkedIn Learning (2019) - PySpark DataFrame API (Section 3) | ✅ |
| **3** | Watch & summarise LinkedIn Learning (2019) - PySpark Built-in Functions (Section 4) | ✅ |
| 4 | Activity: install PySpark + run the DataFrame/Functions notebooks on a real CSV | 🕐 |
| 5 | Activity: Module 4 Interactive Knowledge Check (LMS) | 🕐 |

---

## Key Highlights

### 1. Drabas, T., Lee, D. & Karau, H. (2017). Chapter 1: Understanding Spark. In Learning PySpark.

**Citation:** Drabas, T., Lee, D. & Karau, H. (2017). Chapter 1. Understanding Spark. In *Learning PySpark* (pp. 1-15). Birmingham, England: Packt.

**Purpose:** Introduces Apache Spark as a fast, distributed processing engine - its origin, ecosystem, the execution model (driver / executors / DAG), and the foundational abstraction (RDDs) that everything else (DataFrames, Datasets) is built on.

> **Source-boundary note (honesty):** the supplied PDF excerpt runs **pp. 1-5**, ending at the RDD section. The later topics the chapter advertises - DataFrames vs Datasets, the Catalyst Optimizer, Project Tungsten and the Spark 2.0 architecture - are summarised in Theme 4 below from the broader *Learning PySpark* chapter and standard Spark references, and are reinforced hands-on by Resources 2-3. The boundary is flagged so the source attribution stays honest.

---

#### 1. What is Apache Spark?
- **Definition:** an open-source **distributed querying and processing engine**. Keeps the flexibility/extensibility of MapReduce but runs **up to 100x faster in memory** (≈10x faster on disk).
- **Origin:** built by **Matei Zaharia** (UC Berkeley PhD), v1 released **2012**, donated to the **Apache Software Foundation** (now its flagship project); Zaharia co-founded **Databricks** in 2013.
- **Polyglot APIs:** Java, Scala, Python, R, SQL. (Spark + Python = **PySpark**.)
- **Runs anywhere:** locally on a laptop, standalone, on **YARN** or **Apache Mesos**, on-prem cluster or cloud.
- **Reads/writes diverse sources:** HDFS, Apache Cassandra, Apache HBase, Amazon S3.
- **One unified stack of libraries** (combine them in the same app):

| Library | Purpose |
|---|---|
| **Spark Core** | the RDD engine + execution |
| **Spark SQL** | structured queries over DataFrames |
| **Spark Streaming** | real-time (DStreams + Structured Streaming) |
| **MLlib / ML** | machine learning |
| **GraphX / GraphFrames** | graph processing |

#### 2. Spark Jobs & the Execution Process
- **Driver process** (master node): one per application; holds the SparkSession, builds the plan, decides the number and composition of tasks. Can contain multiple jobs.
- **Executor processes** (worker nodes): run the tasks; any worker can run tasks from multiple jobs.
- **DAG (Directed Acyclic Graph):** every job is a chain of object dependencies organised as a DAG. The **DAGScheduler** is stage-oriented - it optimises scheduling (how many tasks/workers) and tries to **avoid shuffling** (the most resource-intensive operation).

| Term | What it is |
|---|---|
| **Driver** | master process; plans and coordinates |
| **Executor** | worker process; runs tasks |
| **Job** | full computation triggered by an action |
| **Task** | unit of work sent to an executor |
| **DAG** | dependency graph Spark optimises before running |

#### 3. RDD - Resilient Distributed Dataset (the foundation)
- **Definition:** an **immutable, distributed** collection of JVM objects. In PySpark, the Python data is stored *inside* these JVM objects.
- **In-memory + cached:** orders of magnitude faster than disk-based Hadoop.
- **Two operation types:**
  - **Transformations** (`map`, `filter`, `reduce`) - return a pointer to a *new* RDD; **lazy** (nothing computes yet).
  - **Actions** (`count`, `collect`, `take`) - return a value to the driver and **trigger** the computation.
- **Lazy evaluation:** transformations only run when an action fires, so Spark can optimise the whole query first.
- **Lineage / fault tolerance:** by logging every transformation, an RDD keeps a **data lineage** (an ancestry graph). If a partition is lost, Spark **recomputes** it from lineage instead of relying on replication.
- 🔴 **Coarse-grained + immutable:** transformations apply to the whole dataset in parallel - you cannot update one record in place. Same "append-only / immutable" idea as **HDFS in Module 3**.

#### 4. DataFrames, Datasets & the Catalyst/Tungsten optimisers (pp. 6-15 + Resources 2-3)
- **DataFrame:** an RDD organised into **named columns** - conceptually a table in a relational DB, a pandas DataFrame, or a spreadsheet, but **distributed across many machines**. The high-level API; usually **easier and faster** than raw RDDs because it passes through the optimiser.
- **Dataset:** a **strongly-typed** API available only in **statically-typed languages (Java/Scala)**. **Python (dynamically typed) has no Dataset API** - but gets most of the benefit through DataFrames.
- **Catalyst Optimizer:** Spark SQL's query optimiser - turns your DataFrame/SQL into an optimised physical plan.
- **Project Tungsten:** memory/CPU optimisations (off-heap memory, whole-stage code generation) that make DataFrame operations fast.
- 🔴 **A1 rule of thumb:** prefer **DataFrames over RDDs** - same answer, less code, and the optimiser does the heavy lifting.

#### Key Takeaways for BDA601
1. Spark is the **analytics engine** that sits on top of the data hub designed in Modules 2-3 - the "process at scale" tool for the data analytics lifecycle (Module 1).
2. **Why Spark over Hadoop/MapReduce:** in-memory + lazy DAG optimisation = up to 100x faster; **one unified stack** (SQL, streaming, ML, graph) instead of stitched-together tools.
3. **RDD → DataFrame → Dataset** is the abstraction ladder; in PySpark you live in **DataFrames**.
4. **Lineage** (recompute lost partitions) is Spark's answer to fault tolerance - the resilience theme that runs across the subject.
5. For **Assessment 1**, Spark/PySpark is the natural **processing/consumption layer** of the pipeline; name it as the engine that runs analytics on your stored, integrated data.

---

### 2. LinkedIn Learning (2019). Working with the DataFrame API (Section 3). Apache PySpark by Example.

**Citation:** LinkedIn Learning (2019, January 31). Working with the DataFrame API, Apache PySpark [Video file].

**Purpose:** Hands-on Section 3 - how to load data into a DataFrame and manipulate it at the row and column level in PySpark, with pandas syntax shown side-by-side for an easy transition. Uses the public **Chicago Reported Crimes** dataset.

---

#### 1. DataFrames vs RDDs (the two APIs)
- **DataFrames = high-level API** (easy to start, covers most on-the-job needs); **RDDs = low-level API**.
- Spark originally shipped only RDDs (MapReduce-style). DataFrames were added to attract **data analysts/scientists** already fluent in R/pandas DataFrames.
- A Spark DataFrame is a **distributed table** - it can span hundreds of machines (unlike a single-machine Excel/pandas frame).
- Build a DataFrame from: structured files, Hive tables, external DBs, or existing RDDs.
- **Dataset API** is statically-typed (Java/Scala) only; **Python uses DataFrames**.

#### 2. Loading & viewing data
- **SparkSession** is the entry point: `import pyspark`, then access via `spark`.

| Goal | PySpark | Notes |
|---|---|---|
| Read CSV | `spark.read.csv('file.csv')` | pandas: `pd.read_csv` |
| First *n* as list | `df.take(3)` | returns Row objects |
| All data | `df.collect()` | ⚠️ pulls everything to the **driver** - can crash it on big data |
| Pretty print | `df.show(3)` | formatted table |
| First *n* as new DataFrame | `df.limit(n)` | `head`/`take` return a **list**; `limit` returns a **DataFrame** |

- Under the hood: `take` calls `collect` on `limit`; `head` calls `take`; `show` just prints.

#### 3. Working with columns
| Operation | PySpark |
|---|---|
| Access a column | `df.col` (dot) or `df['col']` (bracket - needed when names clash with reserved attributes) |
| List column names | `df.columns` |
| Select columns | `df.select('a','b')` |
| Add a column | `df.withColumn('new', df.x * 2)` |
| Rename | `df.withColumnRenamed('old','new')` (no-op if column missing; returns new DF) |
| Drop | `df.drop('col')` (no-op if column missing) |
| Group + aggregate | `df.groupBy('col').count()` (always end a `groupBy` with an aggregation) |

- **Immutability:** every operation returns a **new** DataFrame.

#### 4. Working with rows
| Operation | PySpark | pandas |
|---|---|---|
| Filter | `df.filter(condition)` | `df[df.col …]` |
| Unique rows | `df.select('col').distinct()` | `.unique()` |
| Sort | `df.orderBy('col')` (use `ascending=False` to reverse) | `.sort_values()` |
| Append rows | `df.union(df2)` - needs **same columns + schema** or it fails | `pd.concat` |

- **Worked example (Chicago crimes):** add one extra day via `union`; then `groupBy('Primary Type').count().orderBy('count', ascending=False)` → the top reported crime is **theft**.

#### Key Takeaways for BDA601
1. This is the practical **SLO c/d** skill - actually transforming big data with PySpark, not just describing it.
2. The pandas ↔ PySpark mapping is the fast on-ramp: same mental model, distributed execution underneath.
3. The **`collect()` warning** ties straight back to the driver/executor model from Resource 1 - never pull a huge DataFrame to the driver.
4. `groupBy + aggregation + orderBy` is the bread-and-butter analytics pattern you will reuse throughout the subject.
5. Immutability + `union` schema rules echo the "append-only / schema discipline" themes from Modules 2-3.

---

### 3. LinkedIn Learning (2019). Functions (Section 4). Apache PySpark by Example.

**Citation:** LinkedIn Learning (2019, January 31). Working with the DataFrame API, Apache PySpark [Video file].

**Purpose:** Section 4 - PySpark's built-in functions (string / date / math), why built-ins beat user-defined functions on performance, date parsing and formatting, and joining DataFrames.

---

#### 1. Built-in functions
- Imported from **`pyspark.sql.functions`**.
- **Strings:** `lower`, `upper`, `substring` (⚠️ position is **1-based**, not 0-based).
- **Dates:** `dayofweek`, `date_add`, `date_sub`, `date_format`, plus `min`/`max`.
- **Math:** `sin`, `cos`, `log`, etc.
- Practical habit shown: **guess the name → `help(func)` → read the doc** (the API is discoverable).

#### 2. Working with dates
- Date parsing uses Java's **SimpleDateFormat** pattern letters: `yyyy` year, `MM` month-number, `MMM` month-text, `dd` day, `HH:mm:ss` time, `E` day-name, `a` AM/PM.
- **`to_date`** and **`to_timestamp`** convert a string column into a real date/timestamp given the format string.
- Pre-processing the crime data: `to_timestamp(col('Date'), 'MM/dd/yyyy hh:mm:ss a')`, then filter by date.

#### 3. User-Defined Functions (UDFs) & the performance trap
- You **can** write your own functions (applied **row by row**) and register them with Spark for use on all workers.
- **Why built-ins come first:** a **Python** UDF forces Spark to (1) serialize the function, (2) start a **separate Python process** on each worker, (3) **serialize the data** across to Python row by row, then return results to the JVM. That serialization is expensive, and Spark loses control of worker memory → workers can crash (Python and the JVM compete for memory).
- **Rule of thumb:** avoid Python UDFs and a PySpark program runs **roughly as fast as Scala Spark**. If you must write one, do it in **Scala/Java** (runs in the JVM, little penalty). **Apache Arrow** (Wes McKinney) is the longer-term fix - standardises columnar memory so the serialization step goes away.
- 🔴 **One-liner:** *built-in > UDF, always - UDFs break Spark's optimiser and serialization model.*

#### 4. Joins
- A join brings together a **left** and a **right** DataFrame on one or more keys.
- Syntax: `df.join(df2, df.key == df2.key, 'inner')`.

| Join type | Keeps rows with keys in… |
|---|---|
| **Inner** | both left and right |
| **Outer (full)** | either left or right |
| **Left outer** | the left dataset |
| **Right outer** | the right dataset |

- **Worked example:** join crimes (district number with **leading zeros**) to police-station names; needed `lpad(col('DISTRICT'), 3, '0')` to match the key formats, then a **left outer join** to keep all crime rows, then `drop` the unwanted columns.
- **Performance tip shown:** `df.cache()` then run an action (`count()`) to materialise it before repeated use (cache is lazily evaluated).

#### Key Takeaways for BDA601
1. **Built-in > UDF** is the single most exam-worthy performance lesson - and the "why" (serialization across JVM ↔ Python) reinforces the driver/executor architecture from Resource 1.
2. Date handling via SimpleDateFormat + `to_timestamp` is exactly the kind of **cleaning** you would cite in the integration/management tier (Module 3).
3. **Joins** are how you **enrich** data with reference tables (district number → district name) - the practical face of "enrichment" from Module 3.
4. `cache()` + an action ties back to **lazy evaluation / actions vs transformations** (Resource 1).
5. These are the concrete PySpark verbs you would demonstrate for **SLO d** (apply an analytics engine) in coursework.
