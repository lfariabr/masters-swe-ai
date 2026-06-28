# MLN601 · Module 5 - One-Pager

> **Classification · Bayes' Rule · Naive Bayes · Generative Learning · Probabilistic Programming**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4.

**Pen legend:** 🖤 Black = core facts / skeleton · 🔵 Blue = examples & connections · 🔴 Red = traps & assessment hooks

---

## 🖤 The Big Idea (box it, top of page)
> **Bayesian learning updates what we believe after observing evidence.** Start with a **prior**, combine it with how likely the evidence is, and obtain a **posterior**.
> 🔵 In classification: given the features `x`, calculate which class `y` is most probable.

## 🖤 Bayes' Rule (write big, centre-left)
```text
P(A | B) = P(B | A) · P(A) / P(B)

posterior ∝ likelihood × prior
```
| Term | Meaning | Wine A2 example |
|---|---|---|
| `P(low)` | **Prior** - belief before this wine | about 37% of wines are low |
| `P(x \| low)` | **Likelihood** - evidence if low | alcohol/acidity pattern among low wines |
| `P(low \| x)` | **Posterior** - updated probability | probability this wine is low |
| `P(x)` | **Evidence** - normalising denominator | probability of seeing these measurements |

🔵 The vertical bar means **given**: `P(low | alcohol)` = probability of low quality given the alcohol measurement.
🔴 `P(A | B) ≠ P(B | A)` - confusing them causes the **base-rate fallacy**.

## 🔴 Base-Rate Fallacy (red warning box)
**Rare event + imperfect test = false positives can dominate.**
```text
Disease prior = 1/1000 · false-positive rate = 5%
10,000 people -> 10 true positives + about 500 false positives
P(disease | positive) ≈ 10 / 510 ≈ 2%, NOT 95%
```
🔵 A2 connection: always predicting the 63% majority class already gives **accuracy 0.633**, while finding **zero** low-quality wines. Accuracy alone hides failure on the minority class.

## 🖤 Discriminative vs Generative (top-tier exam distinction)
| | **Discriminative** | **Generative** |
|---|---|---|
| Learns | `P(y \| x)` or the class boundary | `P(x \| y)` and `P(y)`, then Bayes |
| Question | "Where is the boundary?" | "What does each class look like?" |
| Examples | Logistic Regression, Decision Tree | **Naive Bayes**, GDA |
| Trade-off | fewer assumptions; often wins with more data | strong assumptions; fast and data-efficient |

🔴 Both are supervised and need labelled training examples. Generative does **not** borrow information from a discriminative model.

## 🖤 Naive Bayes (the Module 5 classifier)
For features `x₁ ... xₙ`:
```text
P(y | x₁...xₙ) ∝ P(y) · P(x₁ | y) · ... · P(xₙ | y)
```
The **naive assumption**: features are conditionally independent **given the class**.
🔵 Example: after knowing an email is spam, pretend each word appears independently of every other word.
🔴 Usually unrealistic, but often still a strong, fast baseline. Its probabilities may be poorly calibrated.

## 🖤 Three sklearn variants (choose by feature type)
| Variant | Feature distribution | Typical use |
|---|---|---|
| `GaussianNB` | continuous, Gaussian per class | wine chemistry, Titanic fare |
| `MultinomialNB` | counts / frequencies | word counts, document classification |
| `BernoulliNB` | binary present / absent | yes/no word features |

🔵 **Laplace smoothing:** add 1 to counts so an unseen feature does not make the whole posterior probability zero.

## 🖤 MAP vs MLE (quick comparison)
| **MLE** | **MAP** |
|---|---|
| maximises likelihood | maximises posterior |
| no prior | **prior + likelihood** |
| data speaks alone | prior stabilises limited/noisy data |

Mantra: **MAP = MLE + prior.** As data grows, a reasonable prior usually matters less.

## 🖤 Classification Evaluation (A2 vocabulary)
```text
Precision = TP / (TP + FP)   -> when I predict LOW, how often am I right?
Recall    = TP / (TP + FN)   -> of all real LOW wines, how many did I catch?
F1        = harmonic mean of precision + recall
ROC       = TPR versus FPR across MANY thresholds
AUC       = ranking ability: 0.5 random · 1.0 perfect
```
🔵 AUC `0.80`: in about 80% of random low/high pairs, the real low receives the higher low-quality score.
🔴 AUC is **not** calculated from one confusion matrix - each threshold creates a different confusion matrix and ROC point.

## 🔵 Bayesian Learning Beyond Naive Bayes
- Standard ML often learns **one parameter value**; Bayesian ML learns a **posterior distribution** over possible values.
- Posterior distributions quantify **uncertainty**, useful with limited data or valuable prior knowledge.
- **Probabilistic programming:** describe priors + generative process; PyMC, Stan or Pyro infer the posterior using MCMC / variational inference.
- 🔵 SAROPS: prior search map -> new sightings/search results -> posterior map -> search highest-probability areas.

## 🔴 Pitfalls (marks-losers)
- Ignore the **class prior / imbalance** -> impressive accuracy, useless minority recall.
- Treat `P(test+ | disease)` as `P(disease | test+)` -> base-rate fallacy.
- Say "features are independent" -> incomplete; Naive Bayes assumes independence **conditional on the class**.
- Use the wrong NB variant -> Gaussian for continuous, Multinomial for counts, Bernoulli for binary.
- Interpret posterior as certainty -> it is conditional on the model assumptions and available evidence.

## 🔵 Module 5 in Practice
- **Activity 1 - German Tank:** MLE = highest serial; MVUE adjusts upward; Bayesian model produces a posterior over total production.
- **Activity 2 - Titanic:** use `GaussianNB`, inspect confusion matrix, precision, recall and class imbalance.

## 🔴 Assessment Hook - A2 Classification (40%)
**Same 6,497 wines, new question:** A1 predicted the numeric score; A2 predicts **low `<6` (positive)** vs **high `>=6`**.

| A2 model | Philosophy | Test AUC |
|---|---|---:|
| Majority baseline | no learning | 0.500 |
| Decision Tree tuned | discriminative, required | 0.809 |
| Logistic Regression | discriminative comparator | 0.814 |
| **Gaussian Naive Bayes** | **generative comparator** | **0.771** |

🔵 NB result is defensible: the heatmap shows correlated wine features, violating conditional independence, yet NB still ranks much better than chance.
🔴 The brief requires the **Decision Tree**; NB is supporting Module 5 context. Keep CRISP-DM as the report spine and use AUC + per-class metrics rather than accuracy alone.

---

### Margin prompts (answer in blue while you write)
1. Why can a highly accurate medical test still produce mostly false positives for a rare disease?
2. In the wine A2, what exactly does `P(low | alcohol, acidity, ...)` represent?
3. Why can Gaussian Naive Bayes still work when its independence assumption is violated?
