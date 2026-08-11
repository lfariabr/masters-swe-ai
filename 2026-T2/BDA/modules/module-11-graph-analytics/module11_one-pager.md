# BDA · Module 11 - One-Pager

> **Graphs as a third lens · graph databases · link prediction as supervised ML · PageRank centrality**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **A graph represents entities as nodes and relationships as edges, then asks connectivity questions - who's linked to whom, how strongly, how the structure changes - a third lens alongside clustering (record-grouping) and association rules (item co-occurrence).**
> (Loshin 2013, Ch. 10)

## 🖤 Zone 1 - What graph analytics is, and when to choose it
- **Graph** = **vertices** (nodes - entities) + **edges** (relationships), optionally labeled, directed, weighted, with properties. A plain unlabeled graph has "limited utility."
- **Triples (RDF):** subject → predicate → object, e.g. "John Smith - is father of - Brad Smith." Loshin (2013) calls this a "semantic database" - today usually called an **RDF graph**/triplestore, queried via **SPARQL**.
  - ⚠️ Loshin's claim that "any graph platform must use RDF" is dated - **property graphs** (Cypher/Gremlin/PGQL, no RDF) are a separate, now-dominant paradigm (see Zone 2).

| Signal (choose graphs over a warehouse when...) | What it means |
|---|---|
| **Connectivity** | Need to analyse relationships across many entity types |
| **Undirected discovery** | Loshin's own term - describes the *exploratory approach*, not edge direction |
| **Absence of structure** | No consistent imposed schema |
| **Flexible semantics** | Meaning depends on connection context, not fixed columns |
| **Extensibility** | New sources/streams added on the fly |
| **Knowledge embedded in the network** | The relationships *are* the insight |

- 🔴 **Complementary, not a replacement:** graph analytics augments an existing warehouse/OLAP/Hadoop stack - it doesn't replace it.

## 🖤 Zone 2 - Graph databases (Erickson 2026) ⚠️ source updated since original citation
- Stores nodes/edges as **first-class data** - relationships are directly queryable, not reconstructed via joins. Headline claim: **subsecond** queries vs "hours or days" of relational joins.

| Type | Focus | Best for |
|---|---|---|
| **Property graph** | Analytics/querying; vertices/edges carry attributes | Finance, manufacturing, retail |
| **RDF graph** (knowledge graph) | Data integration, semantic search, triples + URIs | Linked data, LLM grounding (e.g. DBpedia) |

