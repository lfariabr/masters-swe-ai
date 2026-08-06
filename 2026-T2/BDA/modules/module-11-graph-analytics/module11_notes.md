# Module 11 - Graph Analytics

## Task List

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Loshin (2013) - Using Graph Analytics for Big Data | ✅ |
| **2** | Read & summarise Erickson (2026) - What Is a Graph Database? | ✅ - ⚠️ see source-update note in §2 (live Oracle page has changed since notes.md's undated citation) |
| **3** | Read & summarise Joshi (2020) - A Guide to Link Prediction | ✅ |
| **4** | Watch & summarise Kent (2017) - SEO: Link Building in Depth: PageRank | ✅ |
| 5 | Activity 1: University Popularity Ranking Using PageRank Graph Analytics (discussion forum) | 🕐 |
| 6 | Activity 2: Facebook Graph Analytics (discussion forum) | 🕐 |

**Local sources (this folder):**
- `r1_Using-Graph-Analytics-for-Big-Data_Loshin-2013.pdf` (Resource 1)
- `r2_What-Is-a-Graph-Database_Erickson-2026.pdf` (Resource 2; notes.md cites "Oracle.com (n.d.)" but the saved page is now a dated, bylined Jeffrey Erickson piece - see mismatch note in §2)
- `r3_A-Guide-to-Link-Prediction_Joshi-2020.pdf` (Resource 3 - also Activity 2's source article)
- `r4_PageRank-transcript_Kent-2017.md` (Resource 4 - video transcript)

---

## Key Highlights

### 1. Using Graph Analytics for Big Data (Loshin 2013)

**Citation:** Loshin, D. (2013). *Big data analytics: From strategic planning to enterprise integration with tools, techniques, NoSQL, and graph* (Chapter 10, pp. 91-103). Waltham, MA: Morgan Kaufmann.
**Local source:** `r1_Using-Graph-Analytics-for-Big-Data_Loshin-2013.pdf`

**Purpose:** The module's textbook chapter - the formal grounding for what graph analytics is, when to choose it over a relational/warehouse approach, and why it's technically harder to scale than standard big data platforms.

---

#### 1. The graph model, in one paragraph

- A **graph** = a collection of **vertices** (nodes - entities like customers, products, locations) connected by **edges** (relationships - "purchased," "is married to," "is employed by").
- 🖤 **Enhancements that add meaning:** vertices/edges can be **labeled** (what type of entity/relationship), edges can be **directed** (flow) or **weighted**, and both can carry **properties** - a plain unlabeled undirected graph has "limited utility" on its own.
- **Triples (RDF):** subject → predicate → object, e.g. "John Smith - is father of - Brad Smith." A collection of triples is a **semantic database**. This is the standards-based representation (RDF + SPARQL) a real graph analytics platform is expected to support.

#### 2. When to choose graph analytics over a data warehouse

| Signal | What it means |
|---|---|
| **Connectivity** | The problem needs analysis of relationships/connectivity across many entity types |
| **Undirected discovery** | You're doing iterative, exploratory analysis for unknown patterns - not running a known report |
| **Absence of structure** | Source data has no consistent imposed schema |
| **Flexible semantics** | Meaning depends on context attributed to connections, not fixed columns |
| **Extensibility** | New data sources/streams need to be added on the fly |
| **Knowledge embedded in the network** | The relationships *are* the insight, not just an attribute |

- 🔴 **The core contrast:** relational/warehouse systems are built for known, structured, batch-oriented queries; graph analytics is built for **undirected, exploratory "discovery" analysis** - inferencing, pattern identification, deduction - especially when the question wasn't known in advance. Graph analytics is explicitly framed as **complementary to, not a replacement for**, existing warehouses/OLAP/Hadoop environments.

#### 3. Use cases and algorithm families

- **Use cases:** healthcare quality analytics (comparing treatment effectiveness across patient histories), concept-based correlation discovery (investigative journalism, fraud analysis across organisations), cybersecurity (real-time detection of attack patterns in streaming network logs).
- **Algorithm families:** community/network analysis (tightly-connected groups), path analysis (shape/distance between entities), clustering (grouping by vertex/edge properties), pattern detection, probabilistic graphical models (Bayesian/Markov networks), and **graph metrics** - degree (edges in/out of a vertex), centrality, and distance.

#### 4. Why graphs are technically hard to scale

- **Unpredictable memory access:** graph traversal follows links dynamically, unlike structured queries where access patterns can be pre-fetched/streamed efficiently - lots of time is spent waiting on memory, not computing.
- **Preferential connectivity (graph growth):** as graphs grow, new entities are more likely to connect to already-popular nodes - growth isn't evenly distributed across the structure.
- **Hubs complicate partitioning:** small groups of highly-connected nodes shorten distances (good for analysis) but make it hard to split the graph across processing units without huge cross-partition network traffic (bad for distributed compute).

#### Key Takeaways for BDA601
1. **This is the "why graphs, and why they're hard" chapter** - R2/R3/R4 all assume this context; if an assessment or exam asks "when would you choose graph analytics over a relational approach," the five-signal checklist (§2) is the citable answer.
2. **Complementary, not a replacement** - the explicit "graph analytics augments, doesn't replace, existing warehouses/OLAP/Hadoop" framing is worth remembering if a question tries to frame this as an either/or choice.
3. **Day-job anchor:** Synergetic/SEQTA/Schoolbox data is fundamentally relational - but a question like "which staff, subjects, and co-curricular groups cluster around a given student's engagement pattern" is exactly the kind of undirected, relationship-first question this chapter says a graph model is suited for and a table-per-entity schema is not.

---

### 2. What Is a Graph Database? (Erickson 2026)

⚠️ **Source-update note:** notes.md cites this as "Oracle.com. (n.d.). *Graph database*." The PDF actually saved in this folder is a dated, bylined article - **Jeffrey Erickson, "What Is a Graph Database?", Oracle, 9 January 2026** - at the same URL (`oracle.com/big-data/what-is-graph-database`). Same publisher, same page, but the content has clearly been substantially rewritten/updated since the module citation was written (same pattern as Module 10's Rai erratum). Treat the Key Highlights below as describing the **current** version of the resource.

**Citation:** Erickson, J. (2026, 9 January). *What is a graph database?* Oracle. Retrieved from https://www.oracle.com/big-data/what-is-graph-database
**Local source:** `r2_What-Is-a-Graph-Database_Erickson-2026.pdf`

**Purpose:** The module's vendor-authored primer on graph databases specifically (as opposed to graph analytics generally) - it adds the property-graph vs RDF-graph distinction and several concrete industry use cases Loshin's chapter only gestures at.

---

#### 1. Graph database vs relational database

- A **graph database** stores entities as **nodes** and relationships as **edges** as first-class citizens - relationships are directly queryable, not reconstructed via joins at query time the way a relational database does.
- 🖤 **The headline performance claim:** because relationships are pre-stored, graph queries can run in **subseconds** on problems that would take a relational database "hours or days" of joins to answer.
- **Query languages:** Cypher, Gremlin, PGQL, SQL (via graph extensions).

#### 2. Property graphs vs RDF graphs

| Type | Focus | Best for |
|---|---|---|
| **Property graph** | Analytics and querying; vertices/edges carry attributes ("properties") | Finance, manufacturing, retail, public safety - general analytics workloads |
| **RDF graph** (knowledge graph) | Data integration and semantic search; represented as subject-predicate-object **triples** with URIs | Linked data, complex metadata, government/pharma/healthcare data exchange; increasingly used to train/ground LLMs (e.g. DBpedia) |

- This directly extends Loshin's triple/RDF section (§1.1) with a concrete "which one do I pick" framing.

#### 3. Worked example: Six Degrees of Kevin Bacon

- Nodes = actors + films; edges = "acted in." Query "shortest path from Bacon to Miss Piggy" returns a **shortest-path analysis** result (Bacon → Meryl Streep → Billy Connolly → Miss Piggy).
- Same dataset answers different question types via different graph metrics: **degree centrality** ("who worked with the most actors"), **closeness centrality** ("average distance between Bacon and everyone else").
- 🖤 This is the clearest small-scale illustration in the module of how one graph structure supports multiple distinct algorithmic questions just by choosing a different metric.

#### 4. Real-world use cases (the module's most concrete list)

- **Social media bot detection:** Oracle's own case study - bots repost content to inflate popularity, producing a detectably different connection pattern (density + repost count) than naturally popular accounts. Flagging based on this pattern hit **91.2%** accuracy (89% suspended, 2.2% deleted after a month's follow-up check).
- **Credit card fraud:** nodes = accounts, purchase locations, purchase categories, transactions, terminals. Anomalies (a Bay Area cardholder suddenly transacting in Florida at night) get flagged by deviation from established connection patterns.
- **Money laundering:** a query finds accounts sending funds to each other while sharing identity attributes (email, address, phone) across "different" synthetic identities - a pattern a table-per-account view would never surface without an explicit, expensive multi-way join.

#### Key Takeaways for BDA601
1. **This resource is "graph database" as a product category, not "graph analytics" as a technique** - useful to distinguish in an exam answer: analytics is the *what* (algorithms/questions), the database is the *where it runs* (storage + query engine that makes those algorithms fast).
2. **The fraud/bot examples are the module's most citable "why graphs win" stories** - same rhetorical role as Module 10's Walmart anecdotes: a correlation only a relationship-first structure surfaces efficiently.
3. **Day-job anchor:** the money-laundering pattern (shared attributes across nominally-different accounts) is structurally the same problem as detecting duplicate/synthetic family records across Synergetic - if two "different" parent contacts share an email, phone, and address, that's a graph question (shared-attribute clustering), not a simple `WHERE` filter.

---

### 3. A Guide to Link Prediction - How to Predict your Future Connections on Facebook (Joshi 2020)

**Citation:** Joshi, P. (2020, 16 January). *A guide to link prediction - How to predict your future connections on Facebook*. Analytics Vidhya. Retrieved from https://www.analyticsvidhya.com/blog/2020/01/link-prediction-how-to-predict-your-future-connections-on-facebook/
**Local source:** `r3_A-Guide-to-Link-Prediction_Joshi-2020.pdf` (also Activity 2's source article)

**Purpose:** The module's only hands-on, code-driven resource - turns a graph problem (will these two nodes connect?) into a standard supervised ML problem (binary classification), which is exactly what Activity 2 asks you to walk through.

---

#### 1. Link prediction, framed as supervised learning

- 🖤 **Link prediction** asks: for two currently-unconnected nodes, will a link form between them in the future? Real uses: product recommendations (Amazon), employee-collaboration suggestions, terrorist-network analysis.
- **The reframing trick:** you can't do supervised learning without features + a target variable - but a graph doesn't obviously have either. The fix is to derive both **from the graph itself**: compare the graph at time *t* vs time *t+n* - node pairs that gained a link get **target = 1**, pairs that stayed unconnected get **target = 0**.
- **Real-world constraint:** you usually only have *one* snapshot of the graph (the present), not a "future" version to compare against.

#### 2. Building a training set from a single graph snapshot

1. **Negative samples (unconnected pairs):** build the graph's **adjacency matrix** (1 = linked, 0 = not linked), traverse it, and collect all pairs with a 0 - these become `link = 0` rows. (In the Facebook case study: 620 nodes → **19,018** unconnected pairs.)
2. **Positive samples (simulated "future" links):** since there's no real future snapshot, **randomly remove existing edges** - but only if removing an edge doesn't split the graph into disconnected components or strand a node. The removed edges become `link = 1` rows (**1,483** in the case study).
3. 🔴 **Class imbalance is structural, not a data-quality issue:** 19,018 negatives vs 1,483 positives - a real-world graph naturally has far more non-links than links. This is *why* the article uses `class_weight="balanced"` for logistic regression and `is_unbalance: true` for LightGBM.

#### 3. Feature extraction: node2vec

- **node2vec** generates a vector representation for every node via biased random walks (similar to DeepWalk) - features for a node *pair* are computed by **summing the two nodes' vectors**.
- This is the step Activity 2 asks you to interrogate: node2vec parameters used were `dimensions=100, walk_length=16, num_walks=50`.

#### 4. Model results - two models compared

| Model | AUC-ROC | Note |
|---|---|---|
| Logistic Regression (`class_weight="balanced"`) | 0.7817 | Simple baseline |
| LightGBM (`is_unbalance: true`, early stopping at iteration 208) | **0.9273** | Substantially stronger - the article's headline result |

#### Key Takeaways for BDA601
1. **This IS Activity 2's source material.** The activity asks you to summarise the outputs under "Dataset Preparation for Model Building" and consider whether any code there could be removed without changing the outcome - the negative-sampling (adjacency matrix traversal) and positive-sampling (removable-edge check) steps in §2 above are the two blocks to focus on; both are necessary (removing either collapses the training set to all-negative or risks a disconnected graph), which is the citable answer if the activity is asking you to justify that.
2. **Class imbalance (19,018 vs 1,483) is the module's most transferable ML lesson** - it's not a graph-specific quirk, it's what happens whenever you frame a "does X happen" problem as classification over all possible pairs; the fix (`class_weight`/`is_unbalance`) generalises well beyond graphs.
3. **Day-job anchor:** framing "will these two things connect in the future" as a supervised problem over node-pair features is the same pattern you'd use to predict "will this family enrol a sibling" or "will this donor lapse" - derive positive/negative examples from historical Synergetic snapshots rather than needing a literal future dataset.

---

### 4. SEO: Link Building in Depth - PageRank (Kent 2017)

**Citation:** Kent, P. (2017, 12 July). *SEO: Link building in depth: PageRank* [Video file]. LinkedIn Learning.
**Local source:** `r4_PageRank-transcript_Kent-2017.md` (transcript)

**Purpose:** The module's algorithm deep-dive on PageRank specifically - directly feeds Activity 1, which asks you to explain PageRank in your own words using a real-world tool.

---

#### 1. PageRank, mechanically

- 🖤 **Core idea:** PageRank is a numerical value Google assigns to every webpage, based on the number and quality of links pointing to it - "websites vote for pages by linking to them."
- **Not all votes are equal:** a link from a **high-PageRank page** passes more value than a link from a low-PageRank page - PageRank is passed page-to-page, not site-to-site (every page in a site has its own rank).
- **Votes are shared/diluted:** a page's PageRank is split among *all* its outgoing links - a link from a page with only 1-2 outgoing links is worth more than the same-PageRank page with 50-100 outgoing links.
- 🔴 **The corporate-shareholder analogy the video uses:** some "shareholders" (pages) have more votes (PageRank) than others because they hold more "shares" (incoming links) - and each of their votes, when cast (linked out), is itself split across everything they link to.

#### 2. Why this matters for ranking

- When two pages are an equally good topical match for a search query, the page with the **higher PageRank** ranks higher - "the web has voted for that page."
- PageRank is one input among others Google doesn't fully disclose - but it's presented as foundational, and "all major search engines use something similar."

#### Key Takeaways for BDA601
1. **This is Activity 1's algorithm.** The activity asks you to rank universities by "External Backlinks" using an online PageRank tool and explain the algorithm in your own words - the vote/dilution mechanics above (more links = more votes, but votes are shared across outgoing links, and votes from high-PageRank pages count more) is the explanation to reuse.
2. **PageRank is a graph metric, not a separate technique** - it's a concrete instance of Loshin's "centrality" graph metric family (§1.3) and Erickson's degree/closeness centrality examples (§2.3), applied specifically to the WWW-as-a-graph.
3. **Day-job anchor:** the "votes shared across outgoing links" mechanic maps onto how influence/attention should be modelled in any network you'd analyse - e.g. a staff member connected to many students/committees "dilutes" their per-relationship influence the same way a page with many outgoing links dilutes its passed PageRank; concentration of connections (not just raw count) is what centrality measures actually capture.

---

## Where this module fits

- **Graph analytics is the module's third and last "alternative to relational/warehouse thinking"** after clustering (Module 9, groups records) and association rules (Module 10, finds item co-occurrence) - graphs ask a third kind of question: how are entities *connected*, and what can that connectivity structure itself tell you (Loshin §2, the "choose graph analytics" checklist)?
- **The throughline across four resources:** Loshin (R1) supplies the formal "what is it and when do I choose it" foundation; Erickson (R2) narrows to graph *databases* as the implementation layer and adds concrete fraud/bot use cases; Joshi (R3) is the only hands-on code resource, reframing link prediction as ordinary supervised ML over graph-derived features; Kent (R4) drills into one specific, famous graph metric (PageRank) that both activities lean on.
- **Activity 1** (PageRank ranking of universities) draws directly on R4's vote/dilution explanation - no coding required, just applying the concept to a real tool's output.
- **Activity 2** (Facebook link prediction code walkthrough) draws directly on R3 - the negative/positive sampling steps (§2) are the near-complete answer to "what does this code do and can any of it be removed."
- **Feeds Assessment 3?** No - A3 (due Week 12, 40%) requires **K-means** (Module 9) as its algorithm per the Week 9 lecture. Graph analytics, like Module 10's association rules, is curriculum breadth rather than a direct A3 requirement.
