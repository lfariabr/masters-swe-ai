# Module 11 - Graph Analytics

## TL;DR
- **What:** graph analytics represents entities as **nodes** and relationships as **edges**, then asks connectivity questions - who's linked to whom, how strongly, how the structure changes - a third lens alongside clustering (Module 9) and association rules (Module 10).
- **When to choose it:** exploratory/undirected discovery, no fixed schema, relationships carry the meaning - complements a relational warehouse rather than replacing it (Loshin 2013).
- **Graph databases** (Erickson 2026) store edges as first-class data for subsecond relationship queries - property graphs (analytics) vs RDF graphs (semantic search, knowledge graphs).
- **Link prediction** (Joshi 2020) reframes "will these nodes connect?" as supervised ML: derive positive/negative examples from one graph snapshot, extract features with node2vec, classify (LightGBM AUC 0.93 beats logistic regression AUC 0.78).
- **PageRank** (Kent 2017): pages vote for each other via links; votes from high-PageRank pages count more, and each page's vote is diluted across its outgoing links.
- 🔴 **Assessment 3 correction:** graph analytics is a **required, graded A3 section** (correlation-based network of a country and its "neighbours," explicitly NOT geography-based per the live lecture) - not curriculum breadth as earlier module notes claimed. See "From class" below.

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
- `BDA week 11.docx` (Week 11 live-class transcript, 11/08/2026), `BDA_S11_V2.pptx` (Week 11 slides) - source for the "From class" section (§5) and the Assessment 3 correction below

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
- **Triples (RDF):** subject → predicate → object, e.g. "John Smith - is father of - Brad Smith." A collection of triples is what Loshin's chapter calls a **semantic database** - more commonly termed an **RDF graph** or triplestore today, queryable via **SPARQL**.
  - ⚠️ **Dated claim, worth flagging:** Loshin (2013) states "any graph analytics platform must employ RDF" - true of the era's semantic-web-first tooling, but not true of the **property graphs** covered in R2 (Erickson 2026), which use Cypher/Gremlin/PGQL and don't require RDF at all. Treat RDF+SPARQL as one representation family, not a universal requirement.

#### 2. When to choose graph analytics over a data warehouse

| Signal | What it means |
|---|---|
| **Connectivity** | The problem needs analysis of relationships/connectivity across many entity types |
| **Undirected discovery** | Loshin's own term - "undirected" describes the *analysis approach* (iterative, exploratory, no known report shape), not the direction of graph edges |
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
1. **This is the "why graphs, and why they're hard" chapter** - R2/R3/R4 all assume this context; if an assessment or exam asks "when would you choose graph analytics over a relational approach," the six-signal checklist (§2) is the citable answer.
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

- **Social media bot detection:** Oracle's own case study - bots repost content to inflate popularity, producing a detectably different connection pattern (density + repost count) than naturally popular accounts. Of accounts flagged by this pattern, **91.2%** were later suspended or deleted (89% suspended, 2.2% deleted) when checked a month on - a strong outcome signal, though not a formal accuracy score against labelled ground truth.
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
1. **This IS Activity 2's source material.** The activity asks you to summarise the outputs under "Dataset Preparation for Model Building" and consider whether any code there could be removed without changing the outcome - the negative-sampling (adjacency matrix traversal) and positive-sampling (removable-edge check) steps in §2 above are the two blocks to focus on; both are necessary, but for different reasons: **skip negative sampling and the training set becomes all-positive** (no examples of "no link" to learn from); **skip positive sampling and it becomes all-negative**, and it's *this* step alone that carries the disconnected-graph risk, since it's the one removing real edges from the graph.
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

⚠️ **Historical model, not current Google reality:** Kent's 2017 explanation is a simplified, pre-2017 picture of PageRank. Google has since confirmed PageRank is only one of several ranking systems it uses, and the exact algorithm has evolved well beyond this description. Activity 1's tool (checkpagerank.net) is a **third-party site, not affiliated with Google** - its "External Backlinks" metric is a raw backlink count, not Google's actual (long-unpublished) PageRank score. Use Kent's vote/dilution mechanics to *explain the concept*, not to claim the tool's number *is* PageRank or that it drives current search rankings.

