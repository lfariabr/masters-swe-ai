# Module 4 - Class Notes (Week 4 Live Lecture)
## Analytics Engine for Big Data - Apache Spark · Dr. Chen Zhan

> **Source:** Week 4 live lecture recording (23 Jun 2026, ~3h16m), Dr. Chen Zhan. This file captures what the **lecture** emphasised on top of the textbook/video resources in [module04_notes.md](module04_notes.md). Where lecture and readings overlap (RDD, DataFrame/Dataset, lazy evaluation, built-in vs UDF) the resource notes carry the detail; this file focuses on the **conceptual framing**, the **architecture detail (cluster manager, stages, skew)**, and the **Assessment 1 debrief** that only appear live.

---

## TL;DR
Module 4 is about **scale**: an engine like Spark lets you work on huge data **as if it were small data on your laptop** - it hides the "dirty work" of distributing computation. The lecture's spine: (1) **one machine is not enough** (memory/disk overflow, swapping, long-job failures); (2) Spark is a **distributed engine, not a Python library** - its **optimization layer** is what makes it special; (3) architecture = **driver → cluster manager → executors**, entered through a **SparkSession** (`getOrCreate`); (4) you **describe** a plan, **lazy evaluation** lets Spark **reorder** it into a **DAG of stages** split at **shuffle** boundaries, then run it across **partitions** in parallel; (5) watch for **data skew** (the barrel effect); (6) Spark is the **scalable execution engine for the data analytics lifecycle** - it does not replace it. Spark's price: **lots of RAM**. A1 is **design only**, and the **code practical is not assessed**.

## 1. Why an analytics engine? (scale)
- **"At scale" / scalability** = even with very large data, the engine lets a developer "play with big data just like working on a small laptop." It **automatically handles the dirty work** - distributing tasks, optimising, choosing strategies.
- **Spark distributes computation across a cluster** (many nodes = laptops/cores/servers acting as one) while exposing a **high-level API** for analysts and scientists.

### The fundamental problem: 1 machine is not enough
Single-machine tools assume the data **and** the computation fit inside one computer. Big data breaks that:
- **Data exceeds local memory/disk.**
- **Intermediate results pile up** - algorithms produce middle results that accumulate and fill RAM (his example: a 32GB laptop runs out fast).
- **Disk swapping/paging** - forcing a laptop to chew big data means constantly swapping partitions between RAM and disk; less memory → more swaps → read/write thrashing slows everything.
- **Reads can be slower than the compute itself** for large volumes.
- **Failures get more likely on long jobs** → you need a strategy to **recover and pick up where you failed**, not restart from zero.
- **Team collaboration** - you need an abstraction/metadata layer to summarise intermediate results and brief collaborators. Spark keeps metadata about the workflow.

## 2. What is Spark (Dr. Chen's framing)
- A **distributed analytical engine**, **not just another Python library** - even though we drive it through the Python API (PySpark). PySpark = a Python interface that **talks to** the Spark engine.
- **Coordinates distributed computation across many machines**; provides an **API layer in multiple languages** (Python, R, SQL, Scala, Java) and reads from many platforms (SQL, NoSQL, files, ...).
- **What makes it unique = the optimization layer:** it plans, optimises, and executes transformations as distributed jobs so multiple machines work at once → speed.
- **Ecosystem = one engine, several workloads** (a unified platform): **Spark Core + Spark SQL + Structured Streaming + MLlib + GraphX**. A strong ecosystem drives adoption.
- **Spark Core** = the top-level component: schedules and distributes tasks, manages resources, and ensures **fault tolerance** (pick up at the break point on error).

## 3. Spark application architecture ⭐
**driver → cluster manager → workers/executors → tasks**
- **Driver** = the program you write/talk to (PySpark). It creates/gets a **SparkSession**. (Under the hood it uses a Java runtime - relevant only when you hit environment/config errors.)
- **Cluster manager** = allocates resources + distributes tasks; makes a set of machines ("imagine 5 laptops") behave as **one integrated unit**. It splits a job across workers so it runs ~5x faster than running sequentially on one laptop.
  - **In reality it is complex:** a university HPC cluster serves thousands of users; each node has different CPUs/cores/RAM/GPUs; users demand different resources (disk-heavy, CPU-heavy, GPU for deep learning). The manager **queues** requests (e.g. first-in first-served), sets **per-task/per-node limits**, and schedules accordingly.
