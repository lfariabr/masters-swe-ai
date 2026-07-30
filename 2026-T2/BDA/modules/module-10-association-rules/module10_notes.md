# Module 10 - Association Rules

## Task List

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Kumbhare & Chobe (2014) - An Overview of Association Rule Mining Algorithms | ✅ |
| **2** | Read & summarise Andrewngai (2020) - Understand and Build FP-Growth Algorithm in Python | ✅ |
| **3** | Watch & summarise McCormick (2018) - Machine Learning and AI Foundations: Clustering and Association | ✅ |
| **4** | Read & summarise Shanbhag (2020) - Association Rule Mining | ✅ |
| **5** | Read & summarise Rai (2019/2026) - An Overview of Association Rule Mining and Its Applications | ✅ |
| 6 | Activity 1: Create Association Rules (7 Bad Travel Habits, discussion forum) | 🕐 |
| 7 | Activity 2: Let's Explore FP-Growth (explain the conditional-tree code block, discussion forum) | 🕐 |

**Local sources (this folder):**
- `r1_An-Overview-of-Association-Rule-Mining-Algorithms_Kumbhare-Chobe-2014.pdf` (Resource 1)
- `r2_FP-Growth-Frequent-Pattern-Generation-in-Data-Mining-with-Python_Andrewngai-2020.pdf` (Resource 2)
- `r3_Clustering-and-Association-transcript_McCormick-2018.md` (Resource 3 - video transcript, 3 sub-sections)
- `r4_Association-Rule-Mining_Shanbhag-2020.pdf` (Resource 4)
- `r5_Association-Rule-Mining-Overview-and-Applications_Rai-2019.pdf` (Resource 5; the live upGrad page has since been substantially rewritten/expanded from the original 2019 article - see the erratum note in §5 below)
- `a1_7-Bad-Travel-Habits-and-How-to-Quit-Them_Ditaranto-2020.pdf` (Activity 1 source article)

---

## Key Highlights

### 1. An Overview of Association Rule Mining Algorithms (Kumbhare & Chobe 2014)

**Citation:** Kumbhare, T. A., & Chobe, S. V. (2014). An overview of association rule mining algorithms. *International Journal of Computer Science and Information Technologies, 5*(1), 927-930.
**Local source:** `r1_An-Overview-of-Association-Rule-Mining-Algorithms_Kumbhare-Chobe-2014.pdf`

**Purpose:** A compact academic survey of six association rule mining algorithms, positioning FP-Growth as the endpoint of an evolutionary chain that starts with AIS. This is the resource that supplies the historical "why FP-Growth exists" context R2 assumes you already have.

---

#### 1. Where association rules sit inside data mining

- **Data mining** = process of finding correlations/patterns in large relational databases, covering anomaly detection, clustering, association rule learning, regression, summarisation, classification.
- **Association rule learning** searches for relationships among variables - e.g. a supermarket discovering which products are frequently bought together (**market basket analysis**).
- 🖤 **If/then structure:** association rules are if/then statements uncovering relationships between items - "if the customer buys bread, he may also buy butter." Two criteria drive rule generation: **support** and **confidence**, both required to exceed a user-specified minimum simultaneously.

#### 2. Six algorithms, one evolutionary line