#### Key Takeaways for BDA601
1. **This is Activity 1's algorithm.** The activity asks you to rank universities by "External Backlinks" using a third-party online tool and explain the PageRank *algorithm* in your own words - the vote/dilution mechanics above (more links = more votes, but votes are shared across outgoing links, and votes from high-PageRank pages count more) is the explanation to reuse, with the caveat above that the tool's number is a backlink count, not a live Google PageRank score.
2. **PageRank is a graph metric, not a separate technique** - it's a concrete instance of Loshin's "centrality" graph metric family (§1.3) and Erickson's degree/closeness centrality examples (§2.3), applied specifically to the WWW-as-a-graph.
3. **Day-job anchor:** the "votes shared across outgoing links" mechanic maps onto how influence/attention should be modelled in any network you'd analyse - e.g. a staff member connected to many students/committees "dilutes" their per-relationship influence the same way a page with many outgoing links dilutes its passed PageRank; concentration of connections (not just raw count) is what centrality measures actually capture.

---

### 5. From class (Week 11 lecture + code practical, 11/08/2026)

🔴 **Correction to earlier modules' A3 claims:** Module 9's and Module 10's notes both stated A3 only requires K-means and that graph analytics/association rules are "curriculum breadth, not a direct requirement." **That was wrong for graph analytics** - checked directly against `BDA601_Assessment 3_20240603.pdf`: A3 is a four-part pipeline on the JHU COVID-19 dataset (top-3 infected countries by total case count): **(a) linear regression** per country (week number → infection count, pick the highest-variance country) → **(b) K-Means clustering** on that country's series → **(c) Graph Analytics** - build a network between that country and its "neighbours" based on weekly infection counts, assuming neighbours don't share borders → **(d) visualisation**, then an 8-10 slide, <10-min video presentation. Graph analytics is a **required, graded section (SLOs c, d, e)**, not breadth.

⚠️ **Written brief vs. live lecture instruction - a real conflict, worth flagging:** the brief itself says "to determine the neighbouring countries, you can either use the latitude and longitude information from the dataset **or your own knowledge of geography**." Dr. Chen's live lecture explicitly **overrode this** for the majority of the class: "forget about the concept about all the geography concept... the United States may have a neighbouring country as China or Australia as long as it showing the similar patterns... we are defining the relation purely but does it [the data]." He stated this is the single most common mistake he sees "every year" - students who use literal map-adjacency (e.g. "US neighbouring Canada/Mexico") are marked down, because that reintroduces geography through the back door. **Practical takeaway: define "neighbour" via a correlation/similarity threshold on the infection-count time series, not lat/long or a mental map**, even though the written brief technically allows either. If in doubt, default to Chen's verbal instruction over the brief's looser wording - confirmed directly by Monica's question and his answer (§ Q&A below).

#### The actual code practical (a close proxy for A3's method, using a "swimmer daily distance" dataset instead of COVID-19 countries)

1. **Reshape wide → long:** convert a wide table (1 row per swimmer, ~700 daily-distance columns) into a long format (swimmer, date, distance) using `pandas.melt`, then aggregate daily → monthly distance per swimmer.
2. **Regression (per swimmer)** → fit linear regression (month number → distance) for the top-3 swimmers by average distance; the swimmer with the **highest variance/lowest R²** (distance not well explained by time) is carried into clustering - mirrors A3 step (a).
3. **K-Means clustering** on that swimmer's 24 monthly values (elbow method → K=5 in the demo); silhouette score ≈0.5, "relatively good."
4. **Graph construction - the actual technique for A3's step (c):** compute the **Pearson correlation matrix** between every pair of swimmers' monthly-distance patterns. Set a **threshold** (0.3 in the demo, on the ±1 correlation scale) - any pair above threshold gets an **edge**, weighted by the correlation coefficient; pairs below threshold stay unconnected. Lower the threshold → more edges/less isolation; raise it → sparser, more selective graph. Build with `networkx`: empty graph → add nodes → add weighted edges for correlated pairs.
5. **Centrality via `networkx`:** compute degree, betweenness, closeness, eigenvector centrality, and **`networkx.pagerank`** on the constructed graph; scale node size in the visualisation by centrality/PageRank score so visually "bigger" nodes are more central.

#### PageRank - what the lecture adds that Kent's 2017 video (R4) doesn't cover