- **Executors** (on worker nodes) run the tasks and **return results to the driver**.

### SparkSession = the entry point
- A **conceptual handle to Spark**, *not* the analytical task itself - the **connection between your program and the engine**.
- Used to **read data, create DataFrames, register temporary views, run Spark SQL**.
- **Every Spark program must create or get a session first** → `SparkSession.builder.appName(...).getOrCreate()` (get the existing one, else create - one session at a time).
- Key idea: **your program *describes* the computation; Spark decides *how* and *when* to execute** (when resources are free).

## 4. Three levels of data abstraction
- **RDD** - distributed collection of read-only records; **low-level**, less automatic optimization.
- **DataFrame** - distributed **table with named columns**; the main abstraction in PySpark ("just a table"). Spark handles the heavy lifting underneath.
- **Dataset** - **strongly-typed**, JVM languages (Java/Scala) only; rarely used from Python.

*(Verb-level detail in [module04_notes.md](module04_notes.md), Resources 2-3.)*

## 5. Lazy evaluation
- **Spark delays work until it is required.** Your code **defines a plan** (transformations); **actions trigger** execution.
- You **submit the whole plan as a batch**; Spark figures out **how/when** to run it - so it can **optimise the entire workflow**, not one command at a time.
- Analogy: like defining an ML model + parameters first, then choosing when to train.
- Practical tell: you always **build a chain of operations**, and nothing runs until an action (`show`/`collect`/`count`/`write`).

## 6. Logical plan → physical execution (the DAG)
- Your PySpark code = a **logical plan** of intent (download → dedup → drop missing → feature-engineer → ...).
- Submitted to Spark and recorded as a **DAG** (directed acyclic graph) of **dependencies** between steps (some sequential, some parallel).
- Spark then runs its **own optimization**:
  - **Reorders** steps for efficiency.
  - Splits the job into **stages** - a new stage begins where data must be **reshuffled** across the cluster.
  - Optimises the **physical plan** (e.g. the best physical way to sort a large dataset).
  - **Partitions** the work across nodes.
- You only **describe** the goal (e.g. "sort by this column"); Spark picks the physical strategy. This built-in optimization is *why* DataFrame / Spark SQL workflows are preferred.

## 7. Partitioning + data skew (the barrel effect) ⭐
- **Partitioning = the minimum unit of parallelism.** Split a huge dataset into partitions, send each to a different node, compute in parallel, then **combine** results.
  - **Lecture example:** national bowel-cancer screening data → partition patients **by city** → run the risk-screening algorithm per city in parallel → combine the high-risk lists → act (alert patients / suggest treatment).
- **Data skew = the "barrel/bucket" effect:** a wooden barrel holds water only up to its **shortest stave**. Likewise, if **one partition is much larger** than the others, it **dominates total runtime** - the pipeline cannot finish until that partition finishes (if it takes 1 hour, the whole job takes at least 1 hour).
- **Mitigations:** at the **planning stage**, avoid a single task being too large; if a big partition is unavoidable, **allocate more resources** (CPU cores / memory) to it. Efficient Spark needs attention to **partitioning, reshuffles, and work layout**.

## 8. DataFrame + Spark SQL
- **DataFrame** = distributed table with named columns - the fundamental data-science structure across R/Python.
- **PySpark SQL** lets you query DataFrames with **SQL-style logic**. *Why SQL?* Spark was built early (≈2009) when many engineers were SQL fans → **easy skill transfer** from databases to PySpark.
- **Data wrangling verbs** (all optimised internally): **select · filter · join · group by · aggregate · sort · write**.
- **Coding pattern:** load with `spark.read` → operate with SQL-like ops. *"The more Spark understands your operations, the more it can optimise"* → prefer SQL-style and built-ins.

## 9. Built-in functions vs UDFs (lecture angle)
- **Built-in functions** (aggregation, string, date, array) carry **Spark's optimization** → highest efficiency.
- **UDFs** (your own functions) are flexible but **usually slower** - and they **hide your logic from the optimiser**. *(The video adds the mechanical reason: Python UDFs force serialization across the JVM↔Python boundary - see [module04_notes.md](module04_notes.md) R3.)*
- **Rule:** lean on built-ins / SQL-style syntax so Spark can optimise planning, execution, and data movement.

