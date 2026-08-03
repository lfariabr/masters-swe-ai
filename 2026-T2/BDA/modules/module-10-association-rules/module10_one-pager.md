# BDA · Module 10 - One-Pager

> **Association rules · support/confidence/lift · Apriori vs FP-Growth vs Eclat · clustering's "other half"**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Association rules find if-then patterns in unlabelled transactional data - "if a basket has X, it also tends to have Y" - measured by support (how common), confidence (how reliable), and lift (how much better than chance).**
> (Kumbhare & Chobe 2014; Shanbhag 2020; Rai)

## 🖤 Zone 1 - What this is, and where it sits
- **Unsupervised**, same family as Module 9 clustering - no labels, no target variable, just pattern discovery (Rai).
- But a **different question**: clustering groups *whole records* by similarity (broad, few, generic); association rules find *item-level co-occurrence* within records (narrow, many, granular - typical rule support is just a couple percent).
- `X → Y` notation, X = antecedent ("if"), Y = consequent ("then"). Falls under **market basket analysis** when applied to sales data.
- 🔴 **McCormick's frame ("two sides of the same coin"):** 4 customer clusters → thousands of association rules. Not a 1:1 mapping - cross-reference both for the best insight (his big-screen-TV cluster + game-console rule example).

## 🔴 Zone 2 - The three metrics (memorise the formulas)
| Metric | Formula | Asks |
|---|---|---|
| **Support** | `P(X ∪ Y)` | how often X and Y appear together, out of *all* transactions |
| **Confidence** | `P(Y\|X)` = rule support ÷ antecedent support | of the X-buyers, what % also buy Y - **direction matters**, `{A⇒B} ≠ {B⇒A}` |
| **Lift** | `P(Y\|X) / P(Y)` | is Y *more* likely given X than Y's own baseline rate? catches "Y is just popular" trap |

- 🔵 **Worked example (Rai, corrected):** Basmati Rice + Ghee together = 10% of baskets → support 0.10. Of Rice-buyers, 40% also buy Ghee → confidence 0.40. Ghee alone = 20% of baskets → lift = 0.40/0.20 = **2.0x** (real association, not just Ghee being popular).
- ⚠️ Rai's own article says joint support = 0.30 - **impossible**, since joint support can never exceed either item's own support (0.30 > Ghee's 0.20). Use 0.10.
- 🖤 Rule support and antecedent support **share the same denominator** (all transactions) - confidence is what you get dividing one by the other.

## 🔴 Zone 3 - Algorithm lineage (the exam spine) ⭐ THE GRADED CORE (Activity 2)
```
AIS → SETM → Apriori → AprioriTID → AprioriHybrid → FP-Growth
   (single-item      (level-wise,     (counts from     (Apriori early,     (FP-tree, 2 scans,
    consequent only)  repeated scans) TID-struct after AprioriTID later)   NO candidate gen)
                                       pass 1)
```
| Algorithm | Core idea | Weakness |
|---|---|---|
| **Apriori** | k-itemsets → (k+1)-itemsets, breadth-first, hash tree | repeated full DB scans, candidate explosion |
| **FP-Growth** | compress into **FP-tree** once, mine recursively | most complex structure, but no candidate gen, fixed 2 scans |
| **Eclat** | vertical **TID-lists** per item, support = `\|TID(A)∩TID(B)\|` | best on dense data/few unique items; poor when many unique items (sparse) |

- 🖤 **Apriori property (downward closure):** all non-empty subsets of a frequent itemset must also be frequent - lets algorithms prune the search space.
- 🔴 **FP-tree build, 2 stages:** (1) clean & sort items **descending by frequency** per transaction, (2) build tree + **header table** (linked list per item, no re-traversal needed).
- 🔴 **Mine stage:** for each item (lowest-frequency first) → grow prefix → build **conditional pattern base** (prefix paths to that item) → build **conditional FP-tree** → recurse (`mineTree`). This recursion = the whole "pattern growth," and why FP-Growth needs zero candidate generation.
- 🖤 Descending sort > ascending: shared branches early = smaller tree = less work.

## 🖤 Zone 4 - Real-world stories + limitations
- **Walmart Pop-Tarts (2004):** pre-hurricane spike, no-cook/long-shelf-life → they now pre-stock ahead of storms.
- **Walmart beer + diapers:** Friday 5-7pm pattern, moved closer together, sales rose.
- **Fries → Coke, bread → butter:** combo-meal / shelf-placement business logic.
- 🔴 **Correlation ≠ causation:** umbrellas near checkout in monsoon season "associate" with random groceries just from foot traffic, not real product relationship - a human must supply the causal story.
- **Limitations:** many trivial/redundant rules; not directly usable on continuous data (must **discretise** first, e.g. `Cart_Total_1000+` flag); no temporal awareness (use McCormick's **sequence analysis** if order/time matters - web nav paths, predictive maintenance, NOT typical retail).

## 🔵 Zone 5 - Beyond basic rules + applications
- **Multi-level:** brand vs category hierarchy ("Tata Salt → Aashirvaad Atta" vs "salt → flour").
- **Quantitative:** numeric attrs bucketed first (price/qty tiers).
- **Negative rules:** absence patterns (`{Not_Vegetables} → {Frozen_Meals}`).
- **Applications:** retail bundling/shelf/inventory · web/clickstream UX bottlenecks · healthcare phenotype-treatment rules · **feature engineering** (a triggered rule becomes a binary feature like `combo_ABC=1` feeding a downstream classifier - composes with supervised learning, doesn't replace it). School-domain version: `{low attendance, missing Mandatory Data} → {fee statement overdue}` becoming a flag inside a Student 360 risk view.

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 3 - Model Evaluation** · source code + presentation (7-10 min) · **40%** · due **19/08/2026** · SLOs **c), d), e)**.
> A3's required algorithm is **K-means** (Module 9), not association rules - Module 10 is conceptual breadth, not a direct A3 requirement. If A3's report discusses evaluation criteria generally, support/confidence/lift is a legitimate cross-reference point (same "metric ≠ verdict" caution as Module 9's inertia/silhouette).

## 🔴 If you only memorise 5 things
1. Support/confidence/lift formulas + that confidence is directional (`{A⇒B} ≠ {B⇒A}`).
2. Apriori = candidate generation + repeated scans (slow); FP-Growth = FP-tree + 2 scans, no candidates (fast); Eclat = vertical TID-list intersection (best on dense/few-unique-items data).
3. The Apriori property: subsets of a frequent itemset must also be frequent.
4. Clustering and association rules are "two sides of the same coin" - same unlabelled data, different question (record-grouping vs item co-occurrence).
5. A3 needs K-means (Module 9), not Module 10 - this module is breadth, not the graded deliverable.

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. If you ran Apriori/FP-Growth against Synergetic/SEQTA/Schoolbox data, would you use Student ID as the "basket" grain - and what breaks if a system's event log can't reliably link back to a stable Student ID?
2. The FP-tree's header table (linked list per item) is functionally an index - what Student 360 or Synergetic query would you speed up the same way, by building a one-time structure instead of re-scanning on every lookup?

### This-week to-dos (still 🕐 in your notes)
- [ ] Activity 1: Create Association Rules (7 Bad Travel Habits, discussion forum) - write if-then rules using Shanbhag's bread/butter directional-confidence reasoning.
- [ ] Activity 2: Let's Explore FP-Growth (explain the `mineTree` conditional-tree code block, discussion forum) - answer is in R2 §3: grow prefix → conditional pattern base → conditional FP-tree → recurse.