- ⚠️ **Damping factor (missing from R4):** a small fraction of each node's score is redistributed **randomly** to all pages, not just along its outgoing links. This models occasional random browsing and, critically, **prevents the algorithm from getting trapped in closed loops** (e.g. A→B→C→A forever, never reaching any other node). Kent's video never mentions this safety mechanism.
- **Simplified formula:** `new rank = base score + score received from incoming links`, applied **iteratively** until scores stabilise (stop changing materially between passes) - not a one-shot calculation.
- 🖤 **The final score is a relative importance score, not a class label** - a higher PageRank means "more influential within this specific link structure," not a probability or a category.
- **Same logic generalises** beyond webpages to accounts, papers, products, airports, or genes - any graph with directed, influence-like links.

#### The 5 named types of graph analytics questions (from slide 6 - a cleaner framing than R1's 6-signal checklist)

| Question type | Asks | Example |
|---|---|---|
| **Connectivity** | Are two objects connected? Shortest path? | Fraud rings, supply-chain dependencies, route planning |
| **Centrality** | Which nodes are most important/influential? | Social-media influencers, key webpages, critical infrastructure |
| **Community detection** | Which groups naturally form? | Customer segments, research communities |
| **Similarity** | Which nodes behave alike? | Product recommendations, similar users |
| **Link prediction** | Which connection forms next? | Friend suggestions, product cross-sell |

- This is the practical vocabulary to use when framing an A3 graph-analytics question, alongside the 5-step workflow: **define objects → define relationships → build graph → run analytics → interpret & report.**

#### Q&A takeaways (Monica Taniya Soetanto, re: Assessment 3)

- **Dataset access:** the JHU dataset link in the brief may be stale (last maintained ~2020) - Chen confirmed using the **MyLinkedIn (LMS)-provided copy** of the dataset is acceptable if the original source link is unavailable.
- **"Why cluster after regression?"** Monica's own framing, confirmed correct by Chen: clustering is meant to **capture what the regression couldn't explain** - you pick the country/swimmer with the *highest variance* (weakest regression fit) specifically because that's the case where a simple linear trend misses something, and clustering can reveal the structure regression didn't. Chen was explicit this is an open, "critical thinking" question in the rubric - multiple defensible approaches exist as long as they're justified in the report (e.g. highest variance vs. highest residual variance are both defensible readings).
- **Geography confirmed excluded:** directly answering the neighbours-and-borders question (see the ⚠️ conflict note above) - "forget about the geography concept... we are doing our own definitions to define the correlations and the labelling."

#### Key Takeaways for BDA601
1. **This is the direct A3 dry-run.** The code practical's correlation-threshold graph construction + `networkx` centrality/PageRank is essentially A3 step (c) with swimmers standing in for countries - reuse this method, not a geography-based one.
2. **The geography trap is the single highest-value warning in this module** - Chen explicitly said this is the most common error he sees every year, and it's graded under "Analysis and insights" (30% of A3).
3. **Day-job anchor:** choosing a correlation threshold to decide "is this an edge or not" is the same judgment call as choosing a similarity/distance cutoff for deduplicating Synergetic family records (Module 10's money-laundering analogy) - the threshold is a data-driven decision you justify, not a fixed rule.

---

## Where this module fits

- **Graph analytics is the module's third and last "alternative to relational/warehouse thinking"** after clustering (Module 9, groups records) and association rules (Module 10, finds item co-occurrence) - graphs ask a third kind of question: how are entities *connected*, and what can that connectivity structure itself tell you (Loshin §2, the "choose graph analytics" checklist)?
- **The throughline across four resources:** Loshin (R1) supplies the formal "what is it and when do I choose it" foundation; Erickson (R2) narrows to graph *databases* as the implementation layer and adds concrete fraud/bot use cases; Joshi (R3) is the only hands-on code resource, reframing link prediction as ordinary supervised ML over graph-derived features; Kent (R4) drills into one specific, famous graph metric (PageRank) that both activities lean on.
- **Activity 1** (PageRank ranking of universities) draws directly on R4's vote/dilution explanation - no coding required, just applying the concept to a real tool's output.
- **Activity 2** (Facebook link prediction code walkthrough) draws directly on R3 - the negative/positive sampling steps (§2) are the near-complete answer to "what does this code do and can any of it be removed."
- **Feeds Assessment 3? Yes - directly, and it's graded.** A3 (due Week 12, 40%, SLOs c/d/e) requires regression → K-Means (Module 9) → **Graph Analytics** → visualisation, in that order, on the JHU COVID-19 dataset. Graph analytics is A3 step (c): build a correlation-based network between the highest-variance country and its "neighbours" - **not** a geography-based one, despite the brief's wording (see the Week 11 lecture section above for the full correction and the correlation-threshold method that matches it).
