# Module 5 - Activities Draft (a roadmap to follow)

Two hands-on activities. This is your step-by-step plan + the theory you need to discuss each one. Tick the boxes as you go.

---

## Activity 1 - The German Tank Problem

**Files:** `A1_MLN601_Module-5_Tank_problem_v1.ipynb` (notebook) · `A1_German-Tank-Problem_Drost-2024.pdf` (article)
> Note: the brief cites *Fahey (2019)*; the local article is the equivalent *Drost (2024)* - same problem, same maths.

### The idea
Estimate the **total population size N** (total tanks / lottery tickets / products) from a small sample of **serial numbers**, assuming the numbers are a **discrete uniform** distribution `1..N`. In WWII the Allies estimated German tank output from the serial numbers of captured/destroyed tanks - and were far more accurate than spy intelligence.

### The three estimators to compare
Use the worked sample from the article, serials = `[242, 412, 823, 1429, 1702]`, with `k = 5` samples and max `x = 1702`:

| Estimator | Formula | On the sample | Property |
|---|---|---|---|
| **MLE** (max likelihood) | `N̂ = max(sample)` | **1702** | always **under**estimates (biased low) |
| Mean-based | `N̂ = 2·mean − 1` | **1843** | unbiased but **high variance**; can fall below max (invalid!) |
| **MVUE** (frequentist) | `N̂ = x + (x − k)/k` | **2042** | **minimum-variance** unbiased - the best one |

Key insight: **MLE = the maximum serial number** is the most intuitive first guess, but it can only ever be too low. The **MVUE** adds the average gap back on top of the max.

### The Bayesian angle (the point of this module)
Instead of a single number, put a **prior** on N (e.g. a wide discrete uniform), treat the observed serials as evidence, and use **PyMC3** to compute a **posterior distribution over N**. The payoff is **uncertainty quantification** - you get a credible range for N, not just a point estimate. This is the `prior -> evidence -> posterior` loop from Resources 1 and 5, made executable.

### Steps
1. [ ] Open the notebook, run the imports (note the `pymc3` import).
2. [ ] Read the Drost (2024) article; understand **why MLE (max serial) is the MLE** and why it is biased.
3. [ ] Reproduce the **MVUE** `x + (x−k)/k` and compare to MLE and the mean-based estimate.
4. [ ] Run the **simulation** (true N = 2000): confirm both estimators are unbiased on average but the MVUE has **lower variance**.
5. [ ] Run the **Bayesian/PyMC3** section: inspect the **posterior over N** and its credible interval.
6. [ ] Capture your plots/outputs.

### Discussion-forum answers to prepare
- **Other use cases:** iPhone/product units sold (serial numbers), number of users (sample of IDs), students at a university (matriculation numbers).
- **Is probabilistic programming helpful?** Yes - it turns a point estimate into a posterior with uncertainty, with little hand-derived maths.
- **How else could you solve it?** MLE, the MVUE closed form, or simulation/bootstrap.
- **Caveat to mention:** the maths assumes **random, independent** sampling. Asking friends who all enrolled the same year (clustered matriculation numbers) breaks it.

---

## Activity 2 - Naive Bayes Classification + Titanic

**Reference:** Martin (2018) article + the `pb111` Gaussian Naive Bayes notebook · Titanic dataset.

### The idea
Use a **Gaussian Naive Bayes** classifier to predict a passenger's **survival** from the **fare** they paid. Gaussian NB because `fare` is **continuous** (assumed normally distributed per class) - see Resource 4.

### Steps
1. [ ] Read Martin (2018) for the walkthrough.
2. [ ] Load the Titanic data (download or read the URL into the notebook).
3. [ ] Build the classifier - skeleton:
   ```python
   from sklearn.naive_bayes import GaussianNB
   from sklearn.model_selection import train_test_split
   from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

   X = df[["Fare"]]          # continuous feature -> Gaussian NB
   y = df["Survived"]
   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.2, random_state=42)

   nb = GaussianNB().fit(X_train, y_train)
   preds = nb.predict(X_test)

   print("Accuracy:", accuracy_score(y_test, preds))
   print(confusion_matrix(y_test, preds))
   print(classification_report(y_test, preds))
   print("Class priors P(y):", nb.class_prior_)
   ```
4. [ ] **Interpret** the results.
5. [ ] Share interpretation + any issues to the forum.

### How to interpret (and score marks)
- **Accuracy** alone is misleading - read the **confusion matrix**. Its TP/FP/FN/TN is exactly the **base-rate** story from Resource 1 (Westbury): on imbalanced data a model can look "accurate" while being wrong on the minority class.
- **`class_prior_`** = `P(survived)` and `P(died)` - the **prior** Naive Bayes starts from.
- **Honest limitation to state:** fare alone is a **weak** predictor. A natural extension is adding `Pclass`, `Sex`, `Age` (mixing categorical + continuous would mean separate NB variants or encoding) - good "future work" line.

### Discussion-forum answers to prepare
- How realistic is predicting survival from fare alone? (Weak - fare correlates with class, but ignores sex/age, the strongest signals.)
- What does the **conditional-independence** assumption cost here?
- How did Gaussian NB compare to what you expected?

---

## Quick links
- Concepts behind both: [module05_notes.md](module05_notes.md) (Bayes rule, base rates, generative vs discriminative, Naive Bayes variants, probabilistic programming).
