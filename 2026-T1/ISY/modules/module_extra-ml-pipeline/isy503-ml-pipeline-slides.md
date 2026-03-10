# ISY503 — ML Pipelines: From Excel to Prediction
## Slide Deck Outline (20–30 min)

---

### Slide 1 — Title
**ML Pipelines: From Excel to Prediction**
*A hands-on walkthrough with the Titanic dataset*

- Speaker: Luis Faria
- Subject: ISY503 Intelligent Systems | Torrens University
- Date: March 2026
- Live demo: Google Colab → [isy503-ml-pipeline-demo.ipynb]

---

### Slide 2 — What Is a Machine Learning Pipeline?
**The suitcase analogy**

A pipeline is just a series of steps — like packing a suitcase:

| Step | What you do | ML equivalent |
|------|-------------|---------------|
| 1 | Decide what to pack | Choose features |
| 2 | Fold/roll clothes | Encode + clean data |
| 3 | Weigh the bag | Train/test split |
| 4 | Take the trip | Train the model |
| 5 | Did the trip go well? | Evaluate accuracy |

> No magic. Just structured steps.

---

### Slide 3 — The Titanic Problem
**"Can we predict who survives?"**

- 1912: RMS Titanic sinks
- 891 passengers in our dataset
- We know: age, sex, ticket class, fare, family aboard
- We want to predict: **survived (1) or died (0)**

Why Titanic?
- Real data. Life-or-death stakes.
- Small enough to fit on your laptop
- Taught in ML courses worldwide since 2012

---

### Slide 4 — What the Data Looks Like
**EDA: The Excel mindset**

Before ML — what would a pivot table tell us?

```
Survival rate by SEX:
  female: 74%
  male:   19%

Survival rate by CLASS:
  1st:  63%
  2nd:  47%
  3rd:  24%
```

> "Women and wealthy passengers survived more. That's human insight — not ML."
> ML will find which *combination* of factors predicts survival for each individual.

---

### Slide 5 — EDA Visualizations
**3 bar charts**

[Show the 3-panel chart from the notebook: survival by sex / class / age band]

Key takeaways:
- Sex is the single strongest predictor
- Class matters a lot (1st class = 3x more likely to survive than 3rd)
- Children had better odds than adults

**Question for the class:** What's missing here? Can these charts predict *individual* outcomes?
→ No. They show group averages. ML predicts for each individual.

---

### Slide 6 — Cleaning the Data
**The suitcase packing step**

Problems in raw data:
- 177 missing ages → filled with median (28 years)
- `sex` is text → needs to become a number (female=0, male=1)
- Some rows have missing `fare` → dropped

Rule: **ML algorithms only understand numbers. No nulls.**

```python
data['age'] = data['age'].fillna(data['age'].median())
data['sex'] = LabelEncoder().fit_transform(data['sex'])
data = data.dropna()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

Train: 712 passengers | Test: 179 passengers

---

### Slide 7 — Algorithm 1: Linear Regression
**The baseline — why it doesn't quite work here**

Linear Regression finds the best straight line through the data.
- Works great for: house prices, temperature, sales forecasts
- Problem here: survival is 0 or 1 — but it predicts -0.2, 1.3...

[Show the raw predictions output from Section 3]

> "A probability of 130%? Of -20%? That makes no sense."
> This is exactly WHY classification algorithms were invented.

Accuracy (with 0.5 threshold): ~79%
→ Not bad, but the tool is wrong for the job.

---

### Slide 8 — Algorithm 1: Why Linear Regression Fails Here
**Visual explanation**

[Diagram: scatter plot of predicted values, many falling outside [0,1]]

The problem:
- Linear Regression tries to predict a *continuous number*
- For binary outcomes, outputs can exceed [0, 1]
- We can patch it (threshold at 0.5) but it's a workaround

**Next step:** Use an algorithm *designed* for classification.

---

### Slide 9 — Algorithm 2: Decision Tree
**Classification done right**

A Decision Tree learns a flowchart of if/else rules:
```
Is sex == male?
  ├── Yes → Is fare < 26?
  │         ├── Yes → Died  (78% chance)
  │         └── No  → ...
  └── No  → Is pclass == 3?
            ├── Yes → Died  (50/50)
            └── No  → Survived (92% chance)
```

**The superpower:** You can *read* and *verify* the rules.
- Compliance teams love this
- Regulators can audit it
- Stakeholders can challenge it

---

### Slide 10 — Algorithm 2: Decision Tree Visual
**[Show the full plot_tree() output from the notebook]**

Reading a tree node:
```
pclass <= 2.5     ← the rule
gini = 0.48       ← how mixed the samples are (0=pure, 0.5=50/50)
samples = 534     ← how many passengers reached this node
value = [333, 201] ← [died, survived]
class = Died      ← majority prediction
```

Accuracy: ~82%
→ Higher than Linear Regression, and fully interpretable.

---

### Slide 11 — Algorithm 3: KNN
**"Find the 5 most similar passengers"**

How KNN works:
1. New passenger arrives
2. Calculate distance from them to every training passenger
3. Find the 5 closest ones (k=5)
4. Count: how many of those 5 survived?
5. Predict the majority

**School canteen analogy:** New kid asks 5 most similar classmates if they like the food → goes with the majority.

Accuracy: ~80%

---

### Slide 12 — Algorithm 3: KNN — How k Affects Accuracy
**[Show the k vs accuracy chart from the notebook]**

- k=1 → overfits (memorizes, bad on new data)
- k=5 → usually a good balance
- k=20 → underfits (too general)

KNN tradeoff:
- ✅ No training step, no assumptions about data shape
- ❌ Slow to predict on large datasets (has to compare to all training data)
- ❌ All features equally weighted by default

---

### Slide 13 — All 3 Algorithms Compared
**Side-by-side results**

| Algorithm | Accuracy | Interpretability | Designed for this? |
|-----------|----------|------------------|--------------------|
| Linear Regression | ~79% | Medium | No ❌ |
| Decision Tree (d=3) | ~82% | High ✅ | Yes ✅ |
| KNN (k=5) | ~80% | Low | Yes ✅ |

**No single winner** — it depends on your goals:
- Need to explain decisions? → Decision Tree
- Need pure accuracy? → Ensemble methods (next slide)
- Quick prototype? → Linear Regression or KNN

---

### Slide 14 — What's Next: Random Forest, SVM, Deep Learning
**The road ahead**

| Algorithm | Core idea | When to use |
|-----------|-----------|-------------|
| Random Forest | 100 Decision Trees vote | Better accuracy, still somewhat interpretable |
| SVM | Widest road between classes | High-dimensional data (text, images) |
| Neural Network | Layers of connected nodes | Images, speech, language |
| Gradient Boosting (XGBoost) | Trees that fix each other's mistakes | Tabular data competitions |

**The Titanic pipeline we built today is the foundation for all of these.**
Every advanced algorithm starts with: clean data → features → split → train → evaluate.

---

### Slide 15 — Q&A
**Questions?**

Key concepts covered today:
- ✅ EDA as the "Excel pivot table" step
- ✅ Data cleaning: median fill, encoding, train/test split
- ✅ Linear Regression as a baseline (and its limitations)
- ✅ Decision Tree: visual, interpretable classification
- ✅ KNN: distance-based classification
- ✅ Accuracy, confusion matrix, classification report

**Notebook:** `isy503-ml-pipeline-demo.ipynb` — open in Google Colab and run all cells.

> "The best way to understand ML is to run it, break it, and fix it yourself."