## 10. PySpark data analytics lifecycle (ties back to Module 1)
Discovery (profile data fast, check availability/quality, describe, visualise) → **Data prep** (clean, join, aggregate) → **Model building** (distributed ML, feature prep; planning vs building split by lazy evaluation) → **Communicate** (summaries, dashboards, reports) → **Schedule/repeat** the pipeline + **productionise**.
- **Key link:** *Spark does not replace the analytics lifecycle - it gives data scientists/engineers a **scalable execution engine** for it.* This mirrors the Module 1 data-science lifecycle; Spark is the **tool**, not a new pipeline.

## 11. Runtimes, managed services & storage pairing
- **Run Spark on:** Hadoop **YARN**, Apache **Mesos**, **Kubernetes**, **Docker Swarm**.
- **Managed Spark:** Amazon **EMR**, Google Cloud **Dataproc**, Azure **HDInsight**, **Databricks**.
- **Classic pairing:** **HDFS** as the storage layer + **Spark** as the processing/interaction layer.

## 12. Spark's trade-off
- **Biggest disadvantage = the extreme amount of RAM** Spark needs for in-memory processing. Worth it for the speed, but real - and a likely quiz point.

## 13. Code practical / Learning Activity (LA1)
- **Tooling:** Dr. Chen **recommends Google Colab** - local PySpark needs a **Java runtime** that is "tricky to set up." Colab handles the environment for you. *(This is exactly the local-setup wall: PySpark does not support Python 3.14, and only Java 8 was installed - so use Colab, or a Python 3.11 + Java 11/17 setup.)*
- **Dataset:** City of **Chicago traffic-crash** data - **three** CSVs: `crash`, `people`, `vehicles`. Packages: `pyspark` + `gdown` (download from Google Drive links).
- **Pattern:** install → `gdown` download → `SparkSession.builder.appName('traffic crash analysis').getOrCreate()` → `spark.read` with `header=True`, `inferSchema=True`, CSV format → `printSchema()` / `show(5)`.
- **Ops used:** `select`, `filter`, `groupBy().count()`, `orderBy(desc(...))`, `withColumn` (cast `age` to int, build age-group buckets), `countDistinct`, `when`, `col`, `isin`, `max`/`spark_max`.
- **Questions explored:** ratio of crashes **with vs without cell-phone use** (flag per person → group by crash id → max flag per crash); **which age group** has the most crashes.
- **Live bug (learning point):** the `people` and `vehicles` download links were **swapped**, so `driver actions` (a *vehicles* column) was not where the code expected → errors. **Fix:** swap the two links / rename `people` ↔ `vehicles`. A clean version will be posted to Teams.
- 🟢 **Reassurance:** **this code practical is NOT part of Assessment 1** - "don't feel stressed." Similar tasks return in later modules.

## 14. Assessment 1 debrief (from this lecture)
Dr. Chen re-briefed A1 for a student. It **confirms the Week 3 plan**:
- **Critically analyse the online-retail business case** (same shape as last week's case study, different scenario), ~**1500-word** report. **No coding** - "project planning stage."
- **Identify data sources** aligned to the organisation's data-driven strategy: **primary/secondary · internal/external · structured/semi/unstructured**, plus the **possible columns in each source/table**.
- **Build an effective data pipeline**; identify **integration challenges**.
- **Design the data-lake storage & retrieval** so management teams + data scientists can retrieve efficiently. **Name the tools** (commercial or open-source) - e.g. **S3 bucket**, databases.
- **Provide a workflow diagram** - a good diagram strengthens the report.
- 🆕 **References/citations are NOT mandatory** (not in the rubric) - fine to include if you cite something, but unmarked.
- **Extensions** are available on request before the deadline.

---

### Day-job anchors
1. Your warehouse aggregation over millions of rows = a **DAG of stages**; the slow partition (one giant region/customer) is your **barrel's shortest stave** - how would you rebalance or resource it?
2. "Describe vs execute" = like building a SQL query plan before the DB runs it; **lazy evaluation** is the optimiser waiting for the full plan.
3. Spark = the **execution engine** under the same data-science lifecycle you already run - not a new process, just one that scales.