- 🔵 **Six Degrees of Kevin Bacon:** same graph answers different questions via different metrics - **shortest-path** ("Bacon → Streep → Connolly → Miss Piggy"), **degree centrality** ("most costars"), **closeness centrality** ("average distance to everyone").
- 🔴 **Real use cases:** social-media bot detection (91.2% of flagged accounts later suspended/deleted - a strong outcome signal, not a formal labelled-accuracy score) · credit card fraud (deviation from a cardholder's normal location/category pattern) · money laundering (accounts sharing email/phone/address across "different" identities - a join a relational view would struggle to surface cheaply).

## 🔴 Zone 3 - Link prediction as supervised ML ⭐ Activity 2's source (Joshi 2020)
- **Question:** for two unconnected nodes, will a link form? Reframed as ordinary binary classification by deriving features + target **from the graph itself**.
- **Training set from ONE snapshot:**
  1. **Negative samples** - adjacency matrix, all unconnected pairs → `link = 0` (Facebook case: 620 nodes → **19,018** pairs).
  2. **Positive samples** - randomly drop real edges, but only if it doesn't disconnect the graph → `link = 1` (**1,483** pairs).
  3. 🔴 **Class imbalance is structural** (19,018 vs 1,483), not a data bug - hence `class_weight="balanced"` / `is_unbalance: true`.
- ⚠️ Skip step 1 → all-*positive* dataset. Skip step 2 → all-*negative* dataset, **and only step 2 carries the disconnected-graph risk** (it's the one removing real edges).
- **Features:** `node2vec` (biased random walks, like DeepWalk) - pair features = sum of the two nodes' vectors.
- **Results:** Logistic Regression AUC **0.78** vs LightGBM AUC **0.93** (early stop, iteration 208).

## 🖤 Zone 4 - PageRank ⭐ Activity 1's algorithm (Kent 2017)
- **Core idea:** pages "vote" for each other via links. Votes from **high-PageRank pages count more**; each page's vote is **diluted across all its outgoing links** (a page with 2 outgoing links passes more value per link than one with 100).
- 🔴 **Shareholder analogy:** more "shares" (incoming links) = more votes, but every vote cast is itself split across everything that page links to.
- ⚠️ **Historical model, not current reality:** Kent's 2017 explanation is simplified; Google confirms PageRank is now just one of several ranking signals. Activity 1's tool (checkpagerank.net) is **third-party, not Google-affiliated** - its "External Backlinks" number is a raw backlink count, **not** a live PageRank score. Use the vote/dilution mechanics to explain the *concept*, not to claim the tool's number *is* PageRank.
- 🖤 PageRank = one concrete instance of the **centrality** graph metric family (Zone 1/2) applied to the WWW-as-a-graph.

## 🔴 Zone 5 - From class (Week 11, 11/08/2026): THIS is the A3 method ⭐ graded, not breadth
- 🔴 **A3 is 4 steps in order:** (a) linear regression per country (week → infections, pick **highest-variance** country) → (b) **K-Means** on that country's series (Module 9) → (c) **Graph Analytics** - network of that country + its "neighbours" (Module 11) → (d) visualisation. All four are graded (SLOs c/d/e).
- ⚠️ **The single biggest trap, repeated every year:** the written brief says you may use lat/long **or geography knowledge** to define "neighbours." Dr. Chen verbally **overrode this in class** - "forget about the geography concept... the US may neighbour China as long as it shows a similar pattern." Define neighbours by **correlation on the infection-count series only**, never by the map. Students who use real geographic borders get marked down.
- 🔵 **The actual technique (live-demoed on a swimmer dataset, same method for A3's countries):** compute the **Pearson correlation matrix** between every pair's time series → pick a **threshold** (0.3 in the demo, on the fixed ±1 correlation scale) → any pair above threshold gets a weighted edge; below it, no edge. Build with `networkx`: empty graph → add nodes → add edges for correlated pairs → run `degree/betweenness/closeness/eigenvector` centrality + `networkx.pagerank` → scale node size by centrality in the plot.
- 🖤 **PageRank's damping factor** (missing from Kent's 2017 video, R4): a small % of each node's score is redistributed **randomly**, not just along outgoing links - this stops the algorithm getting trapped in a closed loop (A→B→C→A forever) and is why it's run **iteratively** until scores stabilise. Final score = relative importance, not a class label.

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 3 - Model Evaluation** · source code + presentation (7-10 min) · **40%** · due **19/08/2026** · SLOs **c), d), e)**.
> Graph analytics IS A3 step (c), graded - not curriculum breadth. Build the country-neighbour network from **correlation on infection data**, never from actual geography, per Dr. Chen's explicit in-class correction.

## 🔴 If you only memorise 5 things
1. **Graph analytics IS required for A3** (step c, graded) - not optional breadth. Build it right after K-Means, on the same highest-variance country.
2. **Never use real geography to define "neighbours" in A3** - correlation on the data only. This is the #1 mistake Chen sees every year.
3. Link prediction = supervised ML in disguise: drop real edges for positives, unconnected pairs for negatives, extract features with node2vec, classify.
4. PageRank = votes via links, weighted by voter importance, diluted across outgoing links, with a **damping factor** to escape closed loops - run iteratively until stable.
5. checkpagerank.net's "External Backlinks" ≠ Google's actual PageRank score - it's a third-party backlink count, useful for explaining the concept only.

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. "Which staff, subjects, and co-curricular groups cluster around a given student's engagement pattern" is a graph-shaped question. Why would a Synergetic table-per-entity schema struggle to answer it directly?
2. If you had to spot duplicate/synthetic parent-contact records across Synergetic (shared email/phone/address under "different" names), how does that map onto the money-laundering graph example in Zone 2?

### This-week to-dos (still 🕐 in your notes)
- [ ] Activity 1: University Popularity Ranking Using PageRank Graph Analytics (discussion forum) - rank Torrens/VU/RMIT/MIT by checkpagerank.net's External Backlinks, explain PageRank in your own words using Zone 4's vote/dilution mechanics.
- [ ] Activity 2: Facebook Graph Analytics (discussion forum) - summarise the "Dataset Preparation for Model Building" code outputs and justify whether any step could be removed, using Zone 3's negative/positive-sampling breakdown.