| Algorithm | Core idea | Key drawback |
|---|---|---|
| **AIS** (1993, Agrawal/Imielinski/Swami) | First ARM algorithm; only single-item consequents (`X∩Y ⇒ Z`, not `X ⇒ Y∩Z`) | Too many candidate itemsets generated, most turn out small - wastes space and effort; many database passes |
| **SETM** | Candidate itemsets generated on-the-fly during a scan, counted at the end of the pass (saves transaction ID with each candidate) | Same disadvantage as AIS, plus one entry per support-count occurrence |
| **Apriori** | Level-wise search: k-itemsets explore (k+1)-itemsets; breadth-first + hash tree for efficient counting | Complex candidate generation (time/space/memory-heavy); multiple full database scans |
| **AprioriTID** | Same candidate generation as Apriori, but after the first pass, support is counted from a derived TID-itemset structure, not the raw database | Better than Apriori in **later** passes only |
| **AprioriHybrid** | Uses Apriori in early passes (where it's faster), switches to AprioriTID in later passes | Combines strengths but still inherits both algorithms' complexity |
| **FP-Growth** | Two database scans only; builds a compressed **FP-tree**, mines it recursively with **no candidate generation step at all** | The most complex data structure to implement, but this paper's comparison table shows it winning on every axis |

- 🔴 **Comparison table (data support / speed / accuracy):** FP-Growth scores **"very large" data support, "high" speed in both initial and later phases, and "most accurate"** - strictly better than every predecessor on every criterion the paper tests. This is the paper's explicit conclusion, not implied - **"the performance of FP-growth is better than all other algorithms discussed here."**

#### Key Takeaways for BDA601
1. **This is the "why" behind R2 and R3's shared FP-Growth focus.** Every other resource in this module assumes FP-Growth is the superior choice - this paper is the academic evidence for that claim, tracing the lineage AIS → SETM → Apriori → AprioriTID → AprioriHybrid → FP-Growth as successive fixes to the same two problems (candidate-set explosion, repeated full scans).
2. **Two-scans-only is the number to remember.** Every other algorithm here needs as many passes as the largest frequent itemset; FP-Growth needs exactly 2, regardless of itemset size. That's the concrete, citable reason it wins the comparison table.
3. **Day-job anchor:** this is the same "count candidates vs. compress-and-recurse" tradeoff you'd hit choosing between a naive `GROUP BY` scan-per-threshold approach and a pre-aggregated/indexed structure in a warehouse query - repeated full scans get expensive fast as data grows, which is exactly the drawback table's message.

---

### 2. Understand and Build FP-Growth Algorithm in Python (Andrewngai 2020)

**Citation:** Andrewngai. (2020, 30 October). *Understand and build FP-Growth algorithm in Python*. Towards Data Science. Retrieved from https://towardsdatascience.com/understand-and-build-fp-growth-algorithm-in-python-d8b989bab342
**Local source:** `r2_FP-Growth-Frequent-Pattern-Generation-in-Data-Mining-with-Python_Andrewngai-2020.pdf`

**Purpose:** The module's only from-scratch Python implementation of FP-Growth, and the direct source for Activity 2 - the `mineTree` conditional-tree code the activity asks you to explain lives here.

---

#### 1. Why FP-Growth beats Apriori (mechanically, not just by table)

- Apriori's two shortcomings: **candidate itemsets can grow extremely large**, and **support counting requires scanning the database over and over**.
- FP-Growth's fix: **no candidate generation at all.** All the data is compressed into an **FP-tree** once; the itemset-size problem disappears because the tree is a compact shared structure, and repeated scanning disappears because you traverse the tree instead.

#### 2. FP-tree construction - two stages, two steps each

**Stage 1: build the tree**
1. **Clean & sort:** for each transaction, drop items below `min_support`, then sort the remaining items by frequency, **descending**.
2. **Construct tree + header table:** map each cleaned/sorted itemset to a path in the tree one item at a time. If an item already exists on that branch, increment its counter (share the node); otherwise create a new branch. The **header table** keeps one linked list per unique item, threading together every occurrence of that item across the tree, so you can find all instances of an item without re-traversing the whole tree.

**Stage 2: mine the tree**
1. **Divide into conditional FP-trees:** starting from each frequent 1-item pattern, build its "conditional pattern base" (the set of prefix paths leading to that item), then construct a conditional FP-tree from that base using the exact same Stage-1 method.
2. **Mine each conditional tree recursively** (depth-first) - this is where **pattern growth** happens: frequent patterns are generated by concatenating patterns from the conditional trees, one conditional tree per frequent pattern.

#### 3. The code block Activity 2 asks about: `mineTree` / conditional-tree construction

```python
def mineTree(headerTable, minSup, preFix, freqItemList):
    sortedItemList = [item[0] for item in sorted(headerTable...)]  # lowest frequency first
    for item in sortedItemList:
        newFreqSet = preFix.copy()
        newFreqSet.add(item)
        freqItemList.append(newFreqSet)                              # pattern growth happens here
        conditionalPattBase, frequency = findPrefixPath(item, headerTable)
        conditionalTree, newHeaderTable = constructTree(conditionalPattBase, frequency, minSup)
        if newHeaderTable != None:
            mineTree(newHeaderTable, minSup, newFreqSet, freqItemList)  # recurse into the conditional tree
```

- 🔴 **What this block does:** for every item in the header table (processed **lowest-frequency first**), it (1) grows the current prefix into a new frequent itemset and records it, (2) finds that item's **conditional pattern base** via `findPrefixPath` (walk each occurrence of the item up to the root, collecting the path), (3) builds a **conditional FP-tree** from that pattern base using the same `constructTree` function from Stage 1, and (4) if that conditional tree isn't empty, **recurses** into it with the grown prefix.
- 🔴 **Why it matters:** this is the whole "pattern growth" mechanism in one function - it's how FP-Growth avoids ever generating a candidate itemset explicitly. Each recursive call operates on a strictly smaller, item-specific sub-tree, so the search space shrinks with every level instead of exploding combinatorially the way Apriori's candidate generation does.
- `ascendFPtree` (called inside `findPrefixPath`) is the simplest possible recursive walk: append the current node's item, then recurse into its parent, until `parent == None` (the root). This is literally how a prefix path is read off the tree.

#### 4. FP-Growth vs Apriori, empirically

- **Runtime vs. minimum support:** FP-Growth is always faster; Apriori's runtime spikes sharply once `min_support` drops below a certain point, while FP-Growth barely moves.
- **Runtime vs. transaction count:** both slow down as itemsets grow, but Apriori's slope is much steeper - i.e. **FP-Growth scales better**, the practical version of the paper's "very large data support" claim.
- **Sort order matters:** sorting items in **descending** frequency order (Stage 1, step 1) is always faster than ascending, because high-frequency items are more likely to share branches early - more shared branches = smaller tree = less work. This is a mechanical justification for a rule the other resources state without deriving.

#### 5. A practitioner's caveat (from the article's own conclusion)

- 🔴 A colleague's critique, quoted directly in the article: FP-Growth as taught here **"doesn't take weighing under consideration"** - e.g. a transaction with multiple units of the same item, or other business nuances - which is why some companies build custom variants rather than using the textbook algorithm as-is. Worth citing if Activity 2's discussion asks about real-world limitations.

#### Key Takeaways for BDA601
1. **This IS Activity 2's source code.** The `mineTree`/conditional-tree block the activity asks you to explain is walked through step-by-step above - the answer is "it's the pattern-growth recursion: grow the prefix, build a conditional tree from that item's occurrences, recurse into it," and its significance is that this recursion is *why* FP-Growth needs no candidate generation.
2. **Descending-order sort is the module's most citable "small detail, big effect" fact** - same shape as Module 9's `StandardScaler` lesson: a preprocessing choice that looks cosmetic but measurably changes performance.
3. **Day-job anchor:** the header table's linked-list-per-item is functionally an index - the same reason you'd add a DB index on a frequently-filtered column instead of re-scanning the table every query. FP-tree construction *is* a one-time indexing cost that pays for itself across every subsequent recursive lookup.

---

### 3. Machine Learning and AI Foundations: Clustering and Association (McCormick 2018)

**Citation:** McCormick, K. (2018). *Machine learning and AI foundations: Clustering and association* [Video file]. LinkedIn Learning.
**Local source:** `r3_Clustering-and-Association-transcript_McCormick-2018.md` (transcript, 3 sub-sections: "Intro to association rules and sequence analysis," "Some association rules terminology," "Comparing clustering and association rules")

**Purpose:** The only resource that explicitly bridges Module 9 (clustering) and Module 10 (association rules) - both McCormick's own framing and the direct continuation of the same instructor's voice from earlier modules in this subject.

---

#### 1. Data granularity: Customer ID vs. Transaction ID

- **Minimum data needed:** just a Customer ID and a Product Code/SKU - but this breaks down for **cash customers** with no trackable ID across visits (can't link their pizza purchase to their beer purchase two days later).
- **Fix:** fall back to **Transaction ID + SKU** - working off a single receipt instead of a customer's full history. This is a **granularity trade-off**: Customer ID+SKU gives you a customer's whole basket history (many transactions per ID); Transaction ID+SKU gives you only what's on one receipt (fewer items, but no cross-visit linkage).
- **Sequence analysis** adds a time/date stamp on top - useful when *order* matters (web page navigation sequences, predictive maintenance warning-code sequences before a failure), but McCormick notes it's **not typically applied to retail data** the way plain association rules are.

#### 2. Terminology - the exam-shaped vocabulary

| Term | Definition | Note |
|---|---|---|
| **Antecedent** | the "If" item/code | not literally about time-order (this isn't sequence analysis) |
| **Consequent** | the "Then" item/code | pizza→beer and beer→pizza can *both* be valid rules with the same two products |
| **Confidence** | % of antecedent-buyers who also buy the consequent | "accuracy" of the rule; McCormick's own synonym for it |
| **Rule support** | how many of **all** cases include both the antecedent AND consequent | denominator = everyone, not just antecedent-buyers |
| **Antecedent support** | how many cases include just the antecedent | denominator = antecedent-buyers only - this is what rule support gets divided by (conceptually) to reach confidence |
| **Lift** | how many times more likely the consequent is, given the antecedent, vs. its baseline rate | "buyers of pizza are 3x as likely to buy beer" - a multiplier, not a percentage |

- 🔴 **Confidence vs. support, in one line:** confidence asks "of the people who bought the antecedent, how many also bought the consequent" (narrow denominator); support asks "out of everyone, how many bought both" (wide denominator, tells you the rule's overall *relevance*, not just its accuracy).

#### 3. Clustering vs. association rules: "two sides of the same coin"

- 🔴 **Not a one-to-one mapping.** McCormick's own example: 4 customer clusters generated thousands of association rules. **Clusters are broad, generic patterns over large groups; association rules are granular** (typical rule support might be a couple of percent, not tens of percent) and involve far fewer people per rule.
- 🔵 **Worked example:** Cluster 1 = biggest big-screen-TV buyers, spend 18% on video games, less on game consoles, showing brand commitment (repeat visitors only were clustered). Cross-referencing this cluster against rules with "entertainment/big-screen TV" as the antecedent surfaces rules involving video games and game consoles - i.e. **this cluster looks like great candidates for a game-console promotion**, a conclusion neither technique alone would fully justify.
- 🖤 **Why look through both lenses:** clustering tells you *who* your segments are at a high level; association rules tell you *what specific combinations* drive behaviour within (or across) those segments. Same underlying data, two different questions.

#### Key Takeaways for BDA601
1. **This is the module's terminology anchor** - support/confidence/lift are used, mostly undefined-from-first-principles, in every other resource; McCormick's plain-language definitions (with the pizza/beer example) are the ones to fall back on if a definition elsewhere feels circular.
2. **Direct bridge to Module 9** - if an assessment or exam asks "how does clustering relate to association rules," this resource's cluster-vs-rules granularity distinction (broad/generic vs. narrow/granular) plus the big-screen-TV worked example is the citable answer.
3. **Day-job anchor:** the Customer ID vs. Transaction ID granularity trade-off maps directly onto warehouse fact-table grain decisions - do you have a stable customer key across sessions, or are you stuck working from transaction-level receipts because identity resolution is missing? The same "what can you actually link" constraint applies.

---

### 4. Association Rule Mining (Shanbhag 2020)

**Citation:** Shanbhag, A. (2020, 22 May). *Association rule mining*. Analytics Vidhya. Retrieved from https://medium.com/analytics-vidhya/association-rule-mining-7f06401f0601
**Local source:** `r4_Association-Rule-Mining_Shanbhag-2020.pdf`

**Purpose:** The module's business-storytelling resource - two famous real-world anecdotes (Pop-Tarts before hurricanes, beer-and-diapers) plus a clean two-step mechanical process and the module's most complete worked Apriori example.

---

#### 1. Why association rule mining matters - the two headline stories

- **Walmart & Strawberry Pop-Tarts (2004):** mining trillions of bytes of sales data before hurricanes revealed Pop-Tarts were a top pre-hurricane purchase (no-cook, long shelf life) - Walmart began stocking up on them ahead of storms in following years.
- **Walmart & beer/diapers:** analysis of 1.2M baskets found diapers and beer frequently bought together on **Friday evenings 5-7pm** - moving them closer together boosted sales of both. Interpreted as: men heading home from work grab beer while picking up diapers for infants.
- 🖤 **The pattern, not the mechanism, is the point in both stories** - association rules surfaced a *correlation* worth acting on; a human still supplied the causal story afterward.

#### 2. Four business reasons ARM matters
1. **Sales strategy** - knowing fries→Coke lets you design combos that exploit the pattern.
2. **Marketing strategy** - knowing which products *don't* sell together as well informs targeted promotions (e.g. discount slow-moving Christmas ornaments).
3. **Shelf-life planning** - low-frequency perishables (olives) can be bundled at a discount with a frequently-co-bought item (pizza dough) to move stock before expiry.
4. **In-store organisation** - products that drive each other's sales get moved physically closer (bread next to butter).

#### 3. The two-step mechanical process
- **Step 1 - find frequent itemsets:** an **itemset** is any set of items in a basket (e.g. `[bread, butter, eggs]`). **Support count** = raw frequency of an itemset in the dataset. **Support** = that frequency **relative to total transactions** (e.g. "bread has 80% support" = bread appears in 80 of every 100 transactions). `min_support` is a threshold - itemsets below it are discarded.
- **Step 2 - generate strong rules from frequent itemsets:** uses **confidence** to identify which direction of the relationship is strong. Worked example: itemset `[Bread, Butter]` could mean "bread drives butter sales" (makes sense - most bread dishes involve butter) or "butter drives bread sales" (weaker - butter isn't bread-specific). Confidence of 60% on `{A⇒B}` means 60% of transactions with A also contain B - and critically, **`{A⇒B}` and `{B⇒A}` are different rules with potentially very different confidence values.**

#### 4. The Apriori algorithm, worked step by step

- **Core principle - the Apriori property (downward closure):** "all non-empty subsets of a frequent itemset must also be frequent." If `[Bread, Butter]` is frequent, `[Bread]` and `[Butter]` individually must be frequent too - this lets the algorithm prune the search space instead of testing every possible combination.
- 🔵 **Worked example** (4 transactions, min_support/confidence = 50%):
  - Candidate 1-itemsets: `[A]` (3/4), `[B]`, `[C]` all pass the 50% threshold → `L1 = {A, B, C}`.
  - Candidate 2-itemsets from `L1`: only `[A,C]` (2/4 = 50%) passes → `L2 = {A,C}`.
  - Can't generate candidate 3-itemsets - only 2 items remain in `L2`.
  - **Mining the rule from `[A,C]`:** both `{A⇒C}` and `{C⇒A}` are tested; `{C⇒A}` comes out at **100% confidence**, meaning C almost always predicts A, a stronger, more actionable rule than the reverse direction.
- 🔴 **Two drawbacks of Apriori** (setting up why FP-Growth exists, same message as R1/R2): (1) **computationally intensive** - requires repeated full database scans; (2) **can mine misleading patterns** - e.g. umbrellas placed near a checkout during monsoon season might spuriously "associate" with unrelated grocery items just because people notice and grab one while paying, not because of any real product relationship. **Statistical pattern ≠ causal relationship.**

#### Key Takeaways for BDA601
1. **This is your go-to resource for Activity 1's if-then framing** - the bread/butter worked example is the cleanest illustration in the module of *why* `{A⇒B}` and `{B⇒A}` need to be evaluated as separate rules with separate confidence values, directly relevant when writing the 7 travel-habit if-then rules.
2. **The umbrella caveat is the module's "correlation ≠ causation" checkpoint** - worth citing anywhere an assessment asks you to critique or validate a discovered rule, not just report it.
3. **Day-job anchor:** support vs. confidence is the same "how common is this pattern overall" vs. "how reliable is this pattern when the trigger occurs" distinction you'd want before wiring an automated alert off a data-quality rule - a rule with high confidence but tiny support fires rarely and might not be worth automating; the reverse (common but unreliable) is worse.

---

### 5. Association Rule Mining: What is It, Its Types, Algorithms, Uses, & More (Rai)

**Citation:** Rai, A. *An overview of association rule mining and its applications*. upGrad. Retrieved from https://www.upgrad.com/blog/association-rule-mining-an-overview-and-its-applications/
**Local source:** `r5_Association-Rule-Mining-Overview-and-Applications_Rai-2019.pdf`

**Purpose:** The module's broadest resource - support/confidence/lift with a full worked numeric example, a three-way Apriori/FP-Growth/Eclat comparison, advanced rule types (multi-level, quantitative, negative), and real Python (`mlxtend`) code throughout.

---

⚠️ **Source erratum, worth flagging (same pattern as Module 8/9's book erratum notes):** the notes.md citation describes this as a short 2019 upGrad article on "an overview... and its applications." The live page has since been **substantially rewritten** - it's now dated "Updated on Jul 07, 2026," runs to ~30 minutes of reading, and covers far more ground (Eclat, `mlxtend` code throughout, an extensive India-focused use-case catalogue, an FAQ section) than the original citation describes. Same author, same URL - but treat this as a materially different, more current version of the resource, not the exact article the module citation was written against.

---

#### 1. Association rules formally, and where they sit vs. classification/regression

- **Association rule notation:** `X → Y`, where X and Y are disjoint itemsets. Falls under **unsupervised** learning - no labelled data, no target variable to predict, just co-occurrence pattern discovery.

| Feature | Association Rule Learning | Classification / Regression |
|---|---|---|
| Learning type | Unsupervised | Supervised |
| Input data | Unlabeled transactions | Labeled data |
| Goal | Pattern discovery | Prediction (class or numeric value) |
| Output | Rules (`X → Y`) | Predicted labels or values |
| Example | `{milk, sugar} → {tea}` | `Age → Will Buy Product?` |

#### 2. Support, confidence, lift - formalised with a worked numeric example

| Metric | Formula | Meaning |
|---|---|---|
| **Support** | `P(X ∪ Y)` | how often X and Y appear together across the whole dataset |
| **Confidence** | `P(Y \| X)` | of the transactions containing X, what fraction also contain Y |
| **Lift** | `P(Y \| X) / P(Y)` | how much more likely Y is when X is present, vs. Y's baseline rate |

- 🔵 **Worked example:** 30% of transactions contain both Basmati Rice and Ghee → **support = 0.30**. Of transactions with Basmati Rice, 40% also have Ghee → **confidence = 0.40**. Ghee appears in 20% of all transactions overall → **lift = 0.40/0.20 = 2.0** - Ghee is **twice as likely** to be bought when Basmati Rice is purchased, meaning this is a real association, not just Ghee being popular on its own.
- 🔴 **Lift is the tie-breaker metric** - the same "confidence alone can mislead" caution as Shanbhag's umbrella example, but here it's formalised: confidence only tells you how often Y follows X, not whether that's *more* than Y's baseline popularity. A rule can have high confidence purely because Y is generally popular, and lift is what exposes that.

#### 3. Three algorithms compared - adds Eclat to the module's usual Apriori/FP-Growth pair

| Property | Apriori | FP-Growth | Eclat |
|---|---|---|---|
| Candidate generation | Required, every iteration | Not required | Not required |
| Scan count | Multiple | 2 (fixed) | 1 (vertical transform) |
| Data structure | Candidate lists | FP-tree | TID-lists (vertical format), set intersection |
| Best for | Simple, low-volume datasets | Large/dense datasets | Dense data, fewer unique items; easily parallelisable |

- **Eclat's mechanism** (new to this module vs. R1/R2/R4): transforms data into a **vertical format** - each item becomes a set of transaction IDs it appears in (`A: {1,3,5}`). Support of `{A,B}` = `|TID(A) ∩ TID(B)|` - a set intersection instead of a tree traversal or repeated scan. Trades off poorly when there are many unique items but few transactions (sparse, high-dimensional TID lists = memory overhead).

#### 4. Beyond the basic rule: multi-level, quantitative, negative

- **Multi-level rules:** mine rules at different levels of a product hierarchy (e.g. brand-level "Tata Salt → Aashirvaad Atta" vs. category-level "salt → flour").
- **Quantitative rules:** incorporate numeric attributes (price, quantity, spend) - not directly supported by `mlxtend`, so continuous data must be **discretised/bucketed first** (e.g. `Cart_Total_1000+` as a binary flag) before Apriori/FP-Growth can run on it.
- **Negative rules:** detect absence rather than presence (e.g. `{Not_Vegetables} → {Frozen_Meals}`) - simulated by adding inverse indicator columns to the transaction matrix.

#### 5. Applications catalogue (breadth beyond retail)

- **Market basket/retail:** product bundling, shelf optimisation, inventory planning - the module's default framing (Shanbhag, McCormick).
- **Web/clickstream analysis:** navigation-path discovery, UX bottleneck detection (`{Login→Dashboard→Pricing} → {Exit}`) - this is closer to McCormick's "sequence analysis" than plain association rules, since order matters.
- **Healthcare/bioinformatics:** phenotype-genotype associations, treatment pathway rules, adverse drug event monitoring - rules become interpretable features inside clinical decision support systems.
- **Feature engineering for supervised pipelines:** a triggered rule (`{item A, item B} → {item C}`) becomes a binary feature (`combo_ABC = 1`) fed into a downstream classifier (e.g. Random Forest, LightGBM) - association rules and supervised learning aren't mutually exclusive, they can compose.

#### 6. Benefits and limitations

| Benefits | Limitations |
|---|---|
| Simple to interpret, easy to explain to non-technical stakeholders | Can generate a large number of trivial/redundant rules |
| Works well with categorical/binary/transactional data | Not directly applicable to continuous variables unless discretised |
| Fully unsupervised - works when labels are missing | Computationally expensive on large/dense datasets |
| Integrates as feature engineering for supervised pipelines | Low support/confidence rules can be unreliable |

- 🔴 **No temporal awareness** is called out as a structural limitation: `{login, pricing page} → {exit}` doesn't capture *when* the exit happens - for genuinely time-sensitive questions you need McCormick's sequence analysis, not plain association rules.

#### Key Takeaways for BDA601
1. **This is the module's formula reference** - if an assessment or exam question asks you to *compute* support/confidence/lift rather than just define them, the Basmati Rice/Ghee worked example here is the cleanest template to follow.
2. **Eclat rounds out the algorithm picture** - R1/R2/R4 only compare Apriori vs. FP-Growth; this resource adds the third major family (vertical/TID-based) and explains *when* it wins (dense data, few unique items) vs. loses (sparse, high-cardinality).
3. **Day-job anchor:** the multi-level and quantitative rule types map directly onto warehouse dimension hierarchies (SKU → category → department) and fact-table measures (spend buckets, quantity tiers) - the same discretisation-before-mining step you'd need if you ever ran ARM against warehouse transaction data rather than raw POS receipts.

---

## Where this module fits

- **Modules 9 and 10 are both unsupervised**, but ask different questions: clustering (Module 9) groups *records* by similarity across all their features; association rules (Module 10) find *item-level co-occurrence patterns* within records - McCormick's own framing (§3) is the explicit bridge between them.
- **The throughline across five resources:** the module builds one algorithm family (AIS → SETM → Apriori → AprioriTID → AprioriHybrid → FP-Growth) from the ground up (R1's history) into working code (R2's from-scratch implementation, which **is** Activity 2), then wraps it in business storytelling (R4's Walmart anecdotes) and current industry breadth (R5's Eclat + modern applications catalogue). R3 (McCormick) is the odd one out structurally - it's the terminology and clustering-bridge resource, not another algorithm walkthrough.
- **Activity 1** (7 Bad Travel Habits → if-then rules) is a manual, non-coded exercise in *thinking* like an association-rule miner - Shanbhag's bread/butter directional-confidence example (§4.3) is the most relevant citable reasoning pattern.
- **Activity 2** (explain the FP-Growth conditional-tree code block) draws directly and only on R2 - the `mineTree` walkthrough in §3 of that section is a near-complete answer already.
- **Feeds Assessment 3** (due Week 12, 40%): Assessment 3 requires **K-means** (Module 9) as the required algorithm per the Week 9 lecture, so association rules is background/conceptual breadth for this subject rather than a direct A3 requirement - but the support/confidence/lift metric family is a plausible cross-reference if A3's report discusses evaluation criteria generally.
